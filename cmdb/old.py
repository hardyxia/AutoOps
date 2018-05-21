#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 16:13
# @Author  : hardyxia
# @File    : old.py
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from utils.aliyun_sdk import AliyunAPI
from cmdb import models
import json


def region(request):
    """
    获取所有可用区数据
    :param request:
    :return:
    """
    from aliyunsdkvpc.request.v20160428 import DescribeRegionsRequest
    res = {"success": True, "errorCode": None, "errorMsg": None, "data": None}
    if request.method == "GET":
        obj = AliyunAPI()
        result = obj.aliyun_region_result(DescribeRegionsRequest.DescribeRegionsRequest)['Regions']
        for region_info in result.values():
            for row in region_info:
                region_name = row['LocalName']
                region_id = row['RegionId']
                models.Region.objects.update_or_create(id=region_id, name=region_name)
    res['data'] = '可用区数据更新成功'
    return HttpResponse(json.dumps(res, ensure_ascii=False),content_type="application/json")


def vpc(request):
    """
    通过阿里云接口返回VPC信息，更新到数据库
    :param request:
    :return:
    """
    from aliyunsdkvpc.request.v20160428 import DescribeVpcsRequest
    res = {"success": True, "errorCode": None, "errorMsg": None, "data": None}

    obj = AliyunAPI()
    result = obj.aliyun_result(DescribeVpcsRequest.DescribeVpcsRequest)['Vpcs']
    for vpc_info in result.values():
        for row in vpc_info:
            vpc_id = row['VpcId']
            name = row['VpcName']
            description = row['Description']
            is_default = row['IsDefault']
            status = row["Status"]
            cidr_block = row['CidrBlock']
            region_id = row['RegionId']
            creation_time = row['CreationTime']

            models.VPC.objects.update_or_create(id=vpc_id, name=name, description=description, status=status,
                                                cidr_block=cidr_block, region_id=region_id, is_default=is_default,
                                                creation_time=creation_time)

        res['data'] = 'VPC数据更新成功'
        return HttpResponse(json.dumps(res, ensure_ascii=False),content_type="application/json")


def router(request):
    """
    通过阿里云接口返回VPC内路由器，更新到数据库
    :param request:
    :return:
    """
    from aliyunsdkvpc.request.v20160428 import DescribeVRoutersRequest
    res = {"success": True, "errorCode": None, "errorMsg": None, "data": None}
    obj = AliyunAPI()
    result = obj.aliyun_result(DescribeVRoutersRequest.DescribeVRoutersRequest)['VRouters']

    for vpc_info in result.values():
        for row in vpc_info:
            router_id = row['VRouterId']
            name = row['VRouterName']
            creation_time = row['CreationTime']
            description = row['Description']
            vpc_id = row['VpcId']
            region_id = row['RegionId']
            # route_table_id= row['RouteTableIds']['RouteTableId']
            models.Router.objects.update_or_create(id=router_id, name=name, creation_time=creation_time,
                                                   description=description, vpc_id=vpc_id, region_id=region_id)

    res['data'] = '路由器数据更新成功'
    return HttpResponse(json.dumps(res, ensure_ascii=False),content_type="application/json")


def switch(request):
    """
    通过阿里云接口返回VPC内交换机，更新到数据库
    :param request:
    :return:
    """
    from aliyunsdkvpc.request.v20160428 import DescribeVSwitchesRequest
    res = {"success": True, "errorCode": None, "errorMsg": None, "data": None}
    obj = AliyunAPI()
    result = obj.aliyun_result(DescribeVSwitchesRequest.DescribeVSwitchesRequest)['VSwitches']
    for vpc_info in result.values():
        for row in vpc_info:
            switch_id = row['VSwitchId']
            name = row['VSwitchName']
            creation_time = row['CreationTime']
            description = row['Description']
            vpc_id = row['VpcId']
            is_default = row['IsDefault']
            cidr_block = row['CidrBlock']
            available_ip_address_count = row['AvailableIpAddressCount']
            zone = row['ZoneId']
            status = row['Status']
            models.Switch.objects.update_or_create(id=switch_id, name=name, creation_time=creation_time,
                                                   description=description, zone=zone, status=status,
                                                   vpc_id=vpc_id, is_default=is_default, cidr_block=cidr_block,
                                                   available_ip_address_count=available_ip_address_count)

    res['data'] = '虚拟交换机数据更新成功'
    return HttpResponse(json.dumps(res, ensure_ascii=False),content_type="application/json")


def router_table(request):
    """
    通过阿里云接口返回VPC内路由表信息，更新到数据库
    :param request:
    :return:
    """
    from aliyunsdkvpc.request.v20160428 import DescribeRouteTableListRequest
    res = {"success": True, "errorCode": None, "errorMsg": None, "data": None}
    obj = AliyunAPI()
    result = obj.aliyun_result(DescribeRouteTableListRequest.DescribeRouteTableListRequest)['RouterTableList']
    for vpc_info in result.values():
        for row in vpc_info:
            description = row['Description']
            table_id = row['RouteTableId']
            name = row['RouteTableName']
            route_table_type = row['RouteTableType']
            creation_time = row['CreationTime']
            vpc_id = row['VpcId']
            router_id = row['RouterId']
            route_type = row['RouterType']

            models.RouterTable.objects.update_or_create(id=table_id, name=name, creation_time=creation_time,
                                                        description=description, route_table_type=route_table_type,
                                                        router_id=router_id,
                                                        vpc_id=vpc_id, route_type=route_type)

    res['data'] = '路由表数据更新成功'
    return HttpResponse(json.dumps(res, ensure_ascii=False),content_type="application/json")


def eip(request):
    """
    获取EIP信息
    :param request:
    :return:
    """
    from aliyunsdkvpc.request.v20160428 import DescribeEipAddressesRequest
    res = {"success": True, "errorCode": None, "errorMsg": None, "data": None}
    obj = AliyunAPI()
    result = obj.aliyun_result(DescribeEipAddressesRequest.DescribeEipAddressesRequest)['EipAddresses']

    for vpc_info in result.values():
        for row in vpc_info:
            internet_charge_type = row['InternetChargeType']
            bandwidth = row['Bandwidth']
            charge_type = row['ChargeType']
            region_id = row['RegionId']
            status = row['Status']
            description = row['Descritpion']
            operation_locks = row['OperationLocks']  # 返回一个字典
            name = row['Name']
            ip_address = row['IpAddress']
            bandwidth_package_id = row['BandwidthPackageId']
            instance_id = row['InstanceId']
            allocation_time = row['AllocationTime']
            expired_time = row['ExpiredTime']
            allocation_id = row['AllocationId']
            instance_type = row['InstanceType']

            models.EipAddress.objects.update_or_create(id=instance_id, name=name, operation_locks=operation_locks,
                                                       internet_charge_type=internet_charge_type, region_id=region_id,
                                                       bandwidth=bandwidth, charge_type=charge_type, status=status,
                                                       description=description, ip_address=ip_address,
                                                       bandwidth_package_id=bandwidth_package_id,
                                                       allocation_id=allocation_id, instance_type=instance_type,
                                                       allocation_time=allocation_time, expired_time=expired_time)

    res['data'] = '弹性IP数据更新成功'
    return HttpResponse(json.dumps(res, ensure_ascii=False),content_type="application/json")


def nat_gateway(request):
    """
    通过阿里云接口返回NAT网关信息
    :param request:
    :return:
    """
    from aliyunsdkvpc.request.v20160428 import DescribeNatGatewaysRequest
    res = {"success": True, "errorCode": None, "errorMsg": None, "data": None}
    obj = AliyunAPI()
    result = obj.aliyun_result(DescribeNatGatewaysRequest.DescribeNatGatewaysRequest)['NatGateways']
    for vpc_info in result.values():
        for row in vpc_info:
            nat_gateway_id = row['NatGatewayId']
            bandwidth_package_ids = row['BandwidthPackageIds']  # 列表
            description = row['Description']
            creation_time = row['CreationTime']
            spec = row['Spec']
            business_status = row['BusinessStatus']
            snat_table_ids = row['SnatTableIds']  # 列表
            instance_charge_type = row['InstanceChargeType']
            forward_table_ids = row['ForwardTableIds']
            status = row['Status']
            vpc_id = row['VpcId']
            region_id = row['RegionId']
            name = row['Name']

            models.NatGateway.objects.update_or_create(id=nat_gateway_id, name=name, status=status, spec=spec,
                                                       bandwidth_package_ids=bandwidth_package_ids, vpc_id=vpc_id,
                                                       creation_time=creation_time, forward_table_ids=forward_table_ids,
                                                       business_status=business_status, snat_table_ids=snat_table_ids,
                                                       description=description, region_id=region_id,
                                                       instance_charge_type=instance_charge_type,
                                                       )

    res['data'] = 'NAT网关数据更新成功'
    return HttpResponse(json.dumps(res, ensure_ascii=False),content_type="application/json")


def bandwidth_package(request):
    """
     通过阿里云接口返回宽带包
     :param request:
     :return:
     """
    from aliyunsdkvpc.request.v20160428 import DescribeBandwidthPackagesRequest
    res = {"success": True, "errorCode": None, "errorMsg": None, "data": None}
    obj = AliyunAPI()
    result = obj.aliyun_result(DescribeBandwidthPackagesRequest.DescribeBandwidthPackagesRequest)[
        'BandwidthPackages']

    for vpc_info in result.values():
        for row in vpc_info:
            bandwidth_package_id = row['BandwidthPackageId']
            internet_charge_type = row['InternetChargeType']
            instance_charge_type = row['InstanceChargeType']
            business_status = row['BusinessStatus']
            description = row['Description']
            status = row['Status']
            region_id = row['RegionId']
            name = row['Name']
            isp = row['ISP']
            creation_time = row['CreationTime']
            public_ip_addresses = row['PublicIpAddresses']
            nat_gateway_id = row['NatGatewayId']
            bandwidth = row['Bandwidth']
            ip_count = row['IpCount']
            zone_id = row['ZoneId']

            models.BandwidthPackage.objects.update_or_create(id=bandwidth_package_id, name=name, isp=isp,
                                                             zone=zone_id, business_status=business_status,
                                                             internet_charge_type=internet_charge_type,
                                                             region_id=region_id, status=status,
                                                             instance_charge_type=instance_charge_type,
                                                             public_ip_addresses=public_ip_addresses, ip_count=ip_count,
                                                             creation_time=creation_time, nat_gateway_id=nat_gateway_id,
                                                             description=description, bandwidth=bandwidth, )

    res['data'] = '宽带包数据更新成功'
    return HttpResponse(json.dumps(res, ensure_ascii=False),content_type="application/json")


#####无用
def forward_table_entry(request):
    """
     通过阿里云接口返回DNAT
     :param request:
     :return:
     """
    res = {"success": True, "errorCode": None, "errorMsg": None, "data": None}
    res['data'] = '无数据'
    return HttpResponse(json.dumps(res, ensure_ascii=False),content_type="application/json")


# ECS实例部分
def ecs_instance(request):
    '''获取ECS信息'''
    from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
    res = {"success": True, "errorCode": None, "errorMsg": None, "data": None}
    obj = AliyunAPI()
    instance_list = []
    instances = models.InstanceInfo.objects.all().values('id')
    for i in instances:
        instance_list.append(i['id'])

    result = obj.aliyun_result(DescribeInstancesRequest.DescribeInstancesRequest)['Instances']
    for ecs_info in result.values():
        for row in ecs_info:

            instance_id = row['InstanceId']
            instance_name = row['InstanceName']
            cpu = row['Cpu']
            if 'KeyPairName' in row:
                key_pair_name = row['KeyPairName']
            else:
                key_pair_name = None
            os_type = row['OSType']
            os_name = row['OSName']
            memory = row['Memory']
            hostname = row['HostName']
            primary_ip_address = row['NetworkInterfaces']['NetworkInterface'][0]['PrimaryIpAddress']
            mac_address = row['NetworkInterfaces']['NetworkInterface'][0]['MacAddress']
            network_interface_id = row['NetworkInterfaces']['NetworkInterface'][0]['NetworkInterfaceId']
            region_id = row['RegionId']
            zone_id = row['ZoneId']
            instance_type = row['InstanceType']
            io_optimized = row['IoOptimized']
            serial_number = row['SerialNumber']
            description = row['Description']
            internet_max_bandwidth_in = row['InternetMaxBandwidthIn']
            internet_max_bandwidth_out = row['InternetMaxBandwidthOut']
            # spot_price_limit = row['SpotPriceLimit']
            gpu_amount = row['GPUAmount']
            gpu_spec = row['GPUSpec']
            public_ip_address = row['PublicIpAddress']
            status = row['Status']
            recyclable = row['Recyclable']
            security_group_ids = row['SecurityGroupIds']['SecurityGroupId']
            eip_address = row['EipAddress']['IpAddress']
            creation_time = row['CreationTime']
            expired_time = row['ExpiredTime']
            instance_network_type = row['InstanceNetworkType']
            device_available = row['DeviceAvailable']
            v_switch_id = row['VpcAttributes']['VSwitchId']
            private_ip_address = row['VpcAttributes']['PrivateIpAddress']['IpAddress']
            vpc_id = row['VpcAttributes']['VpcId']
            instance_charge_type = row['InstanceChargeType']
            image_id = row['ImageId']

            # 这里使用update_or_create 方法竟然报错，貌似每次都执行create 方法
            if instance_id in instance_list:
                models.InstanceInfo.objects.filter(id=instance_id).update(id=instance_id, name=instance_name, cpu=cpu,
                                                                          hostname=hostname, gpu_amount=gpu_amount,
                                                                          io_optimized=io_optimized, gpu_spec=gpu_spec,
                                                                          instance_type=instance_type, memory=memory,
                                                                          key_pair_name=key_pair_name, status=status,
                                                                          os_type=os_type, os_name=os_name,
                                                                          primary_ip_address=primary_ip_address,
                                                                          mac_address=mac_address, vpc_id=vpc_id,
                                                                          network_interface_id=network_interface_id,
                                                                          zone_id=zone_id, serial_number=serial_number,
                                                                          region_id=region_id, recyclable=recyclable,
                                                                          internet_max_bandwidth_in=internet_max_bandwidth_in,
                                                                          internet_max_bandwidth_out=internet_max_bandwidth_out,
                                                                          public_ip_address=public_ip_address,
                                                                          security_group_ids=security_group_ids,
                                                                          eip_address=eip_address,
                                                                          creation_time=creation_time,
                                                                          expired_time=expired_time,
                                                                          instance_network_type=instance_network_type,
                                                                          device_available=device_available,
                                                                          v_switch_id=v_switch_id, image_id=image_id,
                                                                          private_ip_address=private_ip_address,
                                                                          instance_charge_type=instance_charge_type,
                                                                          description=description)
            else:
                models.InstanceInfo.objects.update_or_create(id=instance_id, name=instance_name, cpu=cpu,
                                                             hostname=hostname, mac_address=mac_address,
                                                             io_optimized=io_optimized, instance_type=instance_type,
                                                             key_pair_name=key_pair_name,
                                                             os_type=os_type, os_name=os_name, memory=memory,
                                                             primary_ip_address=primary_ip_address,
                                                             network_interface_id=network_interface_id, zone_id=zone_id,
                                                             region_id=region_id, recyclable=recyclable,
                                                             gpu_spec=gpu_spec, eip_address=eip_address,
                                                             serial_number=serial_number, gpu_amount=gpu_amount,
                                                             internet_max_bandwidth_in=internet_max_bandwidth_in,
                                                             internet_max_bandwidth_out=internet_max_bandwidth_out,
                                                             public_ip_address=public_ip_address, status=status,
                                                             security_group_ids=security_group_ids,
                                                             creation_time=creation_time, expired_time=expired_time,
                                                             instance_network_type=instance_network_type, vpc_id=vpc_id,
                                                             device_available=device_available, v_switch_id=v_switch_id,
                                                             private_ip_address=private_ip_address, image_id=image_id,
                                                             instance_charge_type=instance_charge_type,
                                                             description=description)

    res['data'] = 'ECS数据更新成功'
    return HttpResponse(json.dumps(res, ensure_ascii=False),content_type="application/json")


# 负载均衡
def elb(request):
    '''查看ELB监控状态'''
    from aliyunsdkslb.request.v20140515 import DescribeHealthStatusRequest
    obj = AliyunAPI()
    LoadBalancerId = 'lb-wz9w9oue3lh0n5ie8wlu6'
    ListenerPort = 80
    res = DescribeHealthStatusRequest.DescribeHealthStatusRequest()
    res.set_ListenerPort(ListenerPort)
    res.set_LoadBalancerId(LoadBalancerId)
    response = obj.client.do_action_with_exception(res)
    result = response.decode()
    return HttpResponse(result)


def elb_action(request):
    '''
    对ELB后端elb提权、降权操作
    :param request:
    :return:
    '''
    obj = AliyunAPI()
    from AliyunService.aliyun_config import ELB_BACKENDS_INFO
    model_list = []
    for model in ELB_BACKENDS_INFO:
        model_list.append(model)
    if request.method == 'GET':
        model_name = request.GET.get('model_name')
        action = request.GET.get('action')
        server_id = request.GET.get('server_id')
        if model_name in model_list:
            current_elb_id_list = ELB_BACKENDS_INFO[model_name]["LoadBalancerIds"]
            current_elb_server_list = []
            for i in ELB_BACKENDS_INFO[model_name]["BackendServers"]:
                current_elb_server_list.append(i['ServerId'])

            if server_id in current_elb_server_list:
                if action == 'up':
                    '''上线操作'''
                    for elb_id in current_elb_id_list:
                        obj.aliyun_elb_set_backend(LoadBalancerId=elb_id,
                                                   BackendServers=[{"ServerId": server_id, "Weight": "100"}])
                    return HttpResponse('服务器上线成功')
                elif action == 'down':
                    '''下线操作'''
                    for elb_id in current_elb_id_list:
                        obj.aliyun_elb_set_backend(LoadBalancerId=elb_id,
                                                   BackendServers=[{"ServerId": server_id, "Weight": "0"}])

                    return HttpResponse(json.dumps({'error_msg': '服务器下线成功', }, ensure_ascii=False),
                                        content_type="application/json")
                else:
                    print('操作错误')

                    return HttpResponse(json.dumps({'error_msg': '不支持此类操作', }, ensure_ascii=False),
                                    content_type="application/json")

            else:
                print('服务器id未绑定该elb')
                return HttpResponse(json.dumps({'error_msg': '服务器ID与绑定的ELB不匹配', }, ensure_ascii=False),
                                    content_type="application/json")

        else:
            print('模块不存在')
            return HttpResponse('该服务模块未配置ELB')
            return HttpResponse(json.dumps({'error_msg': '请求方式不正确', }, ensure_ascii=False),
                            content_type="application/json")
    else:
        print('请求不正确')
        return HttpResponse(json.dumps({'error_msg': '请求方式不正确', }, ensure_ascii=False),
                            content_type="application/json")
