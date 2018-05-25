#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/24 11:53
# @Author  : hardyxia
# @File    : container.py
from django.shortcuts import render, redirect, resolve_url, reverse
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class LogoutView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LogoutView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return HttpResponseRedirect(reverse('login'))
