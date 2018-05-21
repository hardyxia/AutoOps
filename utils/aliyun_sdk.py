#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 16:15
# @Author  : hardyxia
# @File    : aliyun_sdk.py
import json
from django.conf import settings
from aliyunsdkcore.client import AcsClient


# from AliyunService.aliyun_config import AccessKeyId, AccessKeySecret, RegionId, PageSize


class AliyunAPI(object):
    """
    通过阿里云SDK获取API返回数据
    """

    def __init__(self, access_key_id=settings.AccessKeyId,
                 access_key_secret=settings.AccessKeySecret,
                 region_id='cn-shenzhen'):
        """
        实例化 传入AccessKeyId ，AccessKeySecret，RegionId
        :param access_key_id:
        :param access_key_secret:
        :param region_id:
        """
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.region_id = region_id
        self.client = AcsClient(self.access_key_id, self.access_key_secret, self.region_id)

    def aliyun_region_result(self, action_model):
        """获取阿里云API返回值，返回字典"""
        request = action_model()
        # 获取 region 没有分页字段
        response = self.client.do_action_with_exception(request)
        result = json.loads(response.decode())
        return result

    def aliyun_result(self, action_model):
        """获取阿里云API返回值，返回字典"""
        request = action_model()
        request.set_PageSize(settings.PageSize)
        response = self.client.do_action_with_exception(request)
        result = json.loads(response.decode())
        return result


    # 下面2个方法是操作ELB后端
    def aliyun_elb_add_backend(self, LoadBalancerId, BackendServers):
        """
        添加backend server 到elb
        :param LoadBalancerId:  负载均衡器的ID
        :param BackendServers:  后端server ，list格式里面是json
        :return:
        """
        from aliyunsdkslb.request.v20140515 import AddBackendServersRequest
        res = AddBackendServersRequest.AddBackendServersRequest()
        res.set_accept_format('json')
        res.set_LoadBalancerId(LoadBalancerId=LoadBalancerId)
        res.set_BackendServers(BackendServers)
        response = self.client.do_action_with_exception(res)
        return response

    def aliyun_elb_remove_backend(self, LoadBalancerId, BackendServers):
        """
        从elb里面删除后端server
        :param LoadBalancerId:  负载均衡器的ID
        :param BackendServers:  后端server ，list格式里面是json
        :return:
        """
        from aliyunsdkslb.request.v20140515 import RemoveBackendServersRequest
        res = RemoveBackendServersRequest.RemoveBackendServersRequest()
        res.set_accept_format('json')
        res.set_LoadBalancerId(LoadBalancerId=LoadBalancerId)
        res.set_BackendServers(BackendServers)
        response = self.client.do_action_with_exception(res)
        return response

    def aliyun_elb_set_backend(self, LoadBalancerId, BackendServers):
        """
        设置ELB权重,权限为0对于之前的长连接依旧保持，新连接不在转发到该server
        :param LoadBalancerId:  负载均衡器的ID
        :param BackendServers:  后端server ，list格式里面是json
        :return:
        """
        from aliyunsdkslb.request.v20140515 import SetBackendServersRequest
        res = SetBackendServersRequest.SetBackendServersRequest()
        res.set_accept_format('json')
        res.set_LoadBalancerId(LoadBalancerId=LoadBalancerId)
        res.set_BackendServers(BackendServers)
        response = self.client.do_action_with_exception(res)
        return response
