from django.shortcuts import render,HttpResponse,redirect
from db_server import models
from django.core.serializers import serialize
from django.contrib import  auth
from DDIT.ddit_plugins import auth, menu_list,get_current_week
from django.contrib.auth import login, authenticate
import xlrd
from DDIT import imortdb_data
from django.utils import timezone

@auth
def index(request):
    DATE = get_current_week()
   # print(DATE[0],DATE[1])
    #new_device = models.host_info.objects.filter(create_at__gte=DATE[0]).filter(create_at__lt=DATE[1]).count()
    add_asset = models.Reserves.objects.filter(create_at__gte=DATE[0]).filter(create_at__lt=DATE[1]).count()
    #print(new_device)
    asset_total = models.Reserves.objects.all().count()
    out2user = models.Reserves.objects.filter(status='在用').count()
    open_port = models.open_port.objects.filter(create_at__gte=DATE[0]).filter(create_at__gte=DATE[1]).count()
    create_vm = models.create_vm.objects.filter(create_at__gte=DATE[0]).filter(create_at__gte=DATE[1]).count()
    on_line2host = models.monitor_host.objects.filter(on_line='在线').count()
    off_line2host = models.monitor_host.objects.exclude(on_line='在线').count()
    Scrap = models.Reserves.objects.filter(status='报废').count()
    total = {'new_device':0,'asset_total':asset_total,'out2user':out2user,
             'add_asset':add_asset,'open_port':open_port,'create_vm':create_vm,
             'on_line2host':on_line2host,'off_line2host':off_line2host,'Scrap':Scrap}
    info = {}
   # print(menu_list(request))
    info.update(total)
    info.update(menu_list(request))
   # print(info)
    return render(request, 'index.html', info)


def Login(request):
    if request.method == 'POST':
        user = request.POST.get('username', None)
        pwd = request.POST.get('password', None)
        user = authenticate(username=user, password=pwd)
        if user:
            login(request, user)
            request.session['user_id'] = user.id
            request.session['user'] = user.username
            return redirect('/index.html')
    return render(request, 'login.html')



def Logut(request):
    return render(request, 'logout.html')


