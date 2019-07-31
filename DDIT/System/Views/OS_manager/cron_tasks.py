
from db_server import models
from System.Views.OS_manager import kvm_api
import  logging

ddit_collect = logging.getLogger("collect")
ddit_error = logging.getLogger('error')
def get_host_status(obj):
	''' 服务器状态，服务器CPU使用率,内存使用率，磁盘使用率等
	case
	1: // running
	case
	2: // blocked
	case
	3: // paused
	虚拟机处于暂停状态
	case
	4: // shut
	down
	虚拟机在关闭过程中
	case
	5: // shut
	off
	虚拟机已经关闭
	case
	6: // crashed
	虚拟机已经崩溃
	case
	7: // suspended
	挂起一个正在运行的虚拟机
	default: // none
	'''
	status_dict = {'1':'运行中','2':'阻塞','3':'暂停','4':'关机中','5':'关闭','6':'崩溃','7':'正在挂起','dafault':None}
	try:
		
		for i in obj:
			obj_res = kvm_api.KVM_Manger(i)
			hosts = obj_res.get_all_host_name()
			for t in hosts:
				host_status = obj_res.get_host_info(t).get('status')
				# if host_status == '1':
				host_ip = obj_res.get_host_ip(t)
				if host_status == 1:
					host_cpu_in_use = obj_res.get_cpu_in_use(t)
					host_meminfo_in_use = obj_res.get_memoinfo_in_use(t)
					host_disk_in_use = obj_res.get_host_disk(t).get('pct')
					
				else:
					host_cpu_in_use = '0'
					host_meminfo_in_use = '0'
					host_disk_in_use = '0'
					
				with models.transaction.atomic():

					models.monitor_stat.objects.create(**{'ip':t,"cpu":host_cpu_in_use,"meminfo":host_meminfo_in_use,"diskinfo":host_disk_in_use})
					models.monitor_host.objects.update(on_line=status_dict.get(str(host_status)))
					models.Server_info.objects.update(status=str(host_status))
				
	except Exception as e:
		ddit_error.error(e)
		pass
		


def add_vm_host(obj):
	#
	try:
		for i in obj:
			obj_res = kvm_api.KVM_Manger(i)
			hosts =obj_res.get_all_host_name()
			for t in hosts:
				status = obj_res.get_host_info(t).get('status')
				server = '虚拟机'
				name = t
				type = obj_res.get_host_obj(t).OSType()
				Max_cpus = obj_res.get_host_info(t).get('Max_Cpus')
				Max_menminfo =int( obj_res.get_host_info(t).get('Max_memoinfo'))/1024/1024
				Max_diskinfo = obj_res.get_host_disk(t).get('Max_total')
				true_server = i
				ip = obj_res.get_host_ip(t) if obj_res.get_host_ip(t) else None
				info = {'name':name,'IP':ip,'status':status,'server':server,'type':type,'true_server':true_server,
				        'Max_cpus':Max_cpus,'Max_meminfo':Max_menminfo,'Max_disk':Max_diskinfo}
				with models.transaction.atomic():
					obj = models.Server_info.objects.filter(name=name).first()
					if obj is None:
						models.Server_info.objects.get_or_create(**info)
	except Exception as e:
		ddit_error.error(e)
		pass