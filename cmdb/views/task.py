#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/4 17:12
# @Author  : hardyxia
# @File    : task.py
from django.shortcuts import render, redirect, resolve_url, HttpResponse
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from cmdb import models
import json
from django.contrib.auth.decorators import login_required
from utils.task_manager import MultiTaskManger
from utils.pagination import page


def json_date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.strftime("%Y-%m-%d %T")


class SSHHistoryView(View):
    '''历史登录'''

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SSHHistoryView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        title = ['操作用户', '操作IP', '远程用户', '远程主机', '登录时间']
        response = models.WebHistory.objects.order_by('-id')
        total = response.count()
        response = page(request, list(response))
        return render(request, 'cmdb/task_history.html', {"title": title, "total": total,
                                                          "response": response,
                                                          "task_active": "active open",
                                                          "ssh_history_active": "active open", })


class TaskCMDView(View):
    '''批量命令'''

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TaskCMDView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, "cmdb/task_cmd.html", {"task_active": "active open",
                                                      "task_cmd_active": "active open", })


class TaskFileTransfer(View):
    """批量文件"""

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TaskFileTransfer, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'cmdb/task_file.html', {"task_active": "active open",
                                                       "task_file_active": "active open", })


class TaskResultView(View):
    '''获取任务返回结果'''
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TaskResultView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        task_id = request.GET.get('task_id')
        task_obj = models.Task.objects.get(id=task_id)
        task_log_results = list(task_obj.tasklogdetail_set.values('id', 'result', 'status', 'start_date', 'end_date'))

        return HttpResponse(json.dumps(task_log_results, default=json_date_handler))


class TaskView(View):
    '''接受任务'''

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TaskView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print("--->", request.POST)
        task_data = json.loads(request.POST.get('task_data'))
        print("--->selcted hosts", task_data)

        task_obj = MultiTaskManger(request)
        selected_hosts = list(task_obj.task.tasklogdetail_set.all().values('id', 'bind_host__host__eip_address',
                                                                           'bind_host__host__hostname',
                                                                           'bind_host__remote_user__username'))

        return HttpResponse(json.dumps({'task_id': task_obj.task.id, 'selected_hosts': selected_hosts}))


"""
@login_required
def multitask_file_transfer(request):
    return render(request, 'cmdb/multitask_file_transfer.html')



@login_required
def task_result(request):
    task_id = request.GET.get('task_id')
    task_obj = models.Task.objects.get(id=task_id)
    task_log_results = list(task_obj.tasklogdetail_set.values('id', 'result', 'status', 'start_date', 'end_date'))

    return HttpResponse(json.dumps(task_log_results, default=json_date_handler))


@login_required
def task(request):
    print("--->", request.POST)
    task_data = json.loads(request.POST.get('task_data'))
    print("--->selcted hosts", task_data)

    task_obj = MultiTaskManger(request)
    selected_hosts = list(task_obj.task.tasklogdetail_set.all().values('id', 'bind_host__host__eip_address',
                                                                       'bind_host__host__hostname',
                                                                       'bind_host__remote_user__username'))

    return HttpResponse(
        json.dumps({'task_id': task_obj.task.id, 'selected_hosts': selected_hosts})
    )
"""
