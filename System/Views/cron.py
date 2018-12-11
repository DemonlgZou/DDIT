from db_server import models

import  datetime,threadpool
from System.Views.OS_manager.firewall_manager import *
from System.Views.OS_manager.ping_cmd import *


def check_port_excess():
	
	today = datetime.datetime.now().date()
	obj = models.open_port.objects.filter(end_time__lte=today).filter(on_line='否').all()
	if obj :
		for i in obj:
			res = colse_port('192.168.254.248','admin','DDit#20020607!',i.rule_name)
			if res :
				models.open_port.objects.filter(rule_name=i.rule_name).delete()
				models.log_system_info.objects.create(action_type='移除',opeater='系统管理员',type='外网访问',
					                                      info='nat server %s  ' % (i.rule_name))
			
			
			
	
	
	


def check_host_Ping():
	obj = models.monitor_host.objects.values('ip').all()
	pool = threadpool.ThreadPool(10)
	requests = threadpool.makeRequests(Ping,obj)
	[pool.putRequest(req) for req in requests ]
	pool.wait()
	