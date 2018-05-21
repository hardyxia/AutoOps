# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-21 15:40
from __future__ import unicode_literals

import DjangoUeditor.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=64, unique=True, verbose_name='用户名')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BindHost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': '主机与用户绑定关系',
                'db_table': 'ops_bind_host',
            },
        ),
        migrations.CreateModel(
            name='BindUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, validators=['用', '户', '名'])),
                ('ssh_type', models.SmallIntegerField(choices=[(0, 'SSH/Password'), (1, 'SSH/Key')], default=0, verbose_name='ssh类型')),
                ('password', models.CharField(blank=True, max_length=128, null=True, validators=['密', '码'])),
                ('comment', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name_plural': '绑定的用户',
                'db_table': 'ops_bind_user',
            },
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='机房')),
            ],
            options={
                'verbose_name_plural': '机房表',
                'db_table': 'ops_idc',
            },
        ),
        migrations.CreateModel(
            name='InstanceGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('bind_hosts', models.ManyToManyField(to='cmdb.BindHost')),
            ],
            options={
                'verbose_name_plural': '主机实例组',
                'db_table': 'ops_instance_group',
            },
        ),
        migrations.CreateModel(
            name='InstanceInfo',
            fields=[
                ('id', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='实例ID')),
                ('name', models.CharField(blank=True, max_length=64, null=True, verbose_name='实例名称')),
                ('hostname', models.CharField(blank=True, max_length=64, null=True, verbose_name='主机名')),
                ('key_pair_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='密钥')),
                ('os_type', models.CharField(blank=True, max_length=64, null=True, verbose_name='系统类型')),
                ('os_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='系统名称')),
                ('cpu', models.SmallIntegerField(default=1, verbose_name='CPU数量')),
                ('memory', models.IntegerField(default=2048, verbose_name='总内存')),
                ('mac_address', models.CharField(blank=True, max_length=64, null=True, verbose_name='MAC地址')),
                ('zone_id', models.CharField(blank=True, max_length=64, null=True, verbose_name='可用区')),
                ('serial_number', models.CharField(blank=True, max_length=64, null=True, verbose_name='序列号')),
                ('status', models.CharField(blank=True, max_length=64, null=True, verbose_name='状态')),
                ('recyclable', models.BooleanField(default=False, verbose_name='可回收')),
                ('security_group_ids', models.CharField(blank=True, max_length=128, null=True, verbose_name='安全组ID')),
                ('eip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='弹性IP地址')),
                ('public_ip_address', models.CharField(blank=True, max_length=64, null=True, verbose_name='公网IP')),
                ('primary_ip_address', models.GenericIPAddressField(verbose_name='主IP地址')),
                ('private_ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='私有IP地址')),
                ('port', models.IntegerField(default=22, verbose_name='SSH端口')),
                ('creation_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('expired_time', models.DateTimeField(auto_now_add=True, verbose_name='到期时间')),
                ('enabled', models.BooleanField(default=True)),
                ('description', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('bind_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cmdb.BindUser', verbose_name='登陆用户')),
                ('idc', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cmdb.IDC', verbose_name='服务商')),
            ],
            options={
                'verbose_name_plural': '主机实例信息',
                'db_table': 'ops_instance_info',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='区域编码')),
                ('name', models.CharField(blank=True, max_length=64, null=True, verbose_name='区域名称')),
                ('endpoint', models.URLField(blank=True, null=True, verbose_name='API地址')),
                ('idc', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cmdb.IDC', verbose_name='机房')),
            ],
            options={
                'verbose_name_plural': '可用区表',
                'db_table': 'ops_region',
            },
        ),
        migrations.CreateModel(
            name='ServiceUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='服务名称')),
                ('web_url', models.URLField(blank=True, max_length=128, null=True, verbose_name='Web URL地址')),
                ('real_url', models.CharField(blank=True, max_length=128, null=True, verbose_name='后端URL')),
                ('connection', models.SmallIntegerField(choices=[(1, 'HTTP'), (2, 'TCP')], default=1, verbose_name='协议')),
                ('auth', models.SmallIntegerField(choices=[(1, '是'), (0, '否')], default=1, verbose_name='是否认证')),
                ('user', models.CharField(blank=True, max_length=32, null=True, verbose_name='用户名')),
                ('password', models.CharField(blank=True, max_length=64, null=True, verbose_name='密码')),
            ],
            options={
                'verbose_name_plural': '服务URL关系',
                'db_table': 'ops_service_url',
            },
        ),
        migrations.CreateModel(
            name='VPC',
            fields=[
                ('id', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='VPC ID')),
                ('name', models.CharField(blank=True, max_length=64, null=True, verbose_name='VPC名称')),
                ('is_default', models.BooleanField(default=False, verbose_name='默认VPC')),
                ('status', models.CharField(choices=[('Available', '在线'), ('unAvailable', '离线')], default='Available', max_length=16, verbose_name='状态')),
                ('cidr_block', models.CharField(max_length=64, verbose_name='网段')),
                ('creation_time', models.CharField(blank=True, max_length=64, null=True, verbose_name='创建时间')),
                ('description', DjangoUeditor.models.UEditorField(blank=True, default='', verbose_name='内容')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.Region', verbose_name='区域')),
            ],
            options={
                'verbose_name_plural': 'VPC表',
                'db_table': 'ops_vpc',
            },
        ),
        migrations.CreateModel(
            name='WebHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=32, null=True, verbose_name='登录用户')),
                ('ip', models.GenericIPAddressField(null=True, verbose_name='用户地址')),
                ('login_user', models.CharField(max_length=32, null=True, verbose_name='所用账号')),
                ('host', models.CharField(max_length=32, null=True, verbose_name='登录主机')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='时间')),
            ],
            options={
                'verbose_name_plural': '历史登录',
                'db_table': 'ops_web_history',
            },
        ),
        migrations.AddField(
            model_name='instanceinfo',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.Region', verbose_name='区域'),
        ),
        migrations.AddField(
            model_name='instanceinfo',
            name='vpc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.VPC', verbose_name='所在VPC'),
        ),
        migrations.AddField(
            model_name='bindhost',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.InstanceInfo'),
        ),
        migrations.AddField(
            model_name='bindhost',
            name='remote_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.BindUser'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bind_hosts',
            field=models.ManyToManyField(blank=True, to='cmdb.BindHost'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='host_groups',
            field=models.ManyToManyField(blank=True, to='cmdb.InstanceGroup'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='bindhost',
            unique_together=set([('host', 'remote_user')]),
        ),
    ]