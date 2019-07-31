import time,pymysql,subprocess,re
from xml.etree import ElementTree

'''虚拟主机运行状态类型：
case 1: // running
case 2: //blocked
case 3: // paused    虚拟机处于暂停状态
case 4: //shut down  虚拟机在关闭过程中
case 5: // shut off  虚拟机已经关闭
case 6: // crashed   虚拟机已经崩溃
case 7: // suspended 挂起一个正在运行的虚拟机
default: // none
'''

class KVM_Manger(object):
	def __init__(self, ip,user=None,type=None,*args, **kwargs):
		self.ip = ip
		login_name = user if user !=None and user else 'root'
		if type == 'tcp':
			self.conn = libvirt.open(f'qemu+tcp://{login_name}@{self.ip}/system')
		else:
			self.conn = libvirt.open(f'qemu+ssh://{login_name}@{self.ip}/system')
		self.vm_ip_list ={}
		c = subprocess.Popen('ssh root@%s "cat /proc/net/arp"'%self.ip,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		for i in c.stdout.read().decode('utf-8').splitlines():
			d = i.split(" ")
			
			if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$",d[0])and  re.match(r"^\s*([0-9a-fA-F]{2,2}:){5,5}[0-9a-fA-F]{2,2}\s*$", d[23]) :
				tmp_dict = {d[23]:{'vm_ip':d[0],'ip':self.ip}}
				self.vm_ip_list.update(tmp_dict)
	
	
	
	def get_host_obj(self,hostname):
        #根据提供的物理机名称返回该虚拟机的对象信息
		host_obj = self.conn.lookupByName(hostname)
		return host_obj

	def get_all_host_name(self):
    		#获取该物理机下所有虚拟机的名称
			host_list = []
			for i in self.conn.listAllDomains():
				host_list.append(i.name())
			return host_list


	def get_host_info(self,hostname):
    	#获取机器最大CPU，最大内容以及运行状态数据
		res = self.get_host_obj(hostname)
		#print(res.info())
		return {'status':res.info()[0],'Max_memoinfo':res.info()[1],'Max_Cpus':res.info()[3],'Cpu_times':res.info()[-1]}


	def get_host_disk(self,hostname):
    		#获取磁盘相关数据
			Max_total_disk = 0
			Use_total_disk = 0
			disk_info = {'Max_total':Max_total_disk,'use_total':Use_total_disk}
			res = self.get_host_obj(hostname)
			tree = ElementTree.fromstring(res.XMLDesc())
			devices = tree.findall('devices/disk/target')
			for disk in devices:
				device = disk.get('dev')
				try:
					devstat = res.blockInfo(device)
					disk_num = float(devstat[0])/1024/1024/1024
					use_num = float(devstat[1])/1024/1024/1024
					if disk_num >10.0:
						disk_info.update({device:{'total':disk_num,'use':use_num,'pct':use_num/disk_num}})
						Max_total_disk += (int(disk_num))
						Use_total_disk += (int(use_num))
				except Exception as e:
					pass
					#print(e)
			disk_info['Max_total'] = Max_total_disk
			disk_info['use_total'] = Use_total_disk
			disk_info['pct'] = disk_info['use_total']/disk_info['Max_total']
			return disk_info

	def get_disk_io(self,hostname):
    		pass


	def get_cpu_in_use(self,hostname):
       #获取虚拟机CPU使用率
		res =self.get_host_obj(hostname)
		t1 = time.time()
		c1 = int (res.info()[4])
		time.sleep(1);
		t2 = time.time();
		c2 = int (res.info()[4])
		c_nums = int (res.info()[3])
		usage = (c2-c1)*100/((t2-t1)*c_nums*1e9)
		#print (f"{res.name()} Cpu usage {usage}")
		return usage

	def get_memoinfo_in_use(self,hostname):
    		#获取虚拟机内存使用率
		try:
			error_message = '系统没有安装驱动,请安装驱动'
			res = self.get_host_obj(hostname)
			res.memoryStats()
			unused = res.memoryStats().get('unused',None)
			if unused != None:
				free_mem = float(unused)
				total_mem = float(res.memoryStats()['available'])
				#print(((total_mem - free_mem) / total_mem) * 100)
				return (((total_mem - free_mem) / total_mem) * 100)
			else:
		         return '-1'
		except Exception as e:
			   #print({'error':e})
				return {'error':e}
		
	def get_network_in_user(self,hostname):
    		#获取虚拟机网络吞吐情况
				pass
				res = self.get_host_obj()

	def get_host_ip(self,hostname):
		res =  self.get_host_obj(hostname)
		tree = ElementTree.fromstring(res.XMLDesc())
		devices = tree.find('devices/interface/mac')
		mac_address = (devices.get('address'))
		#print(mac_address,hostname)
		
		res = (self.vm_ip_list.get(mac_address)) if (self.vm_ip_list.get(mac_address)) is not None  else False
		return res

# db = pymysql.connect("192.168.0.26","root","1qaz2wsx","tmp" )
# cursor = db.cursor()

# ###获取虚拟机IP地址,主机名,操作系统类型,状态,虚拟化类型,最大CPU数,最大内存,最大磁盘,宿主机器ip,服务器类型
# true_server_list = ['192.168.0.242',]
# t = 0
# for i in true_server_list:
# 	a = KVM_Manger(i)
# 	host_name = a.get_all_host_name()
# 	print(a.vm_ip_list)
# 	for host in host_name:
# 		#print(host)
# 		host_server = a.get_host_obj(host).OSType()
# 		host_name = a.get_host_obj(host).name()
# 		# print(host_name)
# 		host_status = a.get_host_obj(host).isActive()
# 		# print(host_status)
# 		host_Max_cpus = a.get_host_info(host).get('Max_Cpus')
# 		host_Max_menminfo =int( a.get_host_info(host).get('Max_memoinfo'))/1024/1024
# 		host_Max_diskinfo = a.get_host_disk(host).get('Max_total')
# 		true_server = i
# 		# host_OS =
# 	#	print(host_Max_cpus)
# 		ff =list( a.get_host_ip(host).values())
# 		print(ff)
# 		host_ip = ff[0].get('vm_ip')if ff[0] else ''

# 		# print('--------------')
# 		#print(host_ip)
# 		# print(host_name)
# 		# print(host_status)
# 		# print(host_server)
# 	#	print(host_Max_cpus)
# 		# print(host_Max_menminfo)
# 		# print(host_Max_diskinfo)
# 		# print(true_server)
# 		# print('--------------')
# 		if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$",host):
# 			sql = f'update ddit_server_info set IP="{host_name}" where true_server="192.168.0.242" and name = "{host_name}"'
# 			# sql = f'''insert into ddit_server_info (name,IP,status,type,true_server,Max_cpus,Max_disk,Max_meminfo,create_at,update_at)
# 			# values("{host_name}","{host_ip}","{host_status}","{host_server}","{true_server}","{host_Max_cpus}","{host_Max_diskinfo}","{host_Max_menminfo}","2017-03-02 16:34","2017-03-02 16:34")'''
# 			try:
# 				print(sql)
# 				cursor.execute(sql)
# 				db.commit()
# 				print(111)
# 			except Exception as e:
# 				db.rollback()
# 				print(e)
# 			t += 1

# print(t)
# db.close()