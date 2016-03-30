#!/usr/local/bin/python

import os
import sys

path='/mnt/website/shi_xiong_de_yi_gui/server/' #change to your path.DON'T foget the last'/'

sys.path.append(path)
sys.path.append(path+'ShiXiongDeYiGui')

os.environ['DJANGO_SETTINGS_MODULE'] = 'ShiXiongDeYiGui.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
