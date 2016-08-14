#!/bin/bash
# This file init create the base directory of funs
# 
# Author: Mephis Pheies <mephistommm@gmail.com>
# Copyright (c) 2016, Mephis Pheies.
# License: MIT see LICENSE for more details
#
# Begin ---


mkdir -p logs/nginx  logs/supervisor logs/uwsgi

echo "Funs init sucess!"
echo "If you has readied your python3 flask project,"
echo "you should go to config uwsgi file in ./configs/uwsgi_conf.d/config.ini,"
echo "then run:"
echo "  docker-compose up -d"
# End  ---
