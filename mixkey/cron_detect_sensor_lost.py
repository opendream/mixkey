#! /usr/bin/env python

import sys
import os


def setup_environment():
    pathname = os.path.dirname(sys.argv[0])
    sys.path.append(os.path.abspath(pathname))
    sys.path.append(os.path.normpath(os.path.join(os.path.abspath(pathname), '../')))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    
setup_environment()

from domain.tasks import detect_sensor_lost
detect_sensor_lost()

print 'run cron detect complete'
