#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/24 11:56
# @Author  : hardyxia
# @File    : release.py

from django.shortcuts import render, redirect, resolve_url, reverse
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from utils.release import JenkinsApi
from utils.pagination import page
from utils.cache import OperationCache
import inspect

jenkins = JenkinsApi()
# 创建一个cache对象
cache_obj = OperationCache(inspect.stack()[0][3])


class ReleaseListView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ReleaseListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        title = ['项目名称', '运行状态', '是否可运行', '项目描述', ]

        cache_data = cache_obj.read_from_cache()
        if cache_data:
            print('from  redis ====================')
            response = cache_data.get('response')
            total = cache_data.get('total')
        else:
            print('from  api ====================')
            details = jenkins.get_job_details()
            response = details.get('job_list')
            total = details.get("job_count")
            data = {"response": response, "total": total}
            cache_obj.write_to_cache(data)
        response = page(request, response)

        return render(request, 'release/release.html', {"response": response,
                                                        'title': title,
                                                        "total": total,
                                                        "page": 10,
                                                        "release_active": "active open",
                                                        "release_list_active": "active"})


class JobBuildView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(JobBuildView, self).dispatch(request, *args, **kwargs)

    def get(self, request, job_name, *args, **kwargs):
        details = jenkins.get_job_details()
        response = details.get('job_list')
        total = details.get("job_count")
        for job in details.get('job_list'):
            if job["job_name"] == job_name:
                job['job_is_running'] = True
        data = {"response": response, "total": total}
        cache_obj.write_to_cache(data)
        jenkins.build_job(job_name,params=None)
        for job in details.get('job_list'):
            if job["job_name"] == job_name:
                job['job_is_running'] = False
        data = {"response": response, "total": total}
        cache_obj.write_to_cache(data)
        return HttpResponseRedirect(reverse('release_list'))
