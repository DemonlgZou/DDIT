from django.db import models,transaction
from django.db.models import Q, F, Func, Value
from django.db.models.functions import Concat
from django.contrib.auth.models import User, Group
import xlrd, os


class Menu(models.Model):
    # 系统菜单表
    cname = models.CharField(verbose_name='菜单别名', max_length=128)
    url = models.CharField(verbose_name='链接地址', max_length=128, null=True)
    name = models.CharField(verbose_name='菜单名', max_length=128)
    top = models.SmallIntegerField(verbose_name='菜单', null=True)
    child = models.SmallIntegerField(verbose_name='二级菜单', null=True)
    top_no = models.SmallIntegerField(verbose_name='父级菜单ID', null=True)

    class Meta:
        db_table = 'ddit_menu'


class Role2Menu(models.Model):
    rid = models.ForeignKey(User, related_name='user', on_delete=None, null=True)
    #  group = models.ForeignKey(Group,related_name='group',on_delete=None,null=True)
    menu = models.ForeignKey('Menu', related_name='menu', on_delete=None, null=True)

    class Meta:
        db_table = 'ddit_Role2Menu'


class FAssets(models.Model):
    # 出库记录表
    asset_info = models.ForeignKey('Reserves', related_name='no', on_delete=None)
    asset_user = models.CharField(max_length=128, verbose_name='领用人')
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_created=True, auto_now=True, null=True)

    class Meta:
        db_table = 'ddit_assets'


class Dictionary(models.Model):
    arr1 = models.CharField(max_length=128, unique=True,null=True)#设备类型缩写
    arr2 = models.CharField(max_length=10, null=True)
    arr3 = models.CharField(max_length=128,null=True)
    arr4 = models.CharField(max_length=128,null=True)
    # arr3 = models.CharField(max_length=6, default='000')
    # cname = models.CharField(max_length=128)

    class Meta:
        db_table = 'ddit_dict'


class Reserves(models.Model):
    # 固定资产表
    # type_list = ((1,'固定资产'),(2,'低值易耗品'),(3,'其他'))
    name = models.CharField(max_length=128, verbose_name='资产名')
    Type = models.CharField(verbose_name='资产类别', max_length=32)
    # product_model = models.CharField(max_length=128,verbose_name='产品型号')
    asset_No = models.CharField(max_length=128, unique=True, verbose_name='设备编码')
    price = models.CharField(verbose_name='资产价格',max_length=128)
    company = models.CharField(max_length=128, verbose_name='供应商')
    contacts = models.CharField(max_length=128, verbose_name='联系人')
    manger_user = models.CharField(max_length=128, verbose_name='管理人')
    status = models.CharField(verbose_name='资产状态', max_length=32)
    # status = models.SmallIntegerField(choices=status_list,verbose_name='设备状态')
    info = models.ForeignKey('host_info', related_name='host', on_delete=None)
    finance_id = models.CharField(max_length=128,verbose_name='财务对应资产编号',null=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_created=True, auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='更新时间', auto_created=True, auto_now=True)

    class Meta:
        db_table = 'ddit_reserves'


class host_info(models.Model):
    # 设备相信信息
    sn = models.CharField(max_length=128, null=True, verbose_name='设备')
    name = models.CharField(max_length=128, null=True, verbose_name='设备名称')
    type = models.CharField(max_length=128, null=True, verbose_name='设备类型')
    info = models.TextField(verbose_name='设备详细信息')
    create_at = models.DateTimeField(verbose_name='创建时间', auto_created=True, auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='更新时间', auto_created=True, auto_now=True)
    class Meta:
        db_table = 'ddit_host_info'

class Assets_log(models.Model):
    '''资产管理操作记录'''
    #action ：1、新增；2、修改；3、删除
    action = models.SmallIntegerField()
    operator = models.CharField(max_length=64,verbose_name='操作者',null=True)
    asset_no = models.CharField(max_length=256,null=True)
    asset_status = models.CharField(max_length=128,null=True)
    desc = models.CharField(max_length=256,null=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_created=True, auto_now_add=True)
    class Meta:
        db_table = 'ddit_assets_log'


class Company_info(models.Model):
    '''供货商公司名称'''
    name = models.CharField(max_length=128, verbose_name='供货商公司名', default='无')
    contacts = models.CharField(max_length=128, verbose_name='联系人', default='无')
    phone = models.CharField(verbose_name='电话号码', max_length=32)
    type = models.CharField(max_length=32, verbose_name='职能所属')
    Address = models.CharField(max_length=128, verbose_name='地址')
    bill = models.CharField(max_length=32, verbose_name='开票类型')
    buyer = models.CharField(max_length=128, verbose_name='采购类别')
    create_at = models.DateTimeField(verbose_name='创建时间', auto_created=True, auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='更新时间', auto_created=True, auto_now=True)

    class Meta:
        db_table = 'ddit_company'


class Server_info(models.Model):
    '''服务器信息'''

    name = models.CharField(verbose_name='服务器名称', max_length=32)
    IP = models.CharField(max_length=128,verbose_name='IP地址', null=True)
    OS = models.CharField(verbose_name='操作系统类型', max_length=128, null=True)
    desric = models.CharField(verbose_name='说明', max_length=128, null=True)
    status = models.CharField(max_length=128, verbose_name='服务器状态', null=True)
    server = models.CharField(verbose_name='服务器类型', max_length=4, null=True)
    type = models.CharField(verbose_name='虚拟化技术类型',max_length=128,null=True)
    true_server = models.CharField(max_length=128, verbose_name='宿主机', null=True)
    Max_cpus = models.SmallIntegerField(verbose_name='CPU数量',null=True)
    Max_meminfo = models.CharField(max_length=128, verbose_name='内存大小', null=True)
    Max_disk = models.CharField(max_length=128, verbose_name='硬盘大小', null=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_created=True, auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='更新时间', auto_created=True, auto_now=True)
    class Meta:
        db_table = 'ddit_server_info'


class PM_list(models.Model):
    '''项目明细'''
    contract_id = models.CharField(max_length=128, verbose_name='合同编号', null=True)
    contract_start = models.CharField(verbose_name='合同开始日期', null=True,max_length=128)
    contract_end = models.CharField(verbose_name='合同结束日期', null=True,max_length=128)
    contract_price = models.CharField(verbose_name='合同金额', null=True,max_length=128)
    contract_work = models.CharField(verbose_name='预期工作量', null=True,max_length=128)
    pid = models.CharField(max_length=128, verbose_name='项目编号', unique=True)
    father_name = models.CharField(max_length=128, verbose_name='项目名称')
    child_name = models.CharField(max_length=128, verbose_name='项目二级分类')
    service2in = models.CharField(max_length=128, verbose_name='业务线标识in',null=True)
    service2out = models.CharField(max_length=128, verbose_name='业务线标识out',null=True)
    operator = models.CharField(max_length=128, verbose_name='执行方')
    manager = models.CharField(max_length=128, verbose_name='责任方')
    date_time = models.CharField(verbose_name='上线时间', null=True,max_length=128)
    Manage = models.CharField(max_length=128, verbose_name='PM', null=True)
    step = models.CharField(max_length=10, verbose_name='当前阶段')
    desc = models.CharField(max_length=128,verbose_name='备注说明',null=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_created=True, auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='更新时间', auto_created=True, auto_now=True)

    class Meta:
        db_table = 'ddit_PM_list'


class Work_hours(models.Model):
    '''工作量统计表'''
    arr1 = models.FloatField(verbose_name='1月数据', null=True)
    arr2 = models.FloatField(verbose_name='2月数据', null=True)
    arr3 = models.FloatField(verbose_name='3月数据', null=True)
    arr4 = models.FloatField(verbose_name='4月数据', null=True)
    arr5 = models.FloatField(verbose_name='5月数据', null=True)
    arr6 = models.FloatField(verbose_name='6月数据', null=True)
    arr7 = models.FloatField(verbose_name='7月数据', null=True)
    arr8 = models.FloatField(verbose_name='8月数据', null=True)
    arr9 = models.FloatField(verbose_name='9月数据', null=True)
    arr10 = models.FloatField(verbose_name='10月数据', null=True)
    arr11 = models.FloatField(verbose_name='11月数据', null=True)
    arr12 = models.FloatField(verbose_name='12月数据', null=True)
    date = models.CharField(max_length=32, verbose_name='年份', null=True)
    item = models.ForeignKey('PM_list', related_name='pm_id', on_delete=None, null=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_created=True, auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='更新时间', auto_created=True, auto_now=True)

    class Meta:
        db_table = 'ddit_Work_hours'


class period(models.Model):
    '''里程碑数据库'''
    name = models.CharField(max_length=128, verbose_name='任务名称',null=True)
    start_at = models.CharField(verbose_name='开始时间',max_length=128,null=True)
    end_at = models.CharField(verbose_name='结束时间',max_length=128,null=True)
    delay = models.CharField(verbose_name='延期时间',max_length=128,null=True)
    plan_no = models.CharField(verbose_name='预期工作量',max_length=128,null=True)
    fact_no = models.CharField(max_length=128, verbose_name='实际工作量',null=True)
    Evaluation = models.CharField(max_length=128, verbose_name='考评内容',null=True)
    no = models.ForeignKey('PM_list',related_name='No', verbose_name='项目编号', on_delete=None)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_created=True, auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='更新时间', auto_created=True, auto_now=True)

    class Meta:
        db_table = 'ddit_period'

class open_port(models.Model):
    '''开通外网端口的'''
    proposer = models.CharField(max_length=128,verbose_name='申请人')
    dept = models.CharField(max_length=128,verbose_name='申请人部门')
    rule_name = models.CharField(max_length=128,verbose_name='策略名',unique=True)
    desc = models.CharField(max_length=128, verbose_name='策略用途')
    host_ip = models.GenericIPAddressField(verbose_name='ip地址')
    type = models.CharField(max_length=32,verbose_name='协议类型')
    inside_port = models.CharField(verbose_name='内网端口号',max_length=32)
    outside_port = models.CharField(verbose_name='外网端口号',max_length=32)
    start_time = models.DateField(verbose_name='开始日期',auto_created=True, auto_now_add=True)
    end_time = models.DateField(verbose_name='到期日期',null=True)
    on_line = models.CharField(verbose_name='端口状态',null=True,max_length=32)

    create_at = models.DateTimeField(verbose_name='创建时间', auto_created=True, auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='更新时间', auto_created=True, auto_now=True)
    interface = models.CharField(max_length=128,verbose_name='接口名')


    class Meta:
        db_table = 'ddit_open_port'


class create_vm (models.Model):
    '''创建虚拟机记录信息'''
    proposer = models.CharField(max_length=128, verbose_name='申请人')
    dept = models.CharField(max_length=128, verbose_name='申请人部门')
    name = models.UUIDField(verbose_name='机器名')
    host_ip = models.GenericIPAddressField(verbose_name='宿主机IP地址',null=True)
    vm_ip = models.GenericIPAddressField(verbose_name='虚拟机IP地址',null=True)
    cpus = models.SmallIntegerField(verbose_name='CPU个数')
    memory = models.SmallIntegerField(verbose_name='内存大小')
    disk = models.CharField(verbose_name='硬盘大小',max_length=128)
    type = models.CharField(verbose_name='机器类型',max_length=128)
    os_type = models.CharField(verbose_name='机器类型',max_length=128)
    end_time = models.DateField(verbose_name='到期日期', null=True)
    on_line = models.BooleanField(verbose_name='永久生效')
    create_at = models.DateTimeField(verbose_name='创建时间', auto_created=True, auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='更新时间', auto_created=True, auto_now=True)
    class Meta:
        db_table = 'ddit_create_vm'


class log_system_info(models.Model):
    #端口操作日志
    action_type = models.CharField(verbose_name='操作类型',max_length=128)
    opeater = models.CharField(verbose_name='操作人员',max_length=128)
    type = models.CharField(verbose_name='操作类型',max_length=128)
    info = models.CharField(verbose_name='操作日志',max_length=128)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_created=True, auto_now_add=True)
    host = models.CharField(verbose_name='执行主机',max_length=128)

    class Meta:
        db_table = 'ddit_system_info'


class log_vm_info(models.Model):
    #创建虚拟机操作日志
    action_type = models.CharField(verbose_name='操作类型', max_length=128)
    opeater = models.CharField(verbose_name='操作人员', max_length=128)
    type = models.CharField(verbose_name='操作类型', max_length=128)
    info = models.CharField(verbose_name='操作日志', max_length=128)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_created=True, auto_now_add=True)
    host = models.CharField(verbose_name='执行主机', max_length=128)

    class Meta:
        db_table = 'ddit_vm_info'

class monitor_host(models.Model):
      name = models.CharField(max_length=128,verbose_name='机器名')
      ip = models.GenericIPAddressField(unique=True,verbose_name='主机地址')
      user = models.CharField(max_length=32,verbose_name='用户名',null=True)
      pwd = models.CharField(max_length=256,verbose_name='密码',null=True)
      on_line = models.CharField(max_length=256,verbose_name='状态',null=True)
      update_at = models.DateTimeField(verbose_name='更新时间', auto_created=True, auto_now=True)
      create_at = models.DateTimeField(verbose_name='创建时间', null=True, max_length=128)
      class Meta:
          db_table = 'ddit_monitor_host'


class monitor_stat(models.Model):
    cpu = models.CharField(verbose_name='CPU百分比', null=True,max_length=128)
    meminfo = models.CharField(verbose_name='内存百分比', null=True,max_length=128)
    diskinfo = models.CharField(verbose_name='磁盘百分比', null=True,max_length=128)
    netinfo = models.CharField(verbose_name='网络百分比', null=True,max_length=128)
    create_at = models.DateTimeField(verbose_name='创建时间', null=True,max_length=128,auto_created=True,auto_now=True)
    ip = models.CharField(max_length=128, verbose_name='主机名称')
    class Meta:
        db_table = 'ddit_monitor_stat'


class WIFI_OPEARTION_RECORD(models.Model):
    #action 代表操作动作 主要有3类 新增、删除和强制下线
    #info 代表具体操作命令
    action = models.CharField(max_length=128,verbose_name='动作内容')
    created_at = models.DateField(verbose_name='操作时间',null=True,auto_created=True,auto_now=True)
    opeartor = models.CharField(verbose_name='操作人员',max_length=128)
    info = models.TextField(verbose_name='操作内容')

    class Meta:
        db_table = 'ddit_wifi_opeartion_record'




class WIFI_USERS_LIST(models.Model):
    #user_type 1代表是正常用户,2代表是guest用户,
    # mode 1代表是长期用户,2代表是临时用户
    user = models.CharField(max_length=128,verbose_name='用户名',unique=True)
    pwd = models.CharField(max_length=128,verbose_name='密码',null=True)
    mode = models.SmallIntegerField(verbose_name='授权类型')
    created_at = models.DateField(verbose_name='创建时间',null=True,auto_created=True,auto_now=True)
    updated_at = models.DateField(verbose_name='更新时间',null=True,auto_created=True,auto_now=True)
    expired_at = models.DateField(verbose_name='到期时间',null=True)
    user_type = models.SmallIntegerField(verbose_name='账号类型')
    started_at = models.DateField(verbose_name='授权开始时间',null=True)
    dingding_id = models.CharField(verbose_name='钉钉审批单号',max_length=256,null=True)
    proposer = models.CharField(verbose_name='申请人',max_length=128,null=True)
    dept = models.CharField(verbose_name='申请部门',max_length=128,null=True)
    operator = models.CharField(verbose_name='操作人',max_length=128,null=True)
    max_num = models.SmallIntegerField(verbose_name='最大允许在线人数',default=1)
    desc = models.TextField(verbose_name='备注信息',null=True)
    class Meta:
        db_table = 'ddit_wifi_user_list'



class UP_FLOW_LIST(models.Model):
    dingding_id = models.CharField(verbose_name='钉钉审批单号', max_length=256, null=True)
    proposer = models.CharField(verbose_name='申请人', max_length=128, null=True)
    dept = models.CharField(verbose_name='申请部门', max_length=128, null=True)
    operator = models.CharField(verbose_name='操作人', max_length=128, null=True)
    mode = models.SmallIntegerField(verbose_name='授权类型')
    started_at = models.DateField(verbose_name='授权开始时间', null=True)
    expired_at = models.DateField(verbose_name='到期时间', null=True)
    created_at = models.DateField(verbose_name='创建时间', null=True, auto_created=True, auto_now=True)
    #updated_at = models.DateField(verbose_name='更新时间', null=True, auto_created=True, auto_now=True)
    desc = models.TextField(verbose_name='策略用途', null=True)
    host_ip = models.GenericIPAddressField(verbose_name='IP地址',null=True)
    mask = models.GenericIPAddressField(verbose_name='子网掩码',null=True)
    class Meta:
        db_table = 'ddit_up_flow_list'