#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/28 15:01
# @Author  : hardyxia
# @File    : account.py
from django.shortcuts import render, redirect, reverse, resolve_url
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt


class IndexView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'cmdb/index.html', {"index_active": "active"})


class LoginView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'cmdb/../../templates/common/login.html')

    def post(self, request, *args, **kwargs):
        errors = {}
        _username = request.POST.get('username', '')
        _password = request.POST.get('password', '')
        user = auth.authenticate(username=_username, password=_password)
        if user and user.is_active:
            auth.login(request, user)
            next_url = request.GET.get("next", "/")
            return redirect(next_url)
        else:
            errors['error'] = '用户名或密码错误'
        return render(request, 'cmdb/../../templates/common/login.html', {'errors': errors})


class LogoutView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LogoutView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return HttpResponseRedirect(reverse('login'))


