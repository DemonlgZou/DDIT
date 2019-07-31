import platform,subprocess,libvirt,time,datetime
from db_server import models

# def Ping(ip):
# 	os_info = platform.system()
# 	if os_info == 'Linux':
# 		cmd = 'ping %s %s 4' % (ip.get('ip'), '-c')
# 	elif os_info == 'Windows':
# 		cmd = 'ping %s %s 4' % (ip.get('ip'), '-n')
# 	a = subprocess.call(cmd, shell=True)
# 	if a == 1:
# 		print('主机不可达')
#
# 		on_line = '不在线'
# 		models.monitor_host.objects.filter(ip=ip.get('ip')).update(on_line=on_line)
# 	elif a == 0:
# 		print('主机可达')
# 		on_line = '在线'
# 		models.monitor_host.objects.filter(ip=ip.get('ip')).update(on_line=on_line)
#
def get_host_status(ip):
	try:
		
		conn = libvirt.open('qemu+tcp://root@192.168.0.244/system')
		#print(conn)
		host_stat = conn.lookupByName(ip.get('ip'))
		#host_stat = conn.lookupByName('192.168.0.20')
		#print(host_stat.isActive())
		create_at = datetime.datetime.now()
		if host_stat.isActive() == 1:
			on_line = '在线'
			t1 = time.time()
			c1 = int(host_stat.info()[4])
			time.sleep(1);
			t2 = time.time();
			c2 = int(host_stat.info()[4])
			c_nums = int(host_stat.info()[3])
			usage = (c2 - c1) * 100 / ((t2 - t1) * c_nums * 1e9)
			#print(usage)
			
			with models.transaction.atomic():
				models.monitor_host.objects.filter(ip=ip.get('ip')).update(on_line=on_line)
				models.monitor_stat.objects.create(cpu=usage,ip=ip.get('ip'),create_at=create_at)
		else:
			on_line = '不在线'
			with models.transaction.atomic():
				models.monitor_host.objects.filter(ip=ip.get('ip')).update(on_line=on_line)
				models.monitor_stat.objects.create(ip=ip.get('ip'),cpu=0,meminfo=0,diskinfo=0,netinfo=0,create_at=create_at)
	except Exception as e:
		print(e)
		# with open('/home/log','a',encoding='utf-8') as f:
		# 	f.write(e)
		# 	f.flush()
		# f.close()
