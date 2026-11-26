#!/bin/bash
#nonstop autodeploy wrapper: one wave at a time (flock), batch --n
exec 9>/home/drogame/build/.autodeploy.lock
flock -n 9 || { echo "$(date +%H:%M) already running"; exit 0; }
cd /home/drogame/build
/usr/bin/python3 auto_deploy.py --n 8 >> /home/drogame/build/autodeploy.log 2>&1
