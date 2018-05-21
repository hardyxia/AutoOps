from django.shortcuts import render, redirect, resolve_url, HttpResponse
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from cmdb import models
import json
from django.contrib.auth.decorators import login_required
from utils.pagination import page
from webssh.encryption import encrypt_p, decrypt_p
from django.conf import settings


class InstanceView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(InstanceView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        title = ["实例名称", "主机名", "外网IP", "内网IP", "端口", "服务商", "环境", "到期时间"]
        response = models.InstanceInfo.objects.order_by('-creation_time')
        total = response.count()
        response = page(request, list(response))
        return render(request, 'cmdb/instance.html', {"title": title, "response": response,
                                                      "total": total, "page": 10,
                                                      "web_ssh": settings.WEB_SSH,
                                                      "instance_manage_active": "active open",
                                                      "instance_info_active": "active open",
                                                      })


class InstanceDetailView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(InstanceDetailView, self).dispatch(request, *args, **kwargs)

    def get(self, request, instance_id, *args, **kwargs):
        response = models.InstanceInfo.objects.filter(id=instance_id)
        response = list(response)
        return render(request, 'cmdb/instance_detail.html', {"response": response,
                                                             "instance_manage_active": "active open",
                                                             "instance_info_active": "active open"
                                                             })


class InstanceDeleteView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(InstanceDeleteView, self).dispatch(request, *args, **kwargs)

    def get(self, request, instance_id, *args, **kwargs):
        models.InstanceInfo.objects.filter(id=instance_id).delete()
        return redirect(reverse('instance'))


class InstanceAddView(View):
    @method_decorator(login_required, )
    def dispatch(self, request, *args, **kwargs):
        return super(InstanceAddView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'cmdb/instance_add.html', {
            "instance_manage_active": "active open",
            "instance_info_active": "active"
        })

    def post(self, request, *args, **kwargs):
        try:
            data = json.dumps(request.POST)
            dic = json.loads(data)
            del dic['csrfmiddlewaretoken']
            models.InstanceInfo.objects.create(**dic)
            return redirect(reverse('instance'))
        except Exception as e:
            print(str(e))
            return render(request, 'cmdb/instance_add.html', {
                "instance_manage_active": "active open",
                "instance_info_active": "active",
                "error": '输入错误'})


class InstanceEditView(View):
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(InstanceEditView, self).dispatch(request, *args, **kwargs)

    def get(self, request, instance_id, *args, **kwargs):
        response = models.InstanceInfo.objects.filter(id=instance_id)
        response = list(response)
        return render(request, 'cmdb/instance_edit.html', {"response": response,
                                                           "instance_manage_active": "active open",
                                                           "instance_info_active": "active open"
                                                           })

    def post(self, request, instance_id, *args, **kwargs):
        data = json.dumps(request.POST)
        dic = json.loads(data)
        models.InstanceInfo.objects.filter(id=instance_id).update(**dic)
        return redirect(reverse('instance'))


class BindUserView(View):
    @method_decorator(login_required, )
    def dispatch(self, request, *args, **kwargs):
        return super(BindUserView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        title = ["用户名", "密码", "SSH类型", "备注", ]
        response = models.BindUser.objects.all()
        total = response.count()
        response = page(request, list(response))
        return render(request, 'cmdb/bind_user.html', {"title": title, "response": response,
                                                       "total": total, "page": 10,
                                                       "instance_manage_active": "active open",
                                                       "bind_user_active": "active"
                                                       })


class BindUserAddView(View):
    @method_decorator(login_required, )
    def dispatch(self, request, *args, **kwargs):
        return super(BindUserAddView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'cmdb/bind_user_add.html', {
            "instance_manage_active": "active open",
            "bind_user_active": "active"
        })

    def post(self, request, *args, **kwargs):
        try:
            data = json.dumps(request.POST)
            dic = json.loads(data)
            dic['password'] = encrypt_p(dic['password'])
            del dic['csrfmiddlewaretoken']
            models.BindUser.objects.create(**dic)
            return redirect(reverse('bind_user'))
        except Exception as e:
            print(str(e))
            return render(request, 'cmdb/bind_user_add.html', {
                "instance_manage_active": "active open",
                "bind_user_active": "active",
                "error": '输入错误'})


class BindUserEditView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(BindUserEditView, self).dispatch(request, *args, **kwargs)

    def get(self, request, user_id, *args, **kwargs):
        response = models.BindUser.objects.filter(id=user_id)
        password = decrypt_p(response.values('password')[0]['password'])
        response = list(response)

        return render(request, 'cmdb/bind_user_edit.html', {"response": response, "password": password,
                                                            "instance_manage_active": "active open",
                                                            "bind_user_active": "active"
                                                            })

    def post(self, request, user_id, *args, **kwargs):
        data = json.dumps(request.POST)
        dic = json.loads(data)
        dic['password'] = encrypt_p(dic['password'])
        del dic['csrfmiddlewaretoken']
        models.BindUser.objects.filter(id=user_id).update(**dic)
        return redirect(reverse('bind_user'))


class BindUserDetailView(View):
    @method_decorator(login_required, )
    def dispatch(self, request, *args, **kwargs):
        return super(BindUserDetailView, self).dispatch(request, *args, **kwargs)

    def get(self, request, user_id, *args, **kwargs):
        response = models.BindUser.objects.filter(id=user_id)
        response = list(response)
        return render(request, 'cmdb/bind_user_detail.html', {"response": response,
                                                              "instance_manage_active": "active open",
                                                              "bind_user_active": "active"
                                                              })


class BindUserDeleteView(View):
    @method_decorator(login_required, )
    def dispatch(self, request, *args, **kwargs):
        return super(BindUserDeleteView, self).dispatch(request, *args, **kwargs)

    def get(self, request, user_id, *args, **kwargs):
        models.BindUser.objects.filter(id=user_id).delete()
        return redirect(reverse('bind_user'))


class ServiceUrlView(View):
    @method_decorator(login_required, )
    def dispatch(self, request, *args, **kwargs):
        return super(ServiceUrlView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        title = ["名称", "外网地址", "真实地址", "协议", "是否认证", ]
        response = models.ServiceUrl.objects.order_by('connection')
        total = response.count()
        response = page(request, list(response))
        return render(request, 'cmdb/service_url.html', {"title": title, "response": response,
                                                         "total": total, "page": 10,
                                                         "instance_manage_active": "active open",
                                                         "service_url_active": "active"
                                                         })


class ServiceUrlDetailView(View):
    @method_decorator(login_required, )
    def dispatch(self, request, *args, **kwargs):
        return super(ServiceUrlDetailView, self).dispatch(request, *args, **kwargs)

    def get(self, request, service_id, *args, **kwargs):
        response = models.ServiceUrl.objects.filter(id=service_id)
        response = list(response)
        return render(request, 'cmdb/server_url_detail.html', {"response": response,
                                                               "instance_manage_active": "active open",
                                                               "service_url_active": "active open"
                                                               })


class ServiceUrlDeleteView(View):
    @method_decorator(login_required, )
    def dispatch(self, request, *args, **kwargs):
        return super(ServiceUrlDeleteView, self).dispatch(request, *args, **kwargs)

    def get(self, request, url_id, *args, **kwargs):
        models.ServiceUrl.objects.filter(id=url_id).delete()
        return redirect(reverse('service_url'))


class ServiceUrlEditView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ServiceUrlEditView, self).dispatch(request, *args, **kwargs)

    def get(self, request, instance_id, *args, **kwargs):
        response = models.ServiceUrl.objects.filter(id=instance_id)
        response = list(response)
        return render(request, 'cmdb/service_url_edit.html', {"response": response,
                                                              "instance_manage_active": "active open",
                                                              "service_url_active": "active open"
                                                              })

    def post(self, request, url_id, *args, **kwargs):
        data = json.dumps(request.POST)
        dic = json.loads(data)
        del dic['csrfmiddlewaretoken']
        models.ServiceUrl.objects.filter(id=url_id).update(**dic)
        return redirect(reverse('service_url'))


class ServiceUrlAddView(View):
    @method_decorator(login_required, )
    def dispatch(self, request, *args, **kwargs):
        return super(ServiceUrlAddView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'cmdb/server_url_add.html', {
            "instance_manage_active": "active open",
            "service_url_active": "active"
        })

    def post(self, request, *args, **kwargs):
        try:
            data = json.dumps(request.POST)
            dic = json.loads(data)
            del dic['csrfmiddlewaretoken']
            # dic["connection"] = int(dic["connection"])
            # dic["auth"] = int(dic["auth"])
            models.ServiceUrl.objects.create(**dic)
            return redirect(reverse('service_url'))
        except Exception as e:
            print(str(e))
            return render(request, 'cmdb/server_url_add.html', {
                "instance_manage_active": "active open",
                "instance_info_active": "active",
                "error": '输入错误'})


class WebSSHView(View):
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(WebSSHView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        id = request.POST.get('id', None)
        obj = models.InstanceInfo.objects.get(id=id)
        ip = obj.eip_address
        port = obj.port
        username = obj.bind_user.username
        password = obj.bind_user.password
        ret = {"ip": ip, "port": port, "username": username, 'password': password, "static": True}
        login_ip = request.META['REMOTE_ADDR']

        models.WebHistory.objects.create(user=request.user, ip=login_ip, login_user=obj.bind_user.username, host=ip)
        # print(ret)
        return HttpResponse(json.dumps(ret))


'''
@login_required
@csrf_exempt
def web_ssh(request):
    if request.method == 'POST':
        # print(request.POST)
        id = request.POST.get('id', None)
        obj = models.InstanceInfo.objects.get(id=id)

        # ip = obj.eip_address + ":" + obj.bind_user.port
        # ip = '%s:%s' % (obj.eip_address, obj.bind_user.port)
        ip = obj.eip_address
        port = obj.port
        username = obj.bind_user.username
        password = obj.bind_user.password
        ret = {"ip": ip, "port": port, "username": username, 'password': password, "static": True}
        login_ip = request.META['REMOTE_ADDR']

        models.WebHistory.objects.create(user=request.user, ip=login_ip, login_user=obj.bind_user.username, host=ip)
        # print(ret)
        return HttpResponse(json.dumps(ret))
'''
