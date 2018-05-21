from django.db import models

from django.db import models
from DjangoUeditor.models import UEditorField
from django.contrib.auth.models import User

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


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

    def __str__(self):
        return '%s %s' % (self.idc, self.name,)

    class Meta:
        db_table = 'ops_region'
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
    cidr_block = models.CharField(verbose_name='网段', max_length=64)
    region = models.ForeignKey('Region', verbose_name='区域', to_field='id')
    creation_time = models.CharField(verbose_name='创建时间', max_length=64, blank=True, null=True)
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
        db_table = 'ops_vpc'
        verbose_name_plural = 'VPC表'


class InstanceInfo(models.Model):
    '''主机实例信息 '''
    id = models.CharField(verbose_name='实例ID', max_length=64, primary_key=True)
    name = models.CharField(verbose_name='实例名称', max_length=64, null=True, blank=True)
    hostname = models.CharField(verbose_name='主机名', max_length=64, null=True, blank=True)
    key_pair_name = models.CharField(verbose_name='密钥', max_length=64, null=True, blank=True)
    os_type = models.CharField(verbose_name='系统类型', max_length=64, null=True, blank=True)
    os_name = models.CharField(verbose_name='系统名称', max_length=64, null=True, blank=True)
    cpu = models.SmallIntegerField(verbose_name='CPU数量', default=1)
    memory = models.IntegerField(verbose_name='总内存', default=2048)
    mac_address = models.CharField(verbose_name='MAC地址', max_length=64, null=True, blank=True)
    region = models.ForeignKey('Region', verbose_name='区域', )
    zone_id = models.CharField(verbose_name='可用区', max_length=64, null=True, blank=True)
    serial_number = models.CharField(verbose_name='序列号', max_length=64, null=True, blank=True)
    status = models.CharField(verbose_name='状态', max_length=64, null=True, blank=True)
    recyclable = models.BooleanField(verbose_name='可回收', default=False)
    security_group_ids = models.CharField(verbose_name='安全组ID', max_length=128, null=True, blank=True)
    eip_address = models.GenericIPAddressField(verbose_name='弹性IP地址', null=True, blank=True)
    public_ip_address = models.CharField(verbose_name='公网IP', max_length=64, null=True, blank=True)
    primary_ip_address = models.GenericIPAddressField(verbose_name='主IP地址')
    private_ip_address = models.GenericIPAddressField(verbose_name='私有IP地址', null=True, blank=True)
    port = models.IntegerField(verbose_name='SSH端口', default=22)
    creation_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    expired_time = models.DateTimeField(verbose_name='到期时间', auto_now_add=True)
    vpc = models.ForeignKey('VPC', verbose_name='所在VPC')
    idc = models.ForeignKey('IDC', verbose_name='服务商', default=1)
    enabled = models.BooleanField(default=True)
    description = models.TextField(verbose_name='备注', null=True, blank=True)
    bind_user = models.ForeignKey(to="BindUser", to_field='id', on_delete=models.SET_NULL, null=True,
                                  verbose_name='登陆用户', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ops_instance_info'
        verbose_name_plural = '主机实例信息'


class InstanceGroup(models.Model):
    """主机实例组"""
    name = models.CharField(max_length=64, unique=True)
    bind_hosts = models.ManyToManyField("BindHost")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ops_instance_group'
        verbose_name_plural = "主机实例组"


class BindUser(models.Model):
    '''绑定的用户'''
    username = models.CharField(validators='用户名', max_length=32)
    ssh_type_choices = ((0, 'SSH/Password'), (1, 'SSH/Key'))
    ssh_type = models.SmallIntegerField(choices=ssh_type_choices, verbose_name='ssh类型', default=0)
    password = models.CharField(validators='密码', max_length=128, blank=True, null=True)
    comment = models.TextField(verbose_name='备注', blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'ops_bind_user'
        verbose_name_plural = '绑定的用户'


class BindHost(models.Model):
    """绑定远程主机和远程用户的对应关系"""
    host = models.ForeignKey("InstanceInfo")
    remote_user = models.ForeignKey("BindUser")

    def __str__(self):
        return "%s -> %s" % (self.host, self.remote_user)

    class Meta:
        unique_together = ("host", "remote_user")
        db_table = "ops_bind_host"
        verbose_name_plural = '主机与用户绑定关系'


class UserProfileManager(BaseUserManager):
    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            password=password,

        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=64, unique=True )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=('Designates whether the user can log into this admin site.'),
    )

    bind_hosts = models.ManyToManyField("BindHost", blank=True)
    host_groups = models.ManyToManyField("InstanceGroup", blank=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'

    # REQUIRED_FIELDS = ['email',]

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):  # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True



class Task(models.Model):
    """批量任务记录表"""
    user = models.ForeignKey("UserProfile")
    task_type_choices = ((0, 'cmd'), (1, 'file_transfer'))
    task_type = models.SmallIntegerField(choices=task_type_choices)
    content = models.TextField(verbose_name="任务内容")

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.task_type, self.content)

    class Meta:
        db_table = "ops_task"
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
        db_table = "ops_task_log"
        verbose_name_plural = '任务日志'


class ServiceUrl(models.Model):
    """
    服务名对应URL表
    """
    name = models.CharField(max_length=64, verbose_name='服务名称')
    web_url = models.CharField(max_length=128, verbose_name='Web URL地址', null=True, blank=True)
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
        db_table = 'ops_service_url'
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
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='时间')

    class Meta:
        db_table = "ops_web_history"
        verbose_name_plural = '历史登录'
