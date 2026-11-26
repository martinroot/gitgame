#!/bin/bash
# непрерывный автодеплой: одна копия демона (flock), волны back-to-back
exec 9>/home/drogame/build/.autodeploy_daemon.lock
flock -n 9 || exit 0
export PATH="$HOME/.bun/bin:$PATH"
cd /home/drogame/build
while true; do
  /usr/bin/python3 auto_deploy.py --n 12 >> /home/drogame/build/autodeploy.log 2>&1
  sleep 15
done
