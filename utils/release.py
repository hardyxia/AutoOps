#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/24 11:59
# @Author  : hardyxia
# @File    : release.py
"""
调用jenkinsapi 获取job信息
"""

from jenkinsapi.jenkins import Jenkins
from jenkinsapi.build import Build
from AutoOps import settings


class JenkinsApi(object):
    def __init__(self):
        self.url = settings.JENKINS_CONFIG['url']
        self.username = settings.JENKINS_CONFIG['username']
        self.password = settings.JENKINS_CONFIG['password']

    def get_server_instance(self):
        server = Jenkins(baseurl=self.url,
                         username=self.username,
                         password=self.password)
        return server

    def get_job_details(self):
        server = self.get_server_instance()
        job_list = []
        for job_name, job_instance in server.get_jobs():
            job_info = {
                "job_name": job_name,
                "job_parms": None,
                "job_description": job_instance.get_description(),
                "job_is_running": job_instance.is_running(),
                "job_is_enabled": job_instance.is_enabled()}
            job_list.append(job_info)
        return {"job_list": job_list,
                "job_count": len(job_list), }

    def check_has_job(self, job_name):
        return self.get_server_instance().has_job(job_name)

    def get_job_config(self, job_name):
        if not self.check_has_job(job_name):
            return "%s is not exits!" % job_name
        else:
            return self.get_server_instance()[job_name].get_config(), \
                   self.get_server_instance()[job_name].get_config_xml_url()

    def job_delete(self,job_name):
        if not self.check_has_job(job_name):
            return "%s is not exits!" % job_name
        else:
            return self.get_server_instance().delete_job(job_name)

    def build_job(self, job_name, params=None):
        if not self.check_has_job(job_name):
            return "%s is not exits!" % job_name
        else:
            server = self.get_server_instance()
            ret = server.build_job(job_name, params)
            print(ret)
            '''
            # return self.get_server_instance().build_job(job_name,params)
            job = self.get_server_instance()[job_name]
            run_job = job.invoke(build_params=params)
            number = run_job.__dict__['_data']['executable']['number']
            build_url = run_job.__dict__['_data']['executable']['url']
            # url = job.__dict__['_data']['lastBuild']['url']
            # number = job.__dict__['_data']['lastBuild']['number']
            obj = Build(build_url, number, job)
            print("第%d次构建: %s" % (number, build_url))
            # print(obj.get_console().encode('utf-8'))
            is_running = obj.is_running()
            is_stop = obj.stop()
            is_good = obj.is_good()
            status = obj.get_status()

            return {"this_num": number,
                    "build_url": build_url,
                    "is_running": is_running,
                    "is_stop": is_stop,
                    "is_good": is_good,
                    "status": status
                    }
            '''
    def get_job_history(self, job_name):
        job = self.get_server_instance()[job_name]
        current_job_list = []
        for k, v in job.get_build_dict().items():
            current_job_list.append({k: v})
        return current_job_list

# JenkinsApi().build_job("test")
# print(JenkinsApi().build_job("XieKeYun_cloudCenter", params={"branch": "origin/board_optim"}))
