FROM nginx
MAINTAINER Mephis Pheies <mephistommm@gmail.com>

ENV REBUILD_DAY 05.08.2016

# install base dependences
RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    supervisor \
    && pip3 install uwsgi

# create project directory
RUN mkdir -p /opt/project /var/log/project
# create uwsgi config directory
RUN mkdir -p /etc/uwsgi/conf.d

# while configing nginx.conf and supervisord.conf, you should
# put project files to /opt/project directory (-v /host/project_dir:/opt/project)
# write project log files path as /var/log/project, following two env varialbe
# are provided to you
ENV PROJECT_PATH=/opt/project PROJECT_LOG=/var/log/project

# only expose 80 for nginx
EXPOSE 80
# volume all conf.d directories and project root path
VOLUME /opt/project /etc/nginx/conf.d /etc/supervisor/conf.d /etc/uwsgi/conf.d
# volume all log path
VOLUME /var/log/nginx /var/log/supervisor /var/log/project

COPY ./enterscript.sh /root/
WORKDIR /opt/project

CMD ["/root/enterscript.sh"]
