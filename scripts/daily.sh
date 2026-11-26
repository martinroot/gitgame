#!/bin/bash
export PATH="$HOME/.bun/bin:$PATH"
exec 9>/home/drogame/build/.daily.lock; flock -n 9 || exit 0
cd /home/drogame/vibegame
for i in 1 2 3; do /usr/bin/python3 game_crawler.py --discover >> cron.log 2>&1; sleep 65; done
/usr/bin/python3 game_crawler.py --enrich >> cron.log 2>&1
cd /home/drogame/build
/usr/bin/python3 auto_deploy.py --n 80 >> autodeploy.log 2>&1
