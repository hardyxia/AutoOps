#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 16:40
# @Author  : hardyxia
# @File    : urls.py
from django.conf.urls import url
from release.views import release

urlpatterns = [
    # 发布管理
    url(r'^list$', release.ReleaseListView.as_view(), name='release_list'),
    url(r'^job_build/(\w+.*)$', release.JobBuildView.as_view(), name='job_build'),
    # url(r'^instance/delete/(\w+.*)$', instance.InstanceDeleteView.as_view(), name='instance_delete'),
    # url(r'^instance/edit/(\w+.*)$', instance.InstanceEditView.as_view(), name='instance_edit'),
    # url(r'^instance/add$', instance.InstanceAddView.as_view(), name='instance_add'),
    # url(r'^instance/ssh$', instance.WebSSHView.as_view(), name='instance_ssh'),

]
