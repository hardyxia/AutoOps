#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/4 17:17
# @Author  : hardyxia
# @File    : task_manager.py

import json, os, subprocess
from django import conf
from cmdb import models


class MultiTaskManger(object):
    """负责解析并触发批量任务"""

    def __init__(self, request):
        self.request = request
        self.call_task()

    def task_parser(self):
        """解析任务"""
        self.task_data = json.loads(self.request.POST.get("task_data"))

    def call_task(self):
        self.task_parser()

        if self.task_data["task_type"] == 0:  # cmd
            self.cmd_task()

        elif self.task_data["task_type"] == 1:  # file transfer
            self.file_transfer_task()

    def cmd_task(self):
        """
        1.生产任务id
        2.触发任务
        3.返回任务id
        :return:
        """

        task_obj = models.Task.objects.create(
            user=self.request.user,
            task_type=self.task_data["task_type"],
            content=self.task_data["cmd"],
        )

        sub_task_objs = []

        for host_id in self.task_data["selected_host_ids"]:
            sub_task_objs.append(
                models.TaskLogDetail(
                    task=task_obj, bind_host_id=host_id, result="init...", status=2
                )
            )

        models.TaskLogDetail.objects.bulk_create(sub_task_objs)

        task_script_obj = subprocess.Popen(
            "python %s %s" % (conf.settings.MULTITASK_SCRIPT, task_obj.id),
            shell=True,
            stdout=subprocess.PIPE,
        )

        self.task = task_obj

    def file_transfer_task(self):
        """
         1.生产任务记录
         2.触发任务
         3. 返回任务id
        :return:
        """

        task_obj = models.Task.objects.create(
            user=self.request.user,
            task_type=self.task_data["task_type"],
            content=json.dumps(self.task_data),
        )

        sub_task_objs = []

        for host_id in self.task_data["selected_host_ids"]:
            sub_task_objs.append(
                models.TaskLogDetail(
                    task=task_obj, bind_host_id=host_id, result="init...", status=2
                )
            )

        models.TaskLogDetail.objects.bulk_create(sub_task_objs)

        task_script_obj = subprocess.Popen(
            "python3 %s %s" % (conf.settings.MULTITASK_SCRIPT, task_obj.id),
            shell=True,
            stdout=subprocess.PIPE,
        )

        self.task = task_obj
