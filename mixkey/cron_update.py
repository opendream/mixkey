#! /usr/bin/env python

import sys
import os


def setup_environment():
    pathname = os.path.dirname(sys.argv[0])
    sys.path.append(os.path.abspath(pathname))
    sys.path.append(os.path.normpath(os.path.join(os.path.abspath(pathname), '../')))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

setup_environment()

from domain.models import *

inst_list = ['Data', 'DataTenMinute', 'DataThirtyMinute', 'DataHour', 'DataDay', 'DataWeek', 'DataMonth', 'DataYear']

for Inst in inst_list:
    Inst = eval(Inst)
    for d in Inst.objects.filter(water_level_raw__isnull=True).order_by('-created')[0:10]:
        d.save()
