#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/24 17:48
# @Author  : hardyxia
# @File    : cache.py
from django.conf import settings
from django.core.cache import cache
import json


class OperationCache(object):
    def __init__(self, func_name):
        self.key = 'view_of_%s' % func_name

    def write_to_cache(self, value):
        value = json.dumps(value)
        cache.set(self.key, value, settings.REDIS_TIMEOUT)
        return True

    def read_from_cache(self):
        value = cache.get(self.key)
        if value:
            data = json.loads(value)
            return data
        else:
            return False
