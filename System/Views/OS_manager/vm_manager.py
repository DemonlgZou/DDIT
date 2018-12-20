import os,json,requests,psutil,datetime,socket,schedule


def listen():
	meninfo =psutil.virtual_memory()
	cpu = psutil.cpu_percent(interval=1)
	created_time = datetime.datetime.now()
	
	disk = psutil.disk_partitions()
	#print(disk)
	full_disk = ''
	for i in disk:
		try:
	
			#print(psutil.disk_usage(i.mountpoint).percent)
			full_disk += str(psutil.disk_usage(i.mountpoint).percent)+','
	
		except PermissionError:
			pass
	
	
	
	
	name = socket.getfqdn(socket.gethostname(  ))
	ip = socket.gethostbyname(name)
	#获取本机ip
	
	info = {'enctype': 'multipart/form-data','meninfo':meninfo.percent,'cpu':cpu,'disk':full_disk,'created_time':created_time.strftime('%Y-%m-%d %H:%M:%S'),'ip':ip,'name':name}
	
	url = 'http://192.168.100.233:8000/system_manager/revice_info'
	res = requests.post(url,data=info,)


try:

	schedule.every(60).seconds.do(listen)
	while True:
		schedule.run_pending()
		
except Exception as e:
	
	pass

