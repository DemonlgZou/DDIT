from django.shortcuts import render, HttpResponse
from db_server import models
from DDIT import Paging,FROM
from DDIT.ddit_plugins import auth, menu_list
from System.Views.OS_manager.firewall_manager import open_port
import json, datetime,uuid,threading



@auth
def firewall(request):
	#远程开通外网访问权限的方法
	if request.is_ajax():
		obj = FROM.firewall_port(request.POST)
		if obj.is_valid():
			for i in ['Dialer0','Dialer1']:
				rule_name = str(uuid.uuid1()).replace('-','')
				res = open_port('192.168.254.248','admin','DDit#20020607!',rule_name,
				                request.POST.get('type'),i,str(request.POST.get('outside_port')),
				                request.POST.get('host_ip'),str(request.POST.get('inside_port')))
				if res:
					obj.cleaned_data.update({'rule_name':rule_name,'interface':i})
					models.open_port.objects.create(**obj.cleaned_data)
					models.log_system_info.objects.create(action_type='新增',opeater=request.session.get('user'),type='开通外网访问',
					                                      info='nat server %s protocol %s global interface %s %s inside %s  %s no-reverse' % (rule_name,request.POST.get('type'),
					                                                                                                                          i,str(request.POST.get('outside_port')),request.POST.get('host_ip'),str(request.POST.get('inside_port'))))
			return HttpResponse(json.dumps({'ok': '端口已开通'}), content_type="application/json")
		else:
			#print(obj.errors)
			return HttpResponse(json.dumps({'ok': 'pk'}), content_type="application/json")
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
	return render(request, 'port_list.html', menu_list(request))


@auth
def vm(request):
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



	
def get_client_ip(request):
	try:
		real_ip = request.META['HTTP_X_FORWARDED_FOR']
		regip = real_ip.split(",")[0]
	except:
		try:
			regip = request.META['REMOTE_ADDR']
		except:
			regip = ""

	return regip


def revice_info(request):
	if request.method == 'POST':
		
		return HttpResponse('ok')
	
def vm_manager(request):
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
	