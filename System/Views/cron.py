from db_server import models
import  datetime
from System.Views.OS_manager.firewall_manager import colse_port
def check_port_excess():
	today = datetime.datetime.now().date()
	obj = models.open_port.objects.filter(end_time__lte=today).filter(on_line='否').all()
	if obj :
		for i in obj:
			res = colse_port('192.168.254.248','admin','DDit#20020607!',i.rule_name)
			if res :
				models.open_port.objects.filter(rule_name=i.rule_name).delete()
				with open('/home/log','a+',encoding='utf-8')as f:
					f.write('ok')
					f.flush()
				f.close()
			
			
	
	
	


