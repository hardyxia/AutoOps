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
    # url(r'^instance/ssh$', instance_views.WebSSHView.as_view(), name='instance_ssh'),
    url(r'^instance/ssh$', instance.web_ssh, name='instance_ssh'),

    # 登录用户
    url(r'^bind_user$', instance.BindUserView.as_view(), name='bind_user'),
    url(r'^bind_user_add$', instance.BindUserAddView.as_view(), name='bind_user_add'),
    # url(r'^bind_user/detail/(\w+.*)$', instance_views.BindUserView.as_view(), name='bind_user_detail'),
    # url(r'^bind_user/delete/(\w+.*)$', instance_views.InstanceDeleteView.as_view(), name='bind_user_delete'),
    # url(r'^bind_user/edit/(\w+.*)$', instance_views.InstanceEditView.as_view(), name='bind_user_edit'),

    # 常用URL
    url(r'^service_url$', instance.ServiceUrlView.as_view(), name='service_url'),
    url(r'^service_url/detail/(\d+)$', instance.ServiceUrlDetailView.as_view(), name='service_url_detail'),
    url(r'^service_url/delete/(\d+)$', instance.ServiceUrlDeleteView.as_view(), name='service_url_delete'),
    url(r'^service_url/edit/(\d+)$', instance.ServiceUrlEditView.as_view(), name='service_url_edit'),

    # 任务相关
    url(r'^job_cmd$', task.JobCMDView.as_view(), name='job_cmd'),
    url(r'^job_history$', task.JobHistoryView.as_view(), name='job_history'),
    # url(r'^job_file$', job.multitask_file_transfer, name="job_file$"),
    url(r'^job$', task.job, name="multitask"),
    url(r'^job_result$', task.job_result, name="task_result"),

]
