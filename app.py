"""
app.py

Create By Mephis Pheies <mephistommm@gmail.com>

Description:
  Create flask app and add the route to app.

Copyright (c) 2016, Mephis Pheies.
License: MIT see LICENSE for more details

"""
from flask import (request, Flask, abort)
from towerslack import (create_payload, send_payload)

app = Flask(__name__)


@app.route('/<path:hookpath>', methods=['POST'])
def index(hookpath):

    tower_event = request.headers.get('X-Tower-Event')
    if not tower_event:
        abort(403)  # forbiden

    signature = request.headers.get('X-Tower-Signature')
    if signature and signature[0] not in ('@', '#'):
        signature = None

    payload = create_payload(request.get_json(), tower_event)
    url = 'https://hooks.slack.com/services/{}'.format(hookpath)
    send_payload(payload, url, signature)

    return "ok", 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
