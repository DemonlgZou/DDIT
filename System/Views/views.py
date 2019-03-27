from django.shortcuts import render, HttpResponse
from db_server import models
from DDIT import Paging,FROM,imortdb_data
from DDIT.ddit_plugins import auth, menu_list
from System.Views.OS_manager.firewall_manager import open_port,close_port
from System.Views.OS_manager.AC_manager import *
from System.Views.OS_manager.vm_manager import VmManger
import json, datetime,uuid,threading
from DDIT.ddit_plugins import auth, menu_list, search_rules, Fliter_1, Fliter_2  #导入插件



	
	



@auth
def firewall_open_port(request):
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


@auth
def firewall_close_port(request):
	#关闭防火墙端口的方法
	if request.is_ajax():
		#print(request.POST.get('id'))
		open_port = models.open_port.objects.get(id=request.POST.get('id'))
		#print(open_port.rule_name)
		if open_port:
			rule_name = open_port.rule_name
			res = close_port('192.168.254.248','admin','DDit#20020607!',rule_name)
			if res:
				models.open_port.objects.filter(rule_name=rule_name).update(on_line='关闭')
				models.log_system_info.objects.create(action_type='移除', host='192.168.254.248',
				                                      opeater=request.session.get('user'), type='关闭外网访问',
				                                      info='nat server %s ' % (
				                                      rule_name))
				
				return HttpResponse(json.dumps({'ok': '端口已关闭'}), content_type="application/json")
			else:
				return HttpResponse(json.dumps({'ok': '操作异常'}), content_type="application/json")
			
			#return HttpResponse(json.dumps({'ok': rule_name}), content_type="application/json")
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
	#展示主机列表的视图
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
	#展示日志的操作列表
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



def WIFI_Thread(obj_name,obj_agrs,wifi_user_agrs,username):
	#多线程处理删除用户的操作，防止前端出现阻塞。
	# 'proposer'申请人
	# 'dingding_id' 钉钉审批单号
	# 'dept' 部门
	# 'user'  用户名
	# 'pwd'    密码
	# 'user_type': 用户类型 1代表员工 其他代表访客
	# 'mode': 授权类型 1代表长期 其他代表临时
	# 'max_num'最大在线数
	# 'started_at': 开始时间
	# 'expired_at'超期时间
	# 'desc' 备注
	##obj_name 是操作对应的函数名，obj_agrs是对应函数需要传入的参数列表，wifi_user_agrs是数据库需要写入的参数，username是操作人员的名字
	tmp = threading.Thread(target=obj_name,args=obj_agrs)
	tmp.start()
	
	if obj_name == create_wifi_user:
		expired_at = wifi_user_agrs.get('expired_at') if wifi_user_agrs.get(
			'expired_at') != '' else wifi_user_agrs.get(
			'started_at')
		max_num = wifi_user_agrs.get('max_num') if wifi_user_agrs.get('max_num') != '' else 1
		if wifi_user_agrs.get('mode') != '1':
			
			info = {'proposer':wifi_user_agrs.get('proposer'),'dingding_id':wifi_user_agrs.get('dingding_id'),
			        'dept':wifi_user_agrs.get('dept'),'user':wifi_user_agrs.get('user'),
			        'pwd':wifi_user_agrs.get('pwd'),'user_type':int(wifi_user_agrs.get('user_type')),
			        'mode':int(wifi_user_agrs.get('mode')),'max_num':max_num,
			        'started_at':datetime.datetime.strptime(wifi_user_agrs.get('started_at'),'%Y-%m-%d'),
			        'expired_at':datetime.datetime.strptime(expired_at,'%Y-%m-%d'),
			        'desc':wifi_user_agrs.get('desc'),'operator':username}
			
		else:
			info = {'proposer':wifi_user_agrs.get('proposer'),'dingding_id':wifi_user_agrs.get('dingding_id'),
			        'dept':wifi_user_agrs.get('dept'),'user':wifi_user_agrs.get('user'),
			        'pwd':wifi_user_agrs.get('pwd'),'user_type':int(wifi_user_agrs.get('user_type')),
			        'mode':int(wifi_user_agrs.get('mode')),'max_num':max_num,
			        'started_at':datetime.datetime.strptime(wifi_user_agrs.get('started_at'),'%Y-%m-%d'),
			        'desc':wifi_user_agrs.get('desc'),'operator':username}
		models.WIFI_USERS_LIST.objects.create(**info)
		models.WIFI_OPEARTION_RECORD.objects.create(action='创建用户',opeartor=username,info=obj_agrs)
	
	elif obj_name == detele_wifi_user:
		wifi_obj = models.WIFI_USERS_LIST.objects.get(user=wifi_user_agrs)
		models.WIFI_USERS_LIST.objects.get(user=wifi_obj.user).delete()
		models.WIFI_OPEARTION_RECORD.objects.create(action='删除用户', opeartor=username, info=obj_agrs)
	
	elif obj_name == clean_wifi_user:
		models.WIFI_OPEARTION_RECORD.objects.create(action='强制下线', opeartor=username, info=obj_agrs)

	elif obj_name == create_wifi_guest:
		expired_at = wifi_user_agrs.get('expired_at') if wifi_user_agrs.get(
			'expired_at') != '' else wifi_user_agrs.get(
			'started_at')
		info = {'proposer': wifi_user_agrs.get('proposer'), 'dingding_id': wifi_user_agrs.get('dingding_id'),
		        'dept': wifi_user_agrs.get('dept'), 'user': wifi_user_agrs.get('user'),
		        'pwd': wifi_user_agrs.get('pwd'), 'user_type': int(wifi_user_agrs.get('user_type')),
		        'mode': int(wifi_user_agrs.get('mode')),
		        'started_at': datetime.datetime.strptime(wifi_user_agrs.get('started_at'), '%Y-%m-%d'),
		        'desc': wifi_user_agrs.get('desc'), 'operator': username,expired_at:expired_at}
		models.WIFI_USERS_LIST.objects.create(**info)
		models.WIFI_OPEARTION_RECORD.objects.create(action='创建用户', opeartor=username, info=obj_agrs)
	elif obj_name == change_wifi_pwd:
		 models.WIFI_OPEARTION_RECORD.objects.create(action='重置用户密码',opeartor=username,info=obj_agrs)


@auth
def ADD_WIFI_USER(request):
	#'proposer'申请人
	#'dingding_id' 钉钉审批单号
	#'dept' 部门
	#'user'  用户名
	#'pwd'    密码
	#'user_type': 用户类型 1代表员工 其他代表访客
	#'mode': 授权类型 1代表长期 其他代表临时
	#'max_num'最大在线数
	#'started_at': 开始时间
	#'expired_at'超期时间
	#'desc' 备注
	
	if request.method == 'POST':
		max_num = request.POST.get('max_num') if  request.POST.get('max_num') is request.POST.get('max_num').isalnum else '1'
		if request.POST.get('proposer') == '' :
			return HttpResponse(json.dumps({'ok': '申请人不能为空'}), content_type="application/json")
		elif request.POST.get('dingding_id') == '':
			return HttpResponse(json.dumps({'ok': '审批单号不能为空'}), content_type="application/json")
		elif request.POST.get('dept') == '':
			return HttpResponse(json.dumps({'ok': '部门不能为空'}), content_type="application/json")
		elif request.POST.get('user') == '':
			return HttpResponse(json.dumps({'ok': '用户名'}), content_type="application/json")
		elif request.POST.get('pwd') == '':
			return HttpResponse(json.dumps({'ok': '密码不能为空'}), content_type="application/json")
		elif int(max_num) < 1 or int(max_num) > 10:
			return HttpResponse(json.dumps({'ok': '最大允许在线人数10人'}), content_type="application/json")
		else:
			if request.POST.get('started_at') == '':
						return HttpResponse(json.dumps({'ok': '授权时间不能为空'}), content_type="application/json")
			else:
				start = datetime.datetime.strptime(request.POST.get('started_at'),'%Y-%m-%d')
				expired_at = request.POST.get('expired_at') if request.POST.get('expired_at') != '' else request.POST.get('started_at')
				if datetime.datetime.strptime(expired_at, '%Y-%m-%d') < start :
					return HttpResponse(json.dumps({'ok': '授权结束时间不能小于开始时间'}), content_type="application/json")
				if request.POST.get('user_type') == '1' :
						WIFI_Thread(create_wifi_user,
						            (request.POST.get('user'), request.POST.get('pwd'), request.POST.get('max_num'),),
						            request.POST, request.session.get('user'))
						return HttpResponse(json.dumps({'ok': '正在创建无线用户，请稍后！！！'}), content_type="application/json")
					
				else:
						WIFI_Thread(create_wifi_guest,(request.POST.get('user'), request.POST.get('pwd'),request.POST.get('started_at'),expired_at,),request.POST, request.session.get('user'))
						#return HttpResponse(json.dumps({'ok': '暂不支持访客模式！！！'}), content_type="application/json")
						return HttpResponse(json.dumps({'ok': '正在创建无线用户，请稍后！！！'}), content_type="application/json")
	return render(request,'ADD_WIFI_USER.html',menu_list(request))
	


@auth
def wifi_user_list(request):
	#print(request.session['user'])
	#无线用户记录表
	# user_type 1代表是正常用户,2代表是guest用户,
	# mode 1代表是长期用户,2代表是临时用户
	
	# models.WIFI_USERS_LIST.objects.create(user='jiangbenle',
	#                                       user_type=1,
	#                                       max_num=2,
	#                                       mode=1,
	#                                       proposer='蒋本乐',
	#                                       dept='总经理-总经办',
	#                                       operator='demonlg',
	#                                       dingding_id='',
	
	#
	#                                      )
	if request.method == 'GET':
		return render(request,'wifi_user_list.html',menu_list(request))
	elif request.is_ajax():
		if request.method == 'POST':
			
			#正常查询
			if request.POST.get('_search',None) == 'false':
				obj = models.WIFI_USERS_LIST.objects.all().order_by('id')
				res = Paging.page_list(request, obj)
				rows = []
				for i in res.get('data'):
					tmp = {}
					mode = '长期' if i.mode == 1 else '临时'
					user_type = '公司员工' if i.user_type == 1 else '访客'
					expired_at = i.expired_at.strftime('%Y-%m-%d') if i.expired_at else None
					started_at = i.started_at.strftime('%Y-%m-%d') if i.started_at else None
					tmp.update({'id': i.id, 'user': i.user, 'mode': mode, 'user_type': user_type,
					            'operator': i.operator,'expired_at':expired_at,
					            'started_at': started_at,'max_num':i.max_num,
					            'dingding_id': i.dingding_id, 'created_at': (i.created_at).strftime('%Y-%m-%dT%H:%M:%S'),
					            'updated_at': (i.updated_at).strftime('%Y-%m-%dT%H:%M:%S'),'proposer':i.proposer,'dept':i.dept})
					rows.append(tmp)
				data = {'page': res.get('page'),
				        'total': res.get('last'),
				        'records': res.get('records'), 'rows': rows}
				return HttpResponse(json.dumps(data), content_type="application/json")
			elif request.POST.get('_search', None) == 'true':
				####等于、不等于 属于 不属于类的 模糊查询  ####
				if request.POST.get('searchOper') in search_rules.get('rules1'):
					obj = Paging.page_list(request, Fliter_1(request, models.WIFI_USERS_LIST.objects))
				###### id字段下的 大于、小于 不小于、不大于的模糊查询#####
				elif request.POST.get('searchField') == 'id' and request.POST.get('searchOper') in search_rules.get(
						'rules2'):
					obj = Paging.page_list(request, Fliter_2(request, models.WIFI_USERS_LIST.objects))
					#print(obj)
				elif request.POST.get('searchOper') in search_rules.get('rules3'):
					####后续调整
					pass
				res = obj
				rows = []
				for i in res.get('data'):
					tmp = {}
					mode = '长期' if i.mode == 1 else '临时'
					user_type = '公司员工' if i.user_type == 1 else '访客'
					expired_at = i.expired_at.strftime('%Y-%m-%d') if i.expired_at else None
					started_at = i.started_at.strftime('%Y-%m-%d') if i.started_at else None
					tmp.update({'id': i.id, 'user': i.user, 'mode': mode, 'user_type': user_type,
					            'operator': i.operator,'expired_at':expired_at,
					            'started_at': started_at,'max_num':i.max_num,
					            'dingding_id': i.dingding_id, 'created_at': (i.created_at).strftime('%Y-%m-%dT%H:%M:%S'),
					            'updated_at': (i.updated_at).strftime('%Y-%m-%dT%H:%M:%S'),'proposer':i.proposer,'dept':i.dept})
					rows.append(tmp)
				data = {'page': res.get('page'),
				        'total': res.get('last'),
				        'records': res.get('records'), 'rows': rows}
				return HttpResponse(json.dumps(data), content_type="application/json")
			
			
	return render(request,'wifi_user_list.html',menu_list(request))

@auth
def DELETE_WIFI_USER(request):
   #删除WiFi用户信息
	if request.is_ajax():
		if request.method == 'POST':
			try:
				wifi_user = models.WIFI_USERS_LIST.objects.get(id=request.POST.get('data')).user
				WIFI_Thread(detele_wifi_user,
				            (wifi_user,),
				            wifi_user, request.session['user'])
				return HttpResponse(json.dumps({'ok': '删除中，请稍后！！！'}), content_type="application/json")
			except Exception as e:
				return HttpResponse(json.dumps({'ok': f'程序出错,{e}'}), content_type="application/json")

@auth
def CLEAN_WIFI_USER(request):
   #强制用户下线
	if request.is_ajax():
		if request.method == 'POST':
			print(request.POST)
			wifi_user = models.WIFI_USERS_LIST.objects.get(id=request.POST.get('data')).user
			print(wifi_user)
			try:
				WIFI_Thread(clean_wifi_user,
				            (wifi_user,),
				            wifi_user, request.session.get('user'))
				return HttpResponse(json.dumps({'ok': '正在强制用户下线，请稍后！！！'}), content_type="application/json")
			except Exception as e:
				return HttpResponse(json.dumps({'ok': f'程序出错,{e}'}), content_type="application/json")

@auth
def wifi_changepassword(request):
	#修改用户密码
	if request.is_ajax():
		if request.method == 'POST':
			try:
				WIFI_Thread(change_wifi_pwd,(request.POST.get('user'),request.POST.get('pwd'),),request.POST,request.session.get('user'))
				return HttpResponse(json.dumps({'ok': '修改密码成功！！！'}), content_type="application/json")
			except Exception as e:
				return HttpResponse(json.dumps({'ok': f'程序出错,{e}'}), content_type="application/json")
	return render(request,'wifi_changepasswd.html',menu_list(request))


@auth
def OPEN_SW_PORT(request):
	return render(request,'OPEN_SW_PORT.html',menu_list(request))
	
	
	
@auth
def wifi_log(request):
	#wifi用户管理操作记录
	if request.is_ajax():
		if request.method == 'POST':
			if request.POST.get('_search',None) == 'false':
				obj = models.WIFI_OPEARTION_RECORD.objects.all().order_by('id')
				res = Paging.page_list(request, obj)
				rows = []
				for i in res.get('data'):
					tmp = {}
					
					tmp.update({'id': i.id, 'action': i.action, 'opeartor': i.opeartor,
					            'info': i.info,'created_at': (i.created_at).strftime('%Y-%m-%dT%H:%M:%S')})
					rows.append(tmp)
				data = {'page': res.get('page'),
				        'total': res.get('last'),
				        'records': res.get('records'), 'rows': rows}
				return HttpResponse(json.dumps(data), content_type="application/json")
	return render(request,'wifi_log.html',menu_list(request))