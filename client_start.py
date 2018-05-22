#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/22 10:18
# @Author  : hardyxia
# @File    : client_start.py

import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutoOps.settings")
    import django

    django.setup()

    from utils import main

    obj = main.HostManager()
    obj.interactive()