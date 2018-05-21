#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 16:40
# @Author  : hardyxia
# @File    : urls.py
from django.conf.urls import url
from cmdb.views import instance, home, task

urlpatterns = [

    # 资产信息部分
    url(r'^instance$', instance.InstanceView.as_view(), name='instance'),
    url(r'^instance/detail/(\w+.*)$', instance.InstanceDetailView.as_view(), name='instance_detail'),
    url(r'^instance/delete/(\w+.*)$', instance.InstanceDeleteView.as_view(), name='instance_delete'),
    url(r'^instance/edit/(\w+.*)$', instance.InstanceEditView.as_view(), name='instance_edit'),
    url(r'^instance/add$', instance.InstanceAddView.as_view(), name='instance_add'),
    url(r'^instance/ssh$', instance.WebSSHView.as_view(), name='instance_ssh'),
    # url(r'^instance/ssh$', instance.web_ssh, name='instance_ssh'),

    # 登录用户
    url(r'^bind_user$', instance.BindUserView.as_view(), name='bind_user'),
    url(r'^bind_user/add$', instance.BindUserAddView.as_view(), name='bind_user_add'),
    url(r'^bind_user/detail/(\d+)$', instance.BindUserDetailView.as_view(), name='bind_user_detail'),
    url(r'^bind_user/delete/(\d+)$', instance.BindUserDeleteView.as_view(), name='bind_user_delete'),
    url(r'^bind_user/edit/(\d+)$', instance.BindUserEditView.as_view(), name='bind_user_edit'),

    # 常用URL
    url(r'^service_url$', instance.ServiceUrlView.as_view(), name='service_url'),
    url(r'^service_url/detail/(\d+)$', instance.ServiceUrlDetailView.as_view(), name='service_url_detail'),
    url(r'^service_url/delete/(\d+)$', instance.ServiceUrlDeleteView.as_view(), name='service_url_delete'),
    url(r'^service_url/edit/(\d+)$', instance.ServiceUrlEditView.as_view(), name='service_url_edit'),
    url(r'^service_url/add$', instance.ServiceUrlAddView.as_view(), name='service_url_add'),

    # 任务相关
    url(r'^task_cmd$', task.TaskCMDView.as_view(), name='task_cmd'),
    url(r'^ssh_history$', task.SSHHistoryView.as_view(), name='ssh_history'),
    # url(r'^task_file$', task.multitask_file_transfer, name="task_file$"),
    url(r'^task$', task.task, name="multitask"),
    url(r'^task_result$', task.task_result, name="task_result"),

]
