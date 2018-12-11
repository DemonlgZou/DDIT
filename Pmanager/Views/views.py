from django.shortcuts import render, HttpResponse
from db_server import models
import xlrd, datetime, json, time
from DDIT import Paging
from django.db.utils import *
from DDIT.ddit_plugins import auth, menu_list, search_rules, Fliter_1, Fliter_2
from DDIT.imortdb_data import *
from DDIT import FROM
import  datetime
@auth
def pm_list(request):
	#####项目相关内容列表
	if request.method == 'POST':
		if request.POST.get('_search', None) == 'false':
			obj = models.PM_list.objects.all().order_by('id')
			res = Paging.page_list(request, obj)
			rows = []
			for i in res.get('data'):
				tmp = {}
				date_time = i.date_time if i.date_time else None
				tmp.update({'id': i.id, 'contract_id': i.contract_id, 'contract_start': i.contract_start,
				            'contract_end': i.contract_end,
				            'price': i.contract_price,
				            'contract_work':i.contract_work,
				            'contract_price':i.contract_price,
				            'pid': i.pid,
				            'Manage': i.Manage,
				            'operator': i.operator,
				            'manager': i.manager,
				            'step': i.step,
				            'date_time': date_time,
				            'father_name': i.father_name,
				            'child_name': i.child_name,
				            'desc' : i.desc,
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
				obj = Paging.page_list(request, Fliter_1(request, models.PM_list.objects))
			
			
			###### id字段下的 大于、小于 不小于、不大于的模糊查询#####
			elif request.POST.get('searchField') == 'id' and request.POST.get('searchOper') in search_rules.get(
					'rules2'):
				obj = Paging.page_list(request, Fliter_2(request, models.PM_list.objects))
			
			
			elif request.POST.get('searchOper') in search_rules.get('rules3'):
				####后续调整
				pass
			res = obj
			rows = []
			for i in res.get('data'):
				tmp = {}
				date_time = i.date_time if i.date_time else None
				tmp.update({'id': i.id, 'contract_id': i.contract_id, 'contract_start': i.contract_start,
				            'contract_end': i.contract_end,
				            'price': i.contract_price,
				            'contract_work': i.contract_work,
				            'contract_price': i.contract_price,
				            'pid': i.pid,
				            'Manage': i.Manage,
				            'operator': i.operator,
				            'manager': i.manager,
				            'step': i.step,
				            'date_time': date_time,
				            'father_name': i.father_name,
				            'child_name': i.child_name,
				            'desc': i.desc,
				            'create_at': i.create_at.strftime('%Y-%m-%dT%H:%M:%S'),
				            'update_at': i.update_at.strftime('%Y-%m-%dT%H:%M:%S'),
				            })
				rows.append(tmp)
			data = {'page': res.get('page'),
			        'total': res.get('last'),
			        'records': res.get('records'), 'rows': rows}
			return HttpResponse(json.dumps(data), content_type="application/json")
		
		
		
		elif request.POST.get('oper', None) == 'edit':
			info = {
				'contract_id':request.POST.get('contract_id'),
				'contract_start':request.POST.get('contract_start'),
				'contract_end':request.POST.get('contract_end'),
				'contract_price':request.POST.get('contract_price'),
				'contract_work':request.POST.get('contract_work'),
				'pid':request.POST.get('pid'),
				'Manage':request.POST.get('Manage'),
				'operator':request.POST.get('operator'),
				'manager':request.POST.get('manager'),
				'step':request.POST.get('step'),
				'date_time':request.POST.get('date_time'),
				'father_name':request.POST.get('father_name'),
				'child_name':request.POST.get('child_name'),
				'desc':request.POST.get('desc'),}
			models.PM_list.objects.filter(id=request.POST.get('id')).update(**info)
		elif request.POST.get('oper', None) == 'del':
			
				a = models.period.objects.filter(no_id=request.POST.get('id'))
				if a:
					a.delete()
				
				b =models.Work_hours.objects.filter(item_id=request.POST.get('id'))
				if b:
					b.delete()
				models.PM_list.objects.filter(id=request.POST.get('id'))
				
	return render(request, 'project_list.html', menu_list(request))


@auth
def pm_work(request):
	#####人力工时相关信息
	if request.method == 'POST':
		
		# 正常数据分页查询返回数据#
		if request.POST.get('_search', None) == 'false':
			obj = models.Work_hours.objects.all().order_by('id')
			res = Paging.page_list(request, obj)
			rows = []
			for i in res.get('data'):
				tmp = {}
				tmp.update({'id': i.id,
				            'name': i.item.father_name,
				            'type': i.item.child_name,
				            'arr1': i.arr1,
				            'arr2': i.arr2,
				            'arr3': i.arr3,
				            'arr4': i.arr4,
				            'arr5': i.arr5,
				            'arr6': i.arr6,
				            'arr7': i.arr7,
				            'arr8': i.arr8,
				            'arr9': i.arr9,
				            'arr10': i.arr10,
				            'arr11': i.arr11,
				            'arr12': i.arr12,
				            'date': i.date,
				            'create_at': i.create_at.strftime('%Y-%m-%dT%H:%M:%S'),
				            'update_at': i.update_at.strftime('%Y-%m-%dT%H:%M:%S')})
				rows.append(tmp)
			data = {'page': res.get('page'),
			        'total': res.get('last'),
			        'records': res.get('records'), 'rows': rows}
			return HttpResponse(json.dumps(data), content_type="application/json")
		
		# 编写信息内容数据
		elif request.POST.get('oper', None) == 'edit':
			arr1 = request.POST.get('arr1')
			arr2 = request.POST.get('arr2')
			arr3 = request.POST.get('arr3')
			arr4 = request.POST.get('arr4')
			arr5 = request.POST.get('arr5')
			arr6 = request.POST.get('arr6')
			arr7 = request.POST.get('arr7')
			arr8 = request.POST.get('arr8')
			arr9 = request.POST.get('arr9')
			arr10 = request.POST.get('arr10')
			arr11 = request.POST.get('arr11')
			arr12 = request.POST.get('arr12')
			date = request.POST.get('date')
			models.Work_hours.objects.filter(id=request.POST.get('id')).update(arr1=float(arr1), arr2=float(arr2),
			                                                                   arr4=float(arr4), arr3=float(arr3),
			                                                                   arr5=float(arr5), arr6=float(arr6),
			                                                                   arr7=float(arr7), arr8=float(arr8),
			                                                                   arr9=float(arr9), arr10=float(arr10),
			                                                                   arr11=float(arr11), arr12=float(arr12),
			                                                                   date=date)
			
			return HttpResponse(json.dumps({'Status': 'success', }))
		
		#####新增数据内容
		elif request.POST.get('oper', None) == 'add':
			models.Company_info.objects.create(name=request.POST.get('name'), contacts=request.POST.get('contacts'),
			                                   Address=request.POST.get('Address'), phone=request.POST.get('phone'),
			                                   bill=request.POST.get('bill'), type=request.POST.get('type'))
			return HttpResponse(json.dumps({'Status': 'success', 'message': 'ok'}))
		
		####匹配查询返回数据信息###
		elif request.POST.get('_search', None) == 'true':
			if request.POST.get('searchOper') in search_rules.get('rules1'):
				
				# 通过项目名查询
				if request.POST.get('searchField') == 'name':
					tmp = models.PM_list.objects.filter(
						father_name=request.POST.get('searchString')).values_list('id', flat=True, )
				
					q1 = models.Q()
					q1.connector = 'OR'
					for i in tmp:
						q1.children.append(('item_id', i))
					obj = models.Work_hours.objects.filter(q1).all()
					
					res = Paging.page_list(request, obj)
					rows = []
					for i in res.get('data'):
						tmp = {}
						tmp.update({'id': i.id,
						            'name': i.item.father_name,
						            'type': i.item.child_name,
						            'arr1': i.arr1,
						            'arr2': i.arr2,
						            'arr3': i.arr3,
						            'arr4': i.arr4,
						            'arr5': i.arr5,
						            'arr6': i.arr6,
						            'arr7': i.arr7,
						            'arr8': i.arr8,
						            'arr9': i.arr9,
						            'arr10': i.arr10,
						            'arr11': i.arr11,
						            'arr12': i.arr12,
						            'date': i.date,
						            'create_at': i.create_at.strftime('%Y-%m-%dT%H:%M:%S'),
						            'update_at': i.update_at.strftime('%Y-%m-%dT%H:%M:%S')})
						rows.append(tmp)
					data = {'page': res.get('page'),
					        'total': res.get('last'),
					        'records': res.get('records'), 'rows': rows}
					return HttpResponse(json.dumps(data), content_type="application/json")
				
				# 通过项目分类查询
				elif request.POST.get('searchField') == 'type':
					tmp = models.PM_list.objects.filter(
						father_name=request.POST.get('searchString')).values_list('id', flat=True, )
					q1 = models.Q()
					q1.connector = 'OR'
					for i in tmp:
						q1.children.append(('item_id', i))
					obj = models.Work_hours.objects.filter(q1).all()
					
				
				# 通过其他字段查询
				else:
					obj = Paging.page_list(request, Fliter_1(request, models.Work_hours.objects))
				
			###### id字段下的 大于、小于 不小于、不大于的模糊查询#####
			elif request.POST.get('searchField') == 'id' and request.POST.get('searchOper') in search_rules.get(
					'rules2'):
				obj = Paging.page_list(request, Fliter_2(request, models.Work_hours.objects))
			elif request.POST.get('searchOper') in search_rules.get('rules3'):
				####后续调整
				pass
			res = obj
			rows = []
			for i in res.get('data'):
				tmp = {}
				tmp.update({'id': i.id,
				            'name': i.item.father_name,
				            'type': i.item.child_name,
				            'arr1': i.arr1,
				            'arr2': i.arr2,
				            'arr3': i.arr3,
				            'arr4': i.arr4,
				            'arr5': i.arr5,
				            'arr6': i.arr6,
				            'arr7': i.arr7,
				            'arr8': i.arr8,
				            'arr9': i.arr9,
				            'arr10': i.arr10,
				            'arr11': i.arr11,
				            'arr12': i.arr12,
				            'date': i.date,
				            'create_at': i.create_at.strftime('%Y-%m-%dT%H:%M:%S'),
				            'update_at': i.update_at.strftime('%Y-%m-%dT%H:%M:%S')})
				rows.append(tmp)
			data = {'page': res.get('page'),
			        'total': res.get('last'),
			        'records': res.get('records'), 'rows': rows}
			return HttpResponse(json.dumps(data), content_type="application/json")
	
	return render(request, 'work-hours_list.html', menu_list(request))


@auth
def pm_add(request):
	#新增项目信息
	if request.method == 'POST':
		f = FROM.add_project(request.POST)
		if f.is_valid():
			data = f.cleaned_data
			# obj = models.PM_list.objects.create(**data)
			# models.period.objects.create(no_id=obj.id)
			# models.Work_hours.objects.create(item_id=obj.id)
			data1 = {'data':'项目创建成功'}
			return HttpResponse(json.dumps(data1), content_type="application/json")
		else:
			 print(f.errors)
			 data1 = {'data':'缺少参数，请确认所有参数都已填写！'}
			 
			 return HttpResponse(json.dumps(data1), content_type="application/json")
		
	return render(request, 'add_project.html', menu_list(request))


@auth
def pm_period(request):
	if request.method == 'POST':
		#####正常查询####
		if request.POST.get('_search', None) == 'false':
			obj = models.period.objects.all().order_by('id')
			res = Paging.page_list(request, obj)
			rows = []
			for i in res.get('data'):
				info = models.PM_list.objects.get(id=i.no_id).pid
				tmp = {'id':i.id,
				       'pid':info,
				       'start_at':i.start_at,
				       'end_at':i.end_at,
				       'name':i.name,
				       'delay':i.delay,
				       'plan_no':i.plan_no,
				       'Evaluation':i.Evaluation,
				       'create_at': i.create_at.strftime('%Y-%m-%dT%H:%M:%S'),
				       'update_at': i.update_at.strftime('%Y-%m-%dT%H:%M:%S')
				       }
				rows.append(tmp)
			data = {'page': res.get('page'),
			        'total': res.get('last'),
			        'records': res.get('records'), 'rows': rows}
			return HttpResponse(json.dumps(data), content_type="application/json")
		elif request.POST.get('oper', None) == 'edit':
			info = {
			'start_at': request.POST.get('start_at'),
			'end_at': request.POST.get('end_at'),
			'name': request.POST.get('name'),
			'delay': request.POST.get('delay'),
			'plan_no': request.POST.get('plan_no'),
			'Evaluation': request.POST.get('plan_no'),}
			
			models.period.objects.filter(id=request.POST.get('id')).update(**info)
		elif request.POST.get('oper', None) == 'add':
			id = models.PM_list.objects.get(pid=request.POST.get('pid'))
			info = {
				'no_id':id.id,
				'start_at': request.POST.get('start_at'),
				'end_at': request.POST.get('end_at'),
				'name': request.POST.get('name'),
				'delay': request.POST.get('delay'),
				'plan_no': request.POST.get('plan_no'),
				'Evaluation': request.POST.get('plan_no'), }
			models.period.objects.create(**info)
		elif request.POST.get('oper', None) == 'del':
			models.period.objects.filter(id=request.POST.get('id')).delete()
		#####匹配查询
		elif request.POST.get('_search', None) == 'true':
			if request.POST.get('searchOper') in search_rules.get('rules1'):
				
				# 通过项编号查询
				if request.POST.get('searchField') == 'pid' :
					tmp = models.PM_list.objects.get(
						pid=request.POST.get('searchString'))
					if request.POST.get('searchOper') == 'eq':
						obj = models.period.objects.filter(no_id=tmp.id).all().order_by('id')
					elif request.POST.get('searchOper') == 'ne':
						obj = models.period.objects.exclude(no_id=tmp.id).all().order_by('id')
					res = Paging.page_list(request, obj)
					rows = []
					for i in res.get('data'):
						tmp = {}
						tmp.update({'id': i.id,
						            'pid': i.no.pid,
						            'name': i.name,
						            'start_at': i.start_at,
						            'end_at': i.end_at,
						            'delay': i.delay,
						           # 'cost1': i.cost1,
						            'plan_no': i.plan_no,
						            'Evaluation': i.Evaluation,
						            'create_at': i.create_at.strftime('%Y-%m-%dT%H:%M:%S'),
						            'update_at': i.update_at.strftime('%Y-%m-%dT%H:%M:%S')})
						rows.append(tmp)
					data = {'page': res.get('page'),
					        'total': res.get('last'),
					        'records': res.get('records'), 'rows': rows}
					return HttpResponse(json.dumps(data), content_type="application/json")
			
			elif request.POST.get('searchField') == 'id' and request.POST.get('searchOper') in search_rules.get(
					'rules2'):
				obj = Paging.page_list(request, Fliter_2(request, models.period.objects))
			
			elif request.POST.get('searchOper') in search_rules.get('rules3'):
				####后续调整
				pass
			res = Paging.page_list(request, obj)
			rows = []
			for i in res.get('data'):
				info = models.period.objects.get(id=i.no_id).father_name
				tmp = {'id':i.id,
				       'father_name':info,
				       'start_at':i.start_at,
				       'end_at':i.end_at,
				       'name':i.name,
				       'delay':i.delay,
				       'plan_no':i.plan_no,
				       'Evaluation':i.Evaluation,
				       'create_at': i.create_at.strftime('%Y-%m-%dT%H:%M:%S'),
				       'update_at': i.update_at.strftime('%Y-%m-%dT%H:%M:%S')
				       }
				rows.append(tmp)
			data = {'page': res.get('page'),
			        'total': res.get('last'),
			        'records': res.get('records'), 'rows': rows}
			return HttpResponse(json.dumps(data), content_type="application/json")
	return render(request, 'period_list.html', menu_list(request))


@auth
def info_list(request,page):
	#项目详情#
	try:
		project_info = models.PM_list.objects.get(id=int(page))
		period_info = models.period.objects.filter(no_id=project_info.id).all().order_by('id')
		obj = {'project_info':project_info,'period_info':period_info}
		data = {'status': 'success', 'code': 200, 'data': obj}
	except ValueError:
		data = {'status': 'success', 'code': 404, 'data': '没有数据'}
	except Exception as e:
		data = {'status': 'error', 'data': e}
	tmp = {'info': data}
	tmp.update(menu_list(request))
	return render(request, 'project_info.html', tmp)
#write_data()