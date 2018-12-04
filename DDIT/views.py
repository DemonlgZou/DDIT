from django.shortcuts import render,HttpResponse,redirect
from db_server import models
from django.core.serializers import serialize
from django.contrib import  auth
from DDIT.ddit_plugins import auth,menu_list
from django.contrib.auth import login, logout, authenticate
import xlrd

@auth
def index(request):
    return render(request,'index.html',menu_list(request))


def Login(request):
    if request.method == 'POST':
        user = request.POST.get('username',None)
        pwd = request.POST.get('password',None)
        user = authenticate(username=user,password=pwd)
        if user :
            login(request, user)
            request.session['user_id'] = user.id
            request.session['user'] = user.username
            return redirect('/index.html')

    return render(request,'login.html')



def Logut(request):
    return render(request, 'logout.html')


