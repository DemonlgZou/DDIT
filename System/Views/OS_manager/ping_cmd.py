import platform,subprocess
from db_server import models

def Ping(ip):
	os_info = platform.system()
	if os_info == 'Linux':
		cmd = 'ping %s %s 4' % (ip.get('ip'), '-c')
	elif os_info == 'Windows':
		cmd = 'ping %s %s 4' % (ip.get('ip'), '-n')
	a = subprocess.call(cmd, shell=True)
	if a == 1:
		print('主机不可达')
		
		on_line = '不在线'
		models.monitor_host.objects.filter(ip=ip.get('ip')).update(on_line=on_line)
	elif a == 0:
		print('主机可达')
		on_line = '在线'
		models.monitor_host.objects.filter(ip=ip.get('ip')).update(on_line=on_line)
	