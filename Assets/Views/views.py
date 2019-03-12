from django.shortcuts import render ,HttpResponse,redirect
from db_server import models
import xlrd,datetime ,json
from DDIT import Paging
from DDIT.ddit_plugins import auth,menu_list,search_rules,Fliter_1,Fliter_2



@auth
def supplier(request):
   
     #供应商视图
     
        if request.method == 'POST':
            #增加数据
            if request.POST.get('oper',None) == 'add':
                       models.Company_info.objects.create(name=request.POST.get('name'),contacts=request.POST.get('contacts'),Address=request.POST.get('Address'),phone=request.POST.get('phone'),bill=request.POST.get('bill'),type=request.POST.get('type'))
                       return HttpResponse(json.dumps({'Status': 'success','message':'ok' }))


            #修改数据
            elif request.POST.get('oper',None) == 'edit':
                 models.Company_info.objects.filter(id=request.POST.get('id')).update(
                     name=request.POST.get('name'),
                     contacts=request.POST.get('contacts'),
                      phone=request.POST.get('phone'),
                     
                      Address=request.POST.get('Address'),
                      bill= request.POST.get('bill'),
                      buyer= request.POST.get('type'))
                      
                 return HttpResponse(json.dumps({'Status':'success',}))


            #删除数据
            elif request.POST.get('oper', None) == 'del':
                models.Company_info.objects.filter(id=request.POST.get('id')).delete()
                return HttpResponse(json.dumps({'Status': 'success','message':'ok'  }))



            #正常查询数据
            elif request.POST.get('_search',None) == 'false':
                obj = models.Company_info.objects.all().order_by('id')
                res = Paging.page_list(request, obj)
                rows = []
                for i in res.get('data'):
                    tmp = {}
                    tmp.update({'id':i.id,'name':i.name,'contacts':i.contacts,'phone':i.phone,'type':i.type,'Address':i.Address,'bill':i.bill,'buyer':i.buyer,'create_at':(i.create_at).strftime('%Y-%m-%dT%H:%M:%S'),'update_at':(i.update_at).strftime('%Y-%m-%dT%H:%M:%S')})
                    rows.append(tmp)
                data = {'page': res.get('page'),
                            'total': res.get('last'),
                            'records': res.get('records'), 'rows': rows}
                return HttpResponse(json.dumps(data),content_type="application/json")

            ##匹配搜索
            elif  request.POST.get('_search',None) == 'true':


                          ####等于、不等于 属于 不属于类的 模糊查询  ####
                          if   request.POST.get('searchOper') in search_rules.get('rules1'):
                              obj = Paging.page_list(request, Fliter_1(request, models.Company_info.objects))


                          ###### id字段下的 大于、小于 不小于、不大于的模糊查询#####
                          elif request.POST.get('searchField') == 'id' and request.POST.get('searchOper') in search_rules.get('rules2') :
                              obj = Paging.page_list(request, Fliter_2(request,models.Company_info.objects))



                          elif request.POST.get('searchOper') in search_rules.get('rules3'):
                              ####后续调整
                                         pass

                          res = obj
                          rows = []
                          for i in res.get('data'):
                              tmp = {}
                              tmp.update({'id': i.id, 'name': i.name, 'contacts': i.contacts, 'phone': i.phone,
                                          'type': i.type, 'Address': i.Address, 'bill': i.bill, 'buyer': i.buyer,
                                          'create_at': (i.create_at).strftime('%Y-%m-%dT%H:%M:%S'),
                                          'update_at': (i.update_at).strftime('%Y-%m-%dT%H:%M:%S'),
                                         })
                              rows.append(tmp)
                          data = {'page': res.get('page'),
                                  'total': res.get('last'),
                                  'records': res.get('records'), 'rows': rows}
                          return HttpResponse(json.dumps(data), content_type="application/json")
        return  render(request, 'supplier.html',menu_list(request))






@auth
def in2out(request):
    ###资产入库视图
    #目前没完善入库功能
    if request.method == 'POST':
        #print(request.POST.get('name'))
        return HttpResponse(json.dumps({'status':'success'}), content_type="application/json")
    elif request.method == 'GET':
        obj = models.Company_info.objects.all().order_by('id')
        tmp = {'info':obj}
        tmp.update(menu_list(request))
        return  render(request, 'stock_inquiry.html',tmp)




@auth
def assets(request):
    #固定资产视图
    if request.method == 'POST':
        if request.POST.get('oper', None) == 'edit':
            models.Reserves.objects.filter(id=request.POST.get('id')).update(
            name=request.POST.get('name'),
            asset_No= request.POST.get('no'),
            Type= request.POST.get('type'),
            price= request.POST.get('price'),
            status= request.POST.get('status'),
            company= request.POST.get('company'),
            contacts= request.POST.get('contacts'),
            manger_user = request.POST.get('manger_user'),
            finance_id=request.POST.get('finance_id')
            )

            return HttpResponse(json.dumps({'Status': 'success', }))


        elif request.POST.get('_search', None) == 'false':
            obj = models.Reserves.objects.filter(Type='固定资产').all()
            res = Paging.page_list(request, obj)
            rows = []
            for i in res.get('data'):
                tmp = {}
                tmp.update({'id': i.id,
                            'name': i.name,
                            'no': i.asset_No,
                            'type': i.Type,
                            'price': i.price,
                            'status': i.status,
                            'company': i.company,
                            'contacts': i.contacts,
                            'manger_user': i.manger_user,
                            'finance_id': i.finance_id,
                            'host_id': i.info.id,
                            'create_at': i.create_at.strftime('%Y-%m-%dT%H:%M:%S'),
                            'update_at': i.update_at.strftime('%Y-%m-%dT%H:%M:%S')
                            }
                           )
                rows.append(tmp)
            data = {'page': res.get('page'),
                    'total': res.get('last'),
                    'records': res.get('records'), 'rows': rows}
            return HttpResponse(json.dumps(data), content_type="application/json")
            
        elif request.POST.get('_search', None) == 'true':

            if request.POST.get('searchOper') in search_rules.get('rules1'):
                obj = Paging.page_list(request, Fliter_1(request, models.Reserves.objects))
                #print(obj)

            ###### id字段下的 大于、小于 不小于、不大于的模糊查询#####
            elif request.POST.get('searchField') == 'id' and request.POST.get('searchOper') in search_rules.get(
                    'rules2'):
                obj = Paging.page_list(request, Fliter_2(request, models.Reserves.objects))



            elif request.POST.get('searchOper') in search_rules.get('rules3'):
                ####后续调整
                pass
            res = obj
            rows = []
            for i in res.get('data'):
                tmp = {}
                tmp.update({'id': i.id,
                            'name': i.name,
                            'no': i.asset_No,
                            'type': i.Type,
                            'price': i.price,
                            'status': i.status,
                            'company': i.company,
                            'contacts': i.contacts,
                            'manger_user': i.manger_user,
                            'host_id': i.info.id,
                            'finance_id': i.finance_id,
                            'create_at': i.create_at.strftime('%Y-%m-%dT%H:%M:%S'),
                            'update_at': i.update_at.strftime('%Y-%m-%dT%H:%M:%S')
                            }
                           )
                rows.append(tmp)
            data = {'page': res.get('page'),
                    'total': res.get('last'),
                    'records': res.get('records'), 'rows': rows}
            return HttpResponse(json.dumps(data), content_type="application/json")
    return  render(request, 'storage.html',menu_list(request))



@auth
def consumable(request):
    if request.method == 'POST':
        if request.POST.get('oper', None) == 'edit':
            obj = models.Reserves.objects.filter(id=request.POST.get('id')).update(name=request.POST.get('name'),
                                                                                   contacts=request.POST.get(
                                                                                       'contacts'),
                                                                                   Address=request.POST.get('Address'),
                                                                                   phone=request.POST.get('phone'),
                                                                                   bill=request.POST.get('bill'),
                                                                                   type=request.POST.get('type'))
            obj.save()
            return HttpResponse(json.dumps({'Status': 'success', }))


        elif request.POST.get('_search', None) == 'false':
            obj = models.Reserves.objects.filter(Type='低值易耗品').all()
            res = Paging.page_list(request, obj)
            rows = []
            for i in res.get('data'):
                tmp = {}
                tmp.update({'id': i.id,
                            'name': i.name,
                            'no': i.asset_No,
                            'type': i.Type,
                            'price': i.price,
                            'status': i.status,
                            'company': i.company,
                            'contacts': i.contacts,
                            'manger_user': i.manger_user,
                            'host_id': i.info.id,
                            'create_at': i.create_at.strftime('%Y-%m-%dT%H:%M:%S'),
                            'update_at': i.update_at.strftime('%Y-%m-%dT%H:%M:%S')
                            }
                           )
                rows.append(tmp)
            data = {'page': res.get('page'),
                    'total': res.get('last'),
                    'records': res.get('records'), 'rows': rows}
            return HttpResponse(json.dumps(data), content_type="application/json")

        elif request.POST.get('_search', None) == 'true':

            if request.POST.get('searchOper') in search_rules.get('rules1'):
                obj = Paging.page_list(request, Fliter_1(request, models.Reserves.objects))
                

            ###### id字段下的 大于、小于 不小于、不大于的模糊查询#####
            elif request.POST.get('searchField') == 'id' and request.POST.get('searchOper') in search_rules.get(
                    'rules2'):
                obj = Paging.page_list(request, Fliter_2(request, models.Reserves.objects))



            elif request.POST.get('searchOper') in search_rules.get('rules3'):
                ####后续调整
                pass
            res = obj
            rows = []
            for i in res.get('data'):
                tmp = {}
                tmp.update({'id': i.id,
                            'name': i.name,
                            'no': i.asset_No,
                            'type': i.Type,
                            'price': i.price,
                            'status': i.status,
                            'company': i.company,
                            'contacts': i.contacts,
                            'manger_user': i.manger_user,
                            'host_id': i.info.id,
                            'create_at': i.create_at.strftime('%Y-%m-%dT%H:%M:%S'),
                            'update_at': i.update_at.strftime('%Y-%m-%dT%H:%M:%S')
                            }
                           )
                rows.append(tmp)
            data = {'page': res.get('page'),
                    'total': res.get('last'),
                    'records': res.get('records'), 'rows': rows}
            return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'consumable.html',menu_list(request))




@auth
def select(request):
    return  render(request, 'stock_inquiry.html',menu_list(request))




@auth
def info_list(request,page):
    
    try:
         obj = models.Reserves.objects.get(id=int(page))
         print(obj.name)
         data = {'status': 'success', 'code': 200, 'data': obj}
    except ValueError :
       data= {'status': 'success','code':404, 'data':'没有数据'}
    except Exception as e:
        data = {'status': 'error',  'data': e}
    tmp = {'info':data}
    tmp.update(menu_list(request))
    return render(request,'info_list.html',tmp)

@auth
def stock_inquiry(request):
    pass




