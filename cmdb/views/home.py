#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/28 15:01
# @Author  : hardyxia
# @File    : home.py
from django.shortcuts import render, redirect, resolve_url, reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class IndexView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'cmdb/index.html', {"index_active": "active"})


def login(request):
    errors = {}
    try:
        if request.method == "POST":
            _username = request.POST.get('username', '')
            _password = request.POST.get('password', '')
            user = auth.authenticate(username=_username, password=_password)
            if user and user.is_active:
                auth.login(request, user)
                next_url = request.GET.get("next", "/")
                return redirect(next_url)
            else:
                errors['error'] = '用户名或密码错误'

    except Exception as e:
        print(e)
    return render(request, 'cmdb/login.html', {'errors': errors})


@login_required
def change_password(request, user_id):
    errors = {}
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user = User.objects.get(id=user_id)
        if password1 == password2:
            user.set_password(password1)
            user.save()
            return redirect(reverse('login'))
        else:
            errors['error'] = '两次新密码不一致,请重新输入'
    return render(request, 'user/change_password.html', {'errors': errors})


@login_required
def logout(request):
    auth.logout(request)
    return redirect(resolve_url(login))
