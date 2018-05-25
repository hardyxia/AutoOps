from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.conf import settings
import os, re, json
from web import models
from backend.task_manager import MultiTaskManger

from backend import audit


# Create your views here.

def json_date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.strftime("%Y-%m-%d %T")


@login_required
def dashboard(request):
    return render(request, 'index.html')


def acc_login(request):
    error_msg = ''

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)

            return redirect("/")

        else:
            error_msg = "Wrong username or password!"
    return render(request, "login.html", {'error_msg': error_msg})


def acc_logout(request):
    logout(request)

    return redirect("/login/")


@login_required
def webssh(request):
    return render(request, 'web_ssh.html')


@login_required
def user_audit(request):
    log_dirs = os.listdir(settings.AUDIT_LOG_DIR)

    return render(request, 'user_audit.html', locals())


@login_required
def audit_log_date(request, log_date):
    log_date_path = "%s/%s" % (settings.AUDIT_LOG_DIR, log_date)
    log_file_dirs = os.listdir(log_date_path)
    session_ids = [re.search("\d+", i).group() for i in log_file_dirs]

    session_objs = models.Session.objects.filter(id__in=session_ids)

    return render(request, 'user_audit_file_list.html', locals())


@login_required
def multitask_cmd(request):
    return render(request, "multitask_cmd.html")


@login_required
def multitask_file_transfer(request):
    return render(request, 'multitask_file_transfer.html')


@login_required
def multitask_result(request):
    task_id = request.GET.get('task_id')
    task_obj = models.Task.objects.get(id=task_id)
    task_log_results = list(task_obj.tasklogdetail_set.values('id', 'result', 'status', 'start_date', 'end_date'))

    return HttpResponse(json.dumps(task_log_results, default=json_date_handler))


@login_required
def multitask(request):
    print("--->", request.POST)
    task_data = json.loads(request.POST.get('task_data'))
    print("--->selcted hosts", task_data)

    task_obj = MultiTaskManger(request)
    selected_hosts = list(task_obj.task.tasklogdetail_set.all().values('id', 'bind_host__host__ip_addr',
                                                                       'bind_host__host__hostname',
                                                                       'bind_host__remote_user__username'))

    return HttpResponse(
        json.dumps({'task_id': task_obj.task.id, 'selected_hosts': selected_hosts})
    )


@login_required
def audit_log_detail(request, log_date, session_id):
    log_date_path = "%s/%s" % (settings.AUDIT_LOG_DIR, log_date)
    log_file_path = "%s/session_%s.log" % (log_date_path, session_id)

    log_parser = audit.AuditLogHandler(log_file_path)
    cmd_list = log_parser.parse()

    return render(request, "user_audit_detail.html", locals())
