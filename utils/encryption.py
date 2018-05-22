#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/18 17:38
# @Author  : hardyxia
# @File    : encryption.py

from cryptography.fernet import Fernet
import base64

key = 'fV008Pw20qHuRBLG4OPmUUGRkz2J1b3H'

key = base64.urlsafe_b64encode(key.encode('utf-8'))


def encrypt_p(password):
    f = Fernet(key)
    p1 = password.encode()
    token = f.encrypt(p1)
    p2 = token.decode()
    return p2


def decrypt_p(password):
    f = Fernet(key)
    p1 = password.encode()
    token = f.decrypt(p1)
    p2 = token.decode()
    return p2

