#! /bin/bash
cd /home/labs/.virtualenvs/mixkey
source bin/activate

python /web/sites/mixkey/source/mixkey/mixkey/cron_detect_sensor_lost.py
