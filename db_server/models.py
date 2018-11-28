from django.db import models
from django.db.models import Q,F,Func,Value
from django.db.models.functions import Concat
from django.contrib.auth.models import User,Group
import xlrd ,os

class Menu(models.Model):
# 系统菜单表
    cname = models.CharField(verbose_name='菜单别名',max_length=128)
    url = models.CharField(verbose_name='链接地址',max_length=128,null=True)
    name = models.CharField(verbose_name='菜单名',max_length=128)
    top = models.SmallIntegerField(verbose_name='菜单',null=True)
    child = models.SmallIntegerField(verbose_name='二级菜单',null=True)
    top_no = models.SmallIntegerField(verbose_name='父级菜单ID',null=True)


    class Meta:
      db_table = 'ddit_menu'


class Role2Menu(models.Model):
    rid = models.ForeignKey(User,related_name='user',on_delete=None,null=True)
  #  group = models.ForeignKey(Group,related_name='group',on_delete=None,null=True)
    menu = models.ForeignKey('Menu',related_name='menu',on_delete=None,null=True)
    class Meta:
        db_table = 'ddit_Role2Menu'


class FAssets(models.Model):
    #出库记录表

    asset_info = models.ForeignKey('Reserves',related_name='no',on_delete=None)
    asset_user = models.CharField(max_length=128,verbose_name='领用人')
    created_at = models.DateTimeField(auto_created=True,auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_created=True,auto_now=True,null=True)

    class Meta:
        db_table = 'ddit_assets'

class Dictionary(models.Model):
    arr1 = models.CharField(max_length=4,default='DDIT')
    arr2 = models.CharField(max_length=4,unique=True)
    arr3 = models.CharField(max_length=6,null=True)
    cname = models.CharField(max_length=128)

class Reserves(models.Model):
#固定资产表
  #type_list = ((1,'固定资产'),(2,'低值易耗品'),(3,'其他'))
  name = models.CharField(max_length=128,verbose_name='资产名')
  Type = models.CharField(verbose_name='资产类别',max_length=32)
  #product_model = models.CharField(max_length=128,verbose_name='产品型号')
  asset_No = models.CharField(max_length=128,unique=True,verbose_name='设备编码')
  price = models.SmallIntegerField(verbose_name='资产价格')
  company = models.CharField(max_length=128,verbose_name='供应商')
  contacts = models.CharField(max_length=128,verbose_name='联系人')
  manger_user = models.CharField(max_length=128,verbose_name='管理人')
  status = models.CharField(verbose_name='资产状态',max_length=32)
  # status = models.SmallIntegerField(choices=status_list,verbose_name='设备状态')
  info = models.ForeignKey('host_info',related_name='host',on_delete=None)
  create_at = models.DateTimeField(verbose_name='创建时间',auto_created=True,auto_now_add=True)
  update_at = models.DateTimeField(verbose_name='更新时间',auto_created=True,auto_now=True)
  class Meta:
      db_table = 'ddit_reserves'



class host_info(models.Model):
      #设备相信信息
      name = models.CharField(max_length=128,null=True,verbose_name='设备名称')
      type = models.CharField(max_length=128,null=True,verbose_name='设备类型')
      CPU = models.CharField(max_length=128,null=True,verbose_name='CPU型号')
      Memory = models.CharField(max_length=128,null=True,verbose_name='内存型号')
      Bios = models.CharField(max_length=128,null=True,verbose_name='主板型号')
      MAC= models.CharField(max_length=128,null=True,verbose_name='mac地址',unique=True)
      SN = models.CharField(max_length=128,null=True,verbose_name='S/N')
      NETWORK = models.CharField(max_length=128,null=True,verbose_name='网卡型号')
      CDrom = models.CharField(max_length=128,null=True,verbose_name='光驱型号')
      Video = models.CharField(max_length=128,null=True,verbose_name='显卡型号')
      Sound = models.CharField(max_length=128,null=True,verbose_name='声卡型号')
      Disk  = models.CharField(max_length=128,null=True,verbose_name='硬盘')
      Display =  models.CharField(max_length=128,null=True,verbose_name='显示器')
      create_at = models.DateTimeField(verbose_name='创建时间',auto_created=True,auto_now_add=True)
      update_at = models.DateTimeField(verbose_name='更新时间',auto_created=True,auto_now=True)


class Assets_log(models.Model):
    #资产管理操作记录
    pass

    class Meta:
        db_table = 'ddit_assets_log'

class Company_info(models.Model):
#供货商公司名称
   name = models.CharField(max_length=128,verbose_name='供货商公司名',default='无')
   contacts = models.CharField(max_length=128,verbose_name='联系人',default='无')
   phone = models.CharField(verbose_name='电话号码',max_length=32)
   type = models.CharField(max_length=32,verbose_name='职能所属')
   Address = models.CharField(max_length=128,verbose_name='地址')
   bill = models.CharField(max_length=32,verbose_name='开票类型')
   buyer = models.CharField(max_length=128,verbose_name='采购类别')
   create_at = models.DateTimeField(verbose_name='创建时间',auto_created=True,auto_now_add=True)
   update_at = models.DateTimeField(verbose_name='更新时间',auto_created=True,auto_now=True)
   class Meta:
        db_table = 'ddit_company'


class Server_info(models.Model):
    #服务器信息

    name = models.CharField(verbose_name='服务器名称',max_length=32)
    IP  = models.GenericIPAddressField(verbose_name='IP地址',unique=True)
    OS = models.CharField(verbose_name='操作系统类型',max_length=128,null=True)
    desric = models.CharField(verbose_name='说明',max_length=128,null=True)
    status = models.CharField(max_length=128,verbose_name='服务器状态',null=True)
    server = models.CharField(verbose_name='服务器类型',max_length=4,null=True)
    true_server = models.CharField(max_length=128,verbose_name='宿主机',null=True)
    create_at = models.DateTimeField(verbose_name='创建时间',auto_created=True,auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='更新时间',auto_created=True,auto_now=True)
    

    class Meta:
        db_table = 'ddit_server_info'

child = Menu.objects.filter(child=1).all()
#print(child)
top = Menu.objects.filter(top=0).all()

menu_info = {'child':child,'top':top}

