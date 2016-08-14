#!/bin/bash
# This file run project start file , then launch all service.
# You should write your project start logs in project_start.sh.
#
# Author: Mephis Pheies <mephistommm@gmail.com>
# Copyright (c) 2016, Mephis Pheies.
# License: MIT see LICENSE for more details
#
# Begin ---

bash -c ./funs_start.sh
# start supervisor service
service supervisor start > /dev/null 2>&1
# start nginx at foreground
nginx -g 'daemon off;'

# End ---
