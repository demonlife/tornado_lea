#encoding: utf8

'''
配置环境监测
'''
from __future__ import absolute_import

import os

if not os.environ.get('PYTHON_TORNADO'):
    from .config_local import *
else:
    from .config_online import *

