#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/4 17:17
# @Author  : hardyxia
# @File    : task_runner.py

import sys, os
import time, json
from concurrent.futures import ThreadPoolExecutor
from encryption import decrypt_p

import paramiko


def ssh_cmd(task_log_obj):
    host = task_log_obj.bind_host.host
    user_obj = task_log_obj.bind_host.remote_user

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host.eip_address,
                    host.port,
                    user_obj.username,
                    decrypt_p(user_obj.password),
                    timeout=10, )

        stdin, stdout, stderr = ssh.exec_command(task_log_obj.task.content)

        stdout_res = stdout.read()
        stderr_res = stderr.read()

        result = stdout_res + stderr_res
        print(result)
        task_log_obj.result = result

        task_log_obj.status = 0
        ssh.close()

    except Exception as e:
        task_log_obj.result = e
        task_log_obj.status = 1

    task_log_obj.save()


def file_transfer(task_log_obj):
    host = task_log_obj.bind_host.host
    user_obj = task_log_obj.bind_host.remote_user
    try:
        t = paramiko.Transport((host.eip_address, host.port))
        t.connect(username=user_obj.username, password=decrypt_p(user_obj.password))
        sftp = paramiko.SFTPClient.from_transport(t)
        task_data = json.loads(task_log_obj.task.content)

        if task_data["file_transfer_type"] == "send":
            sftp.put(task_data["local_file_path"], task_data["remote_file_path"])
            task_log_obj.result = "send local file [%s] to remote [%s] succeeded!" % (task_data["local_file_path"],
                                                                                      task_data["remote_file_path"],)

        else:  # get
            local_file_path = "%s/%s" % (django.conf.settings.DOWNLOAD_DIR,
                                         task_log_obj.task.id,)
            if not os.path.isdir(local_file_path):
                os.mkdir(local_file_path)
            file_name = task_data["remote_file_path"].split("/")[-1]
            sftp.get(task_data["remote_file_path"], "%s/%s.%s" % (local_file_path, host.eip_address, file_name), )
            task_log_obj.result = "get remote file [%s] succeeded" % (task_data["remote_file_path"])

        t.close()
        task_log_obj.status = 0

    except Exception as e:
        task_log_obj.result = e
        task_log_obj.status = 1
    task_log_obj.save()


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(base_dir)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutoOps.settings")
    import django

    django.setup()
    from django import conf

    from cmdb import models

    if len(sys.argv) == 1:
        exit("error:must provide task_id!")
    task_id = sys.argv[1]

    task_obj = models.Task.objects.get(id=task_id)

    # 1. 生产多线程
    pool = ThreadPoolExecutor(10)

    if task_obj.task_type == 0:  # cmd
        thread_func = ssh_cmd
    else:  # file_transfer
        thread_func = file_transfer

    for task_log_detail_obj in task_obj.tasklogdetail_set.all():
        pool.submit(thread_func, task_log_detail_obj)

        # ssh_cmd(task_log_detail_obj)

    pool.shutdown(wait=True)
