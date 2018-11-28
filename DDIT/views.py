from django.shortcuts import render,HttpResponse,redirect
from db_server import models
from django.core.serializers import serialize
from django.contrib import  auth
import xlrd


def index(request):

    return render(request,'index.html',models.menu_info)


def login(request):
    user = request.POST.get('username',None)
    pwd = request.POST.get('password',None)
    user = auth.authenticate(username=user,password=pwd)
    if user :
        request.session['user_id'] = user.id
        request.session['user'] = user.username
        return redirect('/index.html')
    return render(request,'login.html')



def logout(request):
    return render(request, 'logout.html')


# data = xlrd.open_workbook(r'D:\DDIT\DDIT\采购联系名单_商户明细-改20170612.xlsx')
# table = data.sheet_by_name('Sheet1')
# nrows = table.nrows
# cols = table.ncols
# t= 0
# for i in range(0,int(nrows)):
#     if t not in [0,8,12,13,16,17,19,23,25,27]:
#         info =(table.row_values(i))
#         print(info)
#         name = info[2]
#         Address = info[3]
#         phone = info[4]
#         contacts = info[5]
#         Type = info[1]
#         bill = info[-2]
#         buyer = info[0]
#         #note = info[-1]
#         models.Company_info.objects.create(name=name,Address=Address,phone=phone,contacts=contacts,type=Type,bill=bill,buyer=buyer,)
#     t+=1