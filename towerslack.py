"""
towerslack.py

Created By Hsiaoming Yang.

Modified By Mephis Pheies <mephistommm@gmail.com>

Description:
  Change the format of datas of Tower.im webhook into slack attachment.

Copyright (c) 2015, Hsiaoming Yang.
License: BSD 3

All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.
    * Neither the name of the copyright holder nor the names of its contributors
      may be used to endorse or promote products derived from this software
      without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

"""

import requests

TOWER_ICON = 'http://www.cnplugins.com/uploads/crximage/201503/www.cnplugins.com_dfhmgoomjkcdlfclkpjpmhjgpdakijke_logo.jpg'

TOWER_PROJECT_PREFIX = 'https://tower.im/projects/'
TOWER_MEMBER_PREFIX = 'https://tower.im/members/'

MESSAGES = {
    'created': '创建了',
    'updated': '更新了',
    'deleted': '删除了',
    'commented': '评论了',
    'archived': '归档了',
    'unarchived': '激活了',
    'started': '开始处理',
    'paused': '暂停处理',
    'reopen': '重新打开了',
    'completed': '完成了',
    'deadline_changed': '更新截止时间',
    'sticked': '置顶了',
    'unsticked': '取消置顶',
    'recovered': '恢复了',

    # special
    'assigned': '指派',
    'unassigned': '取消指派',
    'documents': '文档',
    'topics': '讨论',
    'todos': '任务',
    'todolists': '任务清单',
    'attachments': '文件',
}

COLORS = {
    'created': '#439FE0',
    'updated': 'warning',
    'completed': 'good',
    'deleted': 'danger',
}

TOWER_NAME = 'Tower'
TIMEOUT = 4  #seconds


def http_post(count, url, **kwargs):
    try:
        requests.post(url, **kwargs)
    except requests.exceptions.Timeout:
        if count >= 5:
            print("Timeout occurred")
        else:
            return http_post(count + 1, url, **kwargs)


def get_subject_url(project_url, tower_event, guid):
    if tower_event == 'topics':
        tower_event = 'messages'
    elif tower_event == 'documents':
        tower_event = 'docs'
    return '{prt_url}{event}/{guid}/'.format(
        prt_url=project_url, event=tower_event, guid=guid)


## export
def send_payload(payload, url, channel=None):
    if TOWER_NAME:
        payload['username'] = TOWER_NAME
    if TOWER_ICON:
        payload['icon_url'] = TOWER_ICON
    if channel:
        payload['channel'] = channel

    http_post(
        0,
        url,
        json=payload,
        headers={'Content-Type': 'application/json'},
        timeout=TIMEOUT)


## export
def create_payload(body, tower_event):
    action = body['action']
    data = body['data']

    attachment = {}
    color = COLORS.get(action)
    if color:
        attachment['color'] = color

    project = data.pop('project')
    project_url = '{}{}/'.format(TOWER_PROJECT_PREFIX, project['guid'])

    keys = list(data.keys())
    subject = data.pop(keys[0]) if len(keys) == 1 else data.pop(
        tower_event[:-1])
    subject_url = get_subject_url(project_url, tower_event, subject['guid'])

    author = subject.get('handler')
    if author:
        attachment['author_name'] = author['nickname']
        author_link = '{}{}/'.format(TOWER_MEMBER_PREFIX, author['guid'])
        attachment['author_link'] = author_link

    text = '{msg_action} <{prt_url}|#{prt_name}> 的{msg_event} <{sbt_url}|{sbt_title}>'.format(
        msg_action=MESSAGES.get(action, action),
        prt_url=project_url,
        prt_name=project['name'],
        msg_event=MESSAGES.get(tower_event, tower_event),
        sbt_url=subject_url,
        sbt_title=subject['title'], )
    if action in ['assigned', 'unassigned']:
        assignee = subject.get('assignee')
        if assignee:
            text = '{} 给 *{}*'.format(text, assignee['nickname'])

    comment = data.get('comment')
    if comment:
        content = comment['content']
        lines = content.strip().splitlines()
        content = lines[0]
        if len(lines) > 1:
            content += ' ...'
        text = '{}\n> {}'.format(text, content)

    attachment['text'] = text
    attachment['mrkdwn_in'] = ['text']
    return {'attachments': [attachment]}
