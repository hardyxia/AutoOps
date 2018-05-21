from django.db import models

from django.db import models
from DjangoUeditor.models import UEditorField
from django.contrib.auth.models import User


class IDC(models.Model):
    """机房信息"""
    name = models.CharField('机房', max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ops_idc'
        verbose_name_plural = "机房表"


class Region(models.Model):
    """可用区表"""
    id = models.CharField(verbose_name='区域编码', max_length=64, primary_key=True)
    name = models.CharField(verbose_name='区域名称', max_length=64, blank=True, null=True)
    endpoint = models.URLField(verbose_name='API地址', null=True, blank=True)
    idc = models.ForeignKey('IDC', verbose_name='机房', to_field='id', default=1, on_delete=models.CASCADE)

    # zone = models.CharField(verbose_name='可用区', max_length=64, blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.idc, self.name,)

    class Meta:
        db_table = 'ops_ali_vpc_region'
        verbose_name_plural = '可用区表'


class VPC(models.Model):
    """VPC表"""
    id = models.CharField(verbose_name='VPC ID', max_length=64, primary_key=True)
    name = models.CharField(verbose_name='VPC名称', max_length=64, blank=True, null=True)
    is_default = models.BooleanField(verbose_name='默认VPC', default=False)
    status_choices = (
        ('Available', '在线'),
        ('unAvailable', '离线'),
    )
    status = models.CharField(verbose_name='状态', choices=status_choices, max_length=16, default='Available')
    # color = models.CharField(max_length=8, blank=True, null=True)
    # cidr_block = models.GenericIPAddressField(verbose_name='网段', max_length=64)
    cidr_block = models.CharField(verbose_name='网段', max_length=64)
    region = models.ForeignKey('Region', verbose_name='区域', to_field='id')
    creation_time = models.CharField(verbose_name='创建时间', max_length=64, blank=True, null=True)
    # description = models.TextField(verbose_name='备注', blank=True, null=True)
    description = UEditorField(verbose_name='内容', height=200, width=700,
                               default=u'', blank=True, imagePath="uploads/images/",
                               toolbars='besttome', filePath='uploads/files/')

    def color_status(self):
        if self.status == 'Available':
            color = 'red'
        else:
            color = 'green'
        return '<span style="color: %s ">%s</span>' % (color, self.get_status_display())

    color_status.allow_tags = True
    color_status.short_description = '状态'

    def __str__(self):
        return '%s【%s】' % (self.id, self.name)

    class Meta:
        db_table = 'ops_ali_vpc'
        verbose_name_plural = 'VPC表'


class Router(models.Model):
    """虚拟路由器表"""
    id = models.CharField(verbose_name='路由器ID', max_length=32, primary_key=True)
    name = models.CharField(verbose_name='路由器名称', max_length=64, null=True, blank=True)
    creation_time = models.CharField(verbose_name='创建时间', max_length=64, blank=True, null=True)
    vpc = models.ForeignKey('VPC', verbose_name='所属VPC', to_field='id')
    region = models.ForeignKey('Region', verbose_name='区域', to_field='id')
    route_table_id = models.CharField(verbose_name='路由表ID', max_length=128, null=True, blank=True)
    description = models.TextField(verbose_name='备注', blank=True, null=True)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'ops_ali_vpc_router'
        verbose_name_plural = '路由器表'


class Switch(models.Model):
    """交换机表"""
    id = models.CharField(verbose_name='交换机ID', max_length=128, primary_key=True)
    name = models.CharField(verbose_name='交换机名称', max_length=64, null=True, blank=True)
    creation_time = models.CharField(verbose_name='创建时间', max_length=64, blank=True, null=True)
    vpc = models.ForeignKey('VPC', verbose_name='所属VPC', to_field='id')
    is_default = models.BooleanField(verbose_name='是否默认', default=False)
    status_choices = (
        ('Available', '在线'),
        ('unAvailable', '离线'),
    )
    status = models.CharField(verbose_name='状态', choices=status_choices, max_length=16, default='Available')
    cidr_block = models.GenericIPAddressField(verbose_name='网段', max_length=64)
    available_ip_address_count = models.IntegerField(verbose_name='可以IP数')
    # region = models.ForeignKey('Region', verbose_name='区域', to_field='id')
    zone = models.CharField(verbose_name='可用区', max_length=64, blank=True, null=True)
    description = models.TextField(verbose_name='备注', blank=True, null=True)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'ops_ali_vpc_switch'
        verbose_name_plural = '交换机表'


class RouterTable(models.Model):
    """路由信息表"""
    id = models.CharField(verbose_name='路由表ID', max_length=128, primary_key=True)
    name = models.CharField(verbose_name='路由表名称', max_length=64, blank=True, null=True)

    route_table_type_choices = (
        ("System", '系统'), ("Custom", '正常'),
    )
    route_table_type = models.CharField(verbose_name='路由表类型', choices=route_table_type_choices, max_length=16,
                                        default='System')
    creation_time = models.CharField(verbose_name='创建时间', max_length=64, blank=True, null=True)

    vpc = models.ForeignKey('VPC', verbose_name='所属VPC')
    router = models.ForeignKey('Router', verbose_name='路由器')
    route_type_choices = (
        ("VRouter", '虚拟路由'), ("Router", '物理路由'),
    )
    route_type = models.CharField(verbose_name='路由类型', choices=route_type_choices, max_length=16, default='VRouter')
    description = models.TextField(verbose_name='备注', blank=True, null=True)

    # creation_time = models.CharField(verbose_name='创建时间', max_length=64, blank=True, null=True)
    # destination_cidr_block = models.GenericIPAddressField(verbose_name='网段')
    # instance_id = models.CharField(verbose_name='实例ID', max_length=32)
    # status_choices = (
    #     ('Available', '在线'),
    #     ('unAvailable', '离线'),
    # )
    # status = models.CharField(verbose_name='状态', choices=status_choices, max_length=16, default='Available')

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'ops_ali_vpc_router_table'
        verbose_name_plural = '路由信息表'


class EipAddress(models.Model):
    """EIP"""
    id = models.CharField(verbose_name='实例ID', max_length=64, primary_key=True)
    name = models.CharField(verbose_name='实例名称', max_length=64, null=True, blank=True)
    charge_type = models.CharField(verbose_name='计费类型', max_length=64, null=True, blank=True)
    allocation_time = models.CharField(verbose_name='分配时间', max_length=64, null=True, blank=True)
    ip_address = models.GenericIPAddressField(verbose_name='IP地址', )
    allocation_id = models.CharField(verbose_name='分配ID', max_length=64, null=True, blank=True)
    internet_charge_type = models.CharField(verbose_name='收费类型', max_length=64, null=True, blank=True)
    status_choices = (('InUse', '在使用'), ('OutUse', '未使用'),)
    status = models.CharField(verbose_name='状态', choices=status_choices, max_length=16, default='Available')
    region = models.ForeignKey('Region', verbose_name='区域', to_field='id')
    bandwidth = models.IntegerField(verbose_name='带宽(M)')
    operation_locks = models.CharField(verbose_name='操作锁定', max_length=64, null=True, blank=True)
    bandwidth_package_id = models.CharField(verbose_name='宽带包ID', max_length=64, null=True, blank=True)
    expired_time = models.CharField(verbose_name='过期时间', max_length=64, null=True, blank=True)
    instance_type = models.CharField(verbose_name='实例类型', max_length=64, null=True, blank=True)
    description = models.TextField(verbose_name='备注', blank=True, null=True)

    def __str__(self):
        return self.ip_address

    class Meta:
        db_table = 'ops_ali_vpc_eip_address'
        verbose_name_plural = '弹性IP表'


class NatGateway(models.Model):
    """NAT网关列表"""
    id = models.CharField(verbose_name='NAT网关ID', max_length=64, primary_key=True)
    name = models.CharField(verbose_name='NAT网关名称', max_length=32, blank=True, null=True)
    spec = models.CharField(verbose_name='规格', max_length=32, blank=True, null=True)
    forward_table_ids = models.CharField(verbose_name='转发表ID', max_length=256, blank=True, null=True)
    creation_time = models.CharField(verbose_name='创建时间', max_length=64, blank=True, null=True)
    vpc = models.ForeignKey('VPC', verbose_name='所属VPC', to_field='id')
    region = models.ForeignKey('Region', verbose_name='区域', to_field='id')
    bandwidth_package_ids = models.CharField(verbose_name='宽带包ID', max_length=256, blank=True, null=True)
    snat_table_ids = models.CharField(verbose_name='SNAT表ID', max_length=256, blank=True, null=True)
    status_choices = (
        ('Available', '在线'),
        ('unAvailable', '离线'),
    )

    status = models.CharField(verbose_name='状态', choices=status_choices, max_length=16, default='Available')
    business_status = models.CharField(verbose_name='业务状态', max_length=16, default='Normal')
    internet_charge_type = models.CharField(verbose_name='收费类型', max_length=64, null=True, blank=True)
    instance_charge_type = models.CharField(verbose_name='实例费用类型', max_length=64, null=True, blank=True)
    description = models.TextField(verbose_name='备注', blank=True, null=True)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'ops_ali_vpc_nat_gateway'
        verbose_name_plural = 'NAT网关表'


class BandwidthPackage(models.Model):
    """NAT宽带包列表"""
    id = models.CharField(verbose_name='宽带包ID', max_length=64, primary_key=True)
    name = models.CharField(verbose_name='宽带包名称', max_length=64, null=True, blank=True)
    bandwidth = models.IntegerField(verbose_name='带宽(M)')
    business_status = models.CharField(verbose_name='业务状态', max_length=16, default='Normal')
    creation_time = models.CharField(verbose_name='创建时间', max_length=64, blank=True, null=True)

    instance_charge_type = models.CharField(verbose_name='实例费用类型', max_length=64, null=True, blank=True)
    internet_charge_type = models.CharField(verbose_name='收费类型', max_length=64, null=True, blank=True)
    ip_count = models.IntegerField(verbose_name='IP数量')
    isp = models.CharField(verbose_name='网络类型', max_length=64, null=True, blank=True)
    nat_gateway = models.ForeignKey('NatGateway', verbose_name='网关ID')
    public_ip_addresses = models.CharField(verbose_name='公网IP', max_length=256, null=True, blank=True)
    region = models.ForeignKey('Region', verbose_name='区域', to_field='id')  # 大区
    status_choices = (
        ('Available', '在线'),
        ('unAvailable', '离线'),
    )
    status = models.CharField(verbose_name='状态', choices=status_choices, max_length=16, default='Available')
    # zone = models.ForeignKey('Region', verbose_name='可用区', to_field='zone')  # 小区
    zone = models.CharField(verbose_name='可用区', max_length=32, null=True, blank=True)  # 小区
    allocation_id = models.CharField(verbose_name='分配ID', max_length=32, null=True, blank=True)
    # ip_address = models.GenericIPAddressField(verbose_name='IP地址')
    description = models.TextField(verbose_name='备注', blank=True, null=True)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'ops_ali_vpc_bandwidth_package'
        verbose_name_plural = 'NAT宽带包列表'


class InstanceStatus(models.Model):
    name = models.CharField(verbose_name='实例状态', max_length=16)
    description = models.TextField(verbose_name='状态说明', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ops_ali_ecs_instance_status'
        verbose_name_plural = 'ECS实例状态'


class InstanceInfo(models.Model):
    '''ECS实例信息 '''
    id = models.CharField(verbose_name='实例ID', max_length=64, primary_key=True)
    name = models.CharField(verbose_name='实例名称', max_length=64, null=True, blank=True)
    cpu = models.SmallIntegerField(verbose_name='CPU数量')
    key_pair_name = models.CharField(verbose_name='密钥', max_length=64, null=True, blank=True)
    os_type = models.CharField(verbose_name='系统类型', max_length=64, null=True, blank=True)
    os_name = models.CharField(verbose_name='系统名称', max_length=64, null=True, blank=True)
    memory = models.IntegerField(verbose_name='总内存')
    hostname = models.CharField(verbose_name='主机名', max_length=64, null=True, blank=True)
    primary_ip_address = models.GenericIPAddressField(verbose_name='主IP地址')
    mac_address = models.CharField(verbose_name='MAC地址', max_length=64, null=True, blank=True)
    network_interface_id = models.CharField(verbose_name='网关ID', max_length=64, null=True, blank=True)
    # region_id = models.CharField(verbose_name='区域', max_length=64, null=True, blank=True)
    region = models.ForeignKey('Region', verbose_name='区域', )
    zone_id = models.CharField(verbose_name='可用区', max_length=64, null=True, blank=True)
    io_optimized = models.BooleanField(verbose_name='IO优化', default=False)
    serial_number = models.CharField(verbose_name='序列号', max_length=64, null=True, blank=True)
    internet_max_bandwidth_in = models.SmallIntegerField(verbose_name='最大入流量')
    internet_max_bandwidth_out = models.SmallIntegerField(verbose_name='最大出流量')
    gpu_amount = models.SmallIntegerField(verbose_name='GPU数量', )
    gpu_spec = models.CharField(verbose_name='GPU规格', max_length=64, null=True, blank=True)
    public_ip_address = models.CharField(verbose_name='公网IP', max_length=64, null=True, blank=True)
    status = models.CharField(verbose_name='状态', max_length=64, null=True, blank=True)
    recyclable = models.BooleanField(verbose_name='可回收', default=False)
    security_group_ids = models.CharField(verbose_name='安全组ID', max_length=128, null=True, blank=True)
    eip_address = models.GenericIPAddressField(verbose_name='弹性IP地址', null=True, blank=True)
    creation_time = models.CharField(verbose_name='创建时间', max_length=128, null=True, blank=True)
    expired_time = models.CharField(verbose_name='到期时间', max_length=128, null=True, blank=True)
    instance_network_type = models.CharField(verbose_name='实例网络类型', max_length=128, null=True, blank=True)
    device_available = models.CharField(verbose_name='设备可用性', max_length=128, null=True, blank=True)
    v_switch_id = models.CharField(verbose_name='交换机', max_length=128, null=True, blank=True)
    private_ip_address = models.GenericIPAddressField(verbose_name='私有IP地址', null=True, blank=True)
    port = models.IntegerField(verbose_name='SSH端口', default=22)
    vpc = models.ForeignKey('VPC', verbose_name='所在VPC')
    idc = models.ForeignKey('IDC', verbose_name='服务商', default=1)
    instance_charge_type = models.CharField(verbose_name='付款类型', max_length=64, null=True, blank=True)
    image_id = models.CharField(verbose_name='镜像ID', max_length=64, null=True, blank=True)
    instance_type = models.CharField(verbose_name='实例类型', max_length=64, null=True, blank=True)
    description = models.TextField(verbose_name='备注', null=True, blank=True)
    bind_user = models.ForeignKey(to="BindUser", to_field='id', on_delete=models.SET_NULL, null=True,
                                  verbose_name='登陆用户', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ops_ali_ecs_instance_info'
        verbose_name_plural = 'ECS实例信息'


class BindUser(models.Model):
    '''绑定的用户'''
    username = models.CharField(validators='用户名', max_length=32)
    password = models.CharField(validators='密码', max_length=128, blank=True, null=True)
    ssh_type_choices = ((0, 'SSH/Password'), (1, 'SSH/Key'))
    ssh_type = models.SmallIntegerField(choices=ssh_type_choices, verbose_name='ssh类型', default=0)

    # instance = models.ManyToManyField('InstanceInfo')
    comment = models.TextField(verbose_name='备注', blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'ops_ali_ecs_bind_user'
        verbose_name_plural = '绑定的用户'


class ServiceUrl(models.Model):
    """
    服务名对应URL表
    """
    name = models.CharField(max_length=64, verbose_name='服务名称')
    web_url = models.URLField(max_length=128, verbose_name='Web URL地址', null=True, blank=True)
    real_url = models.CharField(max_length=128, verbose_name='后端URL', null=True, blank=True)
    connection_choice = (
        (1, 'HTTP'),
        (2, 'TCP'))
    connection = models.SmallIntegerField(choices=connection_choice, verbose_name='协议', default=1)

    auth_choice = (
        (1, '是'),
        (0, '否')
    )
    auth = models.SmallIntegerField(choices=auth_choice, verbose_name='是否认证', default=1)
    user = models.CharField(verbose_name='用户名', max_length=32, null=True, blank=True)
    password = models.CharField(verbose_name='密码', max_length=64, null=True, blank=True)

    class Meta:
        db_table = 'ops_config_service_url'
        verbose_name_plural = '服务URL关系'

    def __str__(self):
        return self.name

    def url_link(self):

        return '<a href="%s">%s</a>' % (self.web_url, self.web_url)

    url_link.allow_tags = True
    url_link.short_description = 'URL'

    def color_connection(self):
        if self.connection == 1:
            color = 'red'
        else:
            color = 'green'
        return '<span style="color: %s ">%s</span>' % (color, self.get_connection_display())

    color_connection.allow_tags = True
    color_connection.short_description = '协议类型'


class WebHistory(models.Model):
    user = models.CharField(max_length=32, verbose_name='登录用户', null=True)
    ip = models.GenericIPAddressField(verbose_name='用户地址', null=True)
    login_user = models.CharField(max_length=32, verbose_name='所用账号', null=True)
    host = models.CharField(max_length=32, verbose_name='登录主机', null=True)
    ctime = models.DateTimeField(auto_now_add=True, verbose_name='时间')

    class Meta:
        db_table = "ops_config_web_history"
        verbose_name_plural = '历史登录'


class BindHost(models.Model):
    """绑定远程主机和远程用户的对应关系"""
    host = models.ForeignKey("InstanceInfo")
    remote_user = models.ForeignKey("BindUser")

    def __str__(self):
        return "%s -> %s" % (self.host, self.remote_user)

    class Meta:
        unique_together = ("host", "remote_user")
        db_table = "ops_config_bind_host"
        verbose_name_plural = '主机与用户绑定关系'


class Task(models.Model):
    """批量任务记录表"""
    user = models.ForeignKey(User)
    task_type_choices = ((0, 'cmd'), (1, 'file_transfer'))
    task_type = models.SmallIntegerField(choices=task_type_choices)
    content = models.TextField(verbose_name="任务内容")
    # hosts = models.ManyToManyField("BindHost")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.task_type, self.content)

    class Meta:
        db_table = "ops_config_task"
        verbose_name_plural = '任务记录'


class TaskLogDetail(models.Model):
    task = models.ForeignKey("Task")
    bind_host = models.ForeignKey("BindHost")
    result = models.TextField()
    status_choices = ((0, 'success'), (1, 'failed'), (2, 'init'))
    status = models.SmallIntegerField(choices=status_choices)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.bind_host, self.status)

    class Meta:
        db_table = "ops_config_task_log"
        verbose_name_plural = '任务日志'
