from db_server import models

import  datetime,threadpool
from System.Views.OS_manager.firewall_manager import *
from System.Views.OS_manager.AC_manager import *
from System.Views.OS_manager.cron_tasks import *

import  logging

ddit_collect = logging.getLogger("collect")
ddit_error = logging.getLogger('error')

def check_port_excess():
	try:
		with models.transaction.atomic():
			today = datetime.datetime.now().date()
			obj = models.open_port.objects.filter(end_time__lte=today).filter(on_line='否').all()
			for i in obj:
					res = close_port('192.168.254.248','admin','dX!ZCQ#l#UAPY5Cu',i.rule_name)
					if res :
						with models.transaction.atomic():
							models.open_port.objects.filter(rule_name=i.rule_name).delete()
							models.log_system_info.objects.create(action_type='移除',opeater='系统管理员',type='外网访问',
								                                      info='nat server %s  ' % (i.rule_name))
	except Exception as e:
		ddit_error.error(e)
			
			

def check_host_Ping():
	#定期检查虚拟服务器设备状态
	try:
		obj_list = ['192.168.0.242','192.168.0.243','192.168.0.244','192.168.0.251']
		
		get_host_status(obj_list)
		
		# requests = threadpool.makeRequests(get_host_status,obj)
		# [pool.putRequest(req) for req in requests ]
		# pool.wait()# pool = threadpool.ThreadPool(10)
	except Exception as e:
		ddit_error.error(e)
		
		

def discover_vm_host():
	try:
		obj_list = ['192.168.0.242', '192.168.0.243', '192.168.0.244', '192.168.0.251']
		
		add_vm_host(obj_list)
	except Exception as e:
		ddit_error.error(e)
	


def check_wifi_user_time():
	#定期检查wifi用户是否超期，超期将自动剔除该用户
	today = datetime.datetime.now().date()
	obj = models.WIFI_USERS_LIST.objects.filter(expired_at__lt=today).all()
	for i in obj:
		if  i.user_type == 1 and i.mode !=1 :###公司用户临时授权
			with models.transaction.atomic():
				detele_wifi_user(i.user)
				models.WIFI_USERS_LIST.objects.get(i.user).delete()
				models.WIFI_OPEARTION_RECORD.objects.create(action='删除用户', opeartor='系统管理员',
				                                            info=f'undo local-user {i.user} class network')
		elif i.user_type != 1  :###访客用户临时授权
			with models.transaction.atomic():
				detele_wifi_guest(i.user)
				models.WIFI_USERS_LIST.objects.get(i.user).delete()
				models.WIFI_OPEARTION_RECORD.objects.create(action='删除用户', opeartor='系统管理员',
				                                            info=f'undo local-user {i.user} class network guest')
#def dingding_submit_internet_cost():
	
	#每个月1日自动通过钉钉提交申请宽带费用
	#create_task(CTCC_special_line)#电信申请单
	#create_task(CUCC_special_line)#联通申请单
	
	
def flow_up_clear():
	try:
		today = datetime.datetime.now().date()
		obj = models.WIFI_USERS_LIST.objects.filter(mode=0).filter(expired_at__lt=today).all()
		for i in obj:
			res = canlce_keep_up_flow('192.168.254.248','admin',i.host_ip,i.mask)
			if res:
			   with models.transaction.atomic():
				   models.UP_FLOW_LIST.objects.get(id=i.id).delete()
				   models.log_system_info.objects.create(action_type='移除', opeater='系统管理员', type='取消上行带宽保障',
				                                         info='undo source-address  %s %s ' % (i.host_ip,i.mask))
	except Exception as e:
		ddit_error.error(e)