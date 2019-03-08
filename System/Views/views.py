from django.shortcuts import render, HttpResponse
from db_server import models
from DDIT import Paging,FROM,imortdb_data
from DDIT.ddit_plugins import auth, menu_list
from System.Views.OS_manager.firewall_manager import open_port
from System.Views.OS_manager.vm_manager import VmManger
import json, datetime,uuid,threading
from DDIT.ddit_plugins import auth, menu_list, search_rules, Fliter_1, Fliter_2




@auth
def firewall(request):
	#远程开通外网访问权限的方法
	if request.is_ajax():
		obj = FROM.firewall_port(request.POST)
		if obj.is_valid():
			for i in ['Dialer0','Dialer1','Dialer2']:
				rule_name = str(uuid.uuid1()).replace('-','')
				res = open_port('192.168.254.248','admin','DDit#20020607!',rule_name,
				                request.POST.get('type'),i,str(request.POST.get('outside_port')),
				                request.POST.get('host_ip'),str(request.POST.get('inside_port')))
				if res:
					obj.cleaned_data.update({'rule_name':rule_name,'interface':i})
					models.open_port.objects.create(**obj.cleaned_data)
					models.log_system_info.objects.create(action_type='新增',host='192.168.254.248',opeater=request.session.get('user'),type='开通外网访问',
					                                      info='nat server %s protocol %s global interface %s %s inside %s  %s no-reverse' % (rule_name,request.POST.get('type'),
					                                                                                                                          i,str(request.POST.get('outside_port')),request.POST.get('host_ip'),str(request.POST.get('inside_port'))))
			return HttpResponse(json.dumps({'ok': '端口已开通'}), content_type="application/json")
		else:
			return HttpResponse(json.dumps({'ok': 'pk'}), content_type="application/json")
	return render(request, 'port.html', menu_list(request))



def close_port(request):
	#关闭防火墙端口的方法
	if request.is_ajax():
		print(request.POST.get('id'))
		open_port = models.open_port.objects.get(id=request.POST.get('id'))
		print(open_port.rule_name)
		if open_port:
			rule_name = open_port.rule_name
			# res = close_port('192.168.254.248','admin','DDit#20020607!',rule_name)
			# if res:
			# 	models.log_system_info.objects.create(action_type='移除', host='192.168.254.248',
			# 	                                      opeater=request.session.get('user'), type='关闭外网访问',
			# 	                                      info='nat server %s ' % (
			# 	                                      rule_name))
			#	return HttpResponse(json.dumps({'ok': '端口已关闭'}), content_type="application/json")
			#else:
			#	return HttpResponse(json.dumps({'ok': 'pk'}), content_type="application/json")
			
			return HttpResponse(json.dumps({'ok': rule_name}), content_type="application/json")
	return render(request, 'port.html', menu_list(request))




@auth
def firewall_list(request):
	#展示已开通外网端口的方法
	if request.method == 'POST':
		if request.POST.get('_search', None) == 'false':
			obj = models.open_port.objects.all().order_by('id')
			res = Paging.page_list(request, obj)
			rows = []
			for i in res.get('data'):
				tmp = {}
				tmp.update({
					'id': i.id,
					'rule_name': i.rule_name,
					'host_ip': i.host_ip,
					'type': i.type,
					'dept': i.dept,
					'inside_port': i.inside_port,
					'outside_port': i.outside_port,
					'interface': i.interface,
					'proposer': i.proposer,
					'start_time': i.start_time.strftime('%Y-%m-%d'),
					'end_time': i.end_time.strftime('%Y-%m-%d')if i.end_time else None,
					'on_line': i.on_line,
					'desc':i.desc,
					'create_at': i.create_at.strftime('%Y-%m-%dT%H:%M:%S'),
					'update_at': i.update_at.strftime('%Y-%m-%dT%H:%M:%S'),
				})
				rows.append(tmp)
			data = {'page': res.get('page'),
				        'total': res.get('last'),
				        'records': res.get('records'), 'rows': rows}
			
			return HttpResponse(json.dumps(data), content_type="application/json")
		elif request.POST.get('_search', None) == 'true':
			if request.POST.get('searchOper') in search_rules.get('rules1'):
				obj = Paging.page_list(request, Fliter_1(request, models.open_port.objects))
			elif request.POST.get('searchField') == 'id' and request.POST.get('searchOper') in search_rules.get(
					'rules2'):
				obj = Paging.page_list(request, Fliter_2(request, models.open_port.objects))
			elif request.POST.get('searchOper') in search_rules.get('rules3'):
				####后续调整
				pass
			res = obj
			rows = []
			for i in res.get('data'):
				tmp = {}
				tmp.update({
					'id': i.id,
					'rule_name': i.rule_name,
					'host_ip': i.host_ip,
					'type': i.type,
					'dept': i.dept,
					'inside_port': i.inside_port,
					'outside_port': i.outside_port,
					'interface': i.interface,
					'proposer': i.proposer,
					'start_time': i.start_time.strftime('%Y-%m-%d'),
					'end_time': i.end_time.strftime('%Y-%m-%d')if i.end_time else None,
					'on_line': i.on_line,
					'desc':i.desc,
					'create_at': i.create_at.strftime('%Y-%m-%dT%H:%M:%S'),
					'update_at': i.update_at.strftime('%Y-%m-%dT%H:%M:%S'),
				})
				rows.append(tmp)
			data = {'page': res.get('page'),
			        'total': res.get('last'),
			        'records': res.get('records'), 'rows': rows}
			return HttpResponse(json.dumps(data), content_type="application/json")
	return render(request, 'port_list.html', menu_list(request))


@auth
def vm(request):
	#创建虚拟机方法
	if request.method == "POST":
		pass
	return render(request, 'create_host.html', menu_list(request))


@auth
def host_list(request):
	if request.method == 'POST':
		obj = models.Server_info.objects.all().order_by('id')
		res = Paging.page_list(request, obj)
		rows = []
		for i in res.get('data'):
			tmp = {}
			tmp.update({'id': i.id, 'name': i.name, 'IP': i.IP, 'server': i.server, 'OS': i.OS, 'desric': i.desric,
			            'status': i.status, 'create_at': (i.create_at).strftime('%Y-%m-%dT%H:%M:%S'),
			            'update_at': (i.update_at).strftime('%Y-%m-%dT%H:%M:%S')})
			rows.append(tmp)
		data = {'page': res.get('page'),
		        'total': res.get('last'),
		        'records': res.get('records'), 'rows': rows}
		return HttpResponse(json.dumps(data), content_type="application/json")
	return render(request, 'host_list.html', menu_list(request))




@auth
def log(request):
	if request.is_ajax():
		if request.method == 'POST':
			obj = models.log_system_info.objects.all().order_by('id')
			res = Paging.page_list(request, obj)
			rows = []
			for i in res.get('data'):
				tmp = {}
				tmp.update(
					{'id': i.id, 'action_type': i.action_type,
					 'opeater':i.opeater, 'create_at': (i.create_at).strftime('%Y-%m-%dT%H:%M:%S'),
					 'type':i.type,'info':i.info,'host':i.host})
				rows.append(tmp)
			data = {'page': res.get('page'),
			        'total': res.get('last'),
			        'records': res.get('records'), 'rows': rows}
	        
			return HttpResponse(json.dumps(data), content_type="application/json")
	
	return render(request,'log.html',menu_list(request))




@auth
def monitoring_list(request):
	if request.method == 'GET':
		return render(request,'monitoring_list.html',menu_list(request))
	elif request.is_ajax():
		if request.method == 'POST':
			obj = models.monitor_host.objects.all().order_by('id')
			res = Paging.page_list(request, obj)
			rows = []
			for i in res.get('data'):
				stat = models.monitor_stat.objects.filter(ip=i.ip).last()
				tmp = {}
				if stat:
					tmp.update({'id': i.id, 'name': i.name, 'IP': i.ip, 'cpu':  stat.cpu if stat.cpu else '-' ,
					            'meminfo': stat.meminfo if stat.meminfo else '-', 'diskinfo': stat.diskinfo  if stat.diskinfo else '-' ,
					            'on_line':i.on_line,'user':i.user,'create_at': (stat.create_at).strftime('%Y-%m-%dT%H:%M:%S'),
					            'update_at': (i.update_at).strftime('%Y-%m-%dT%H:%M:%S')})
				else:
					tmp.update({'id': i.id, 'name': i.name, 'IP': i.ip, 'cpu': '-',
					            'meminfo': '-',
					            'diskinfo':  '-',
					            'on_line': i.on_line, 'user': i.user,
					            #'create_at': (stat.create_at).strftime('%Y-%m-%dT%H:%M:%S'),
					            'update_at': (i.update_at).strftime('%Y-%m-%dT%H:%M:%S')})
				rows.append(tmp)
			data = {'page': res.get('page'),
			        'total': res.get('last'),
			        'records': res.get('records'), 'rows': rows}
			return HttpResponse(json.dumps(data), content_type="application/json")
	
	
	
	

def add_monitor_host(request):
	if request.method =='GET':
		return render(request,'add_monitor_host.html',menu_list(request),)
	elif request.is_ajax():
		return render(request, 'add_monitor_host.html', menu_list(request), )



	


@auth
def vm_start(request):
	#虚拟机启动的API
	if request.method == 'POST':
		if request.POST.get('action') == 'start':
			#print(request.POST.get('data'))
			tmp = models.Server_info.objects.get(id=request.POST.get('data'))
			#print(tmp.IP)
			obj = models.monitor_host.objects.get(ip=tmp.IP)
			user = obj.user
			pwd = obj.pwd
			#print(user,pwd,tmp.true_server,tmp.type)
			# test = VmManger(tmp.IP,22,'root','DDitTAXrefund241','Y')
			# test.start()
			return HttpResponse(json.dumps({'data':'123'}), content_type="application/json")


@auth
def vm_reboot(request):
	#虚拟机重启的API
	if request.method == 'POST':
		return HttpResponse('ok')



@auth
def vm_shutdown(request):
	#虚拟机关闭的API
	if request.method == 'POST':
		return HttpResponse('ok')




@auth
def vm_manager(request):
	#虚拟机或者容器的管理视图
	if request.method == 'POST':
		obj = models.Server_info.objects.filter(server__in=['虚拟机','容器']).order_by('id')
		res = Paging.page_list(request, obj)
		rows = []
		for i in res.get('data'):
			tmp = {}
			status = models.monitor_host.objects.get(ip=i.IP).on_line
			tmp.update({'id': i.id, 'name': i.name, 'IP': i.IP, 'server': i.server, 'OS': i.OS,
			            'status': status, 'create_at': (i.create_at).strftime('%Y-%m-%dT%H:%M:%S'),
			            'update_at': (i.update_at).strftime('%Y-%m-%dT%H:%M:%S')})
			rows.append(tmp)
		data = {'page': res.get('page'),
		        'total': res.get('last'),
		        'records': res.get('records'), 'rows': rows}
		return HttpResponse(json.dumps(data), content_type="application/json")
	return render(request,'vm_list.html',menu_list(request))


@auth
def ADD_WIFI_USER(request):
	return render(request,'ADD_WIFI_USER.html',menu_list(request))


@auth
def OPEN_SW_PORT(request):
	return render(request,'OPEN_SW_PORT.html',menu_list(request))
