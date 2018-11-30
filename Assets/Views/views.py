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
                  obj = models.Company_info.objects.filter(id=request.POST.get('id')).update( name=request.POST.get('name'),contacts=request.POST.get('contacts'),Address=request.POST.get('Address'),phone=request.POST.get('phone'),bill=request.POST.get('bill'),type=request.POST.get('type'))
                  return HttpResponse(json.dumps({'Status':'success',}))


            #删除数据
            elif request.POST.get('oper', None) == 'del':
                models.Company_info.objects.filter(id=request.POST.get('id')).delete()
                return HttpResponse(json.dumps({'Status': 'success','message':'ok'  }))



            #正常查询数据
            elif request.POST.get('_search',None) == 'false':
                obj = models.Company_info.objects.all()
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
                                          'update_at': (i.update_at).strftime('%Y-%m-%dT%H:%M:%S')})
                              rows.append(tmp)
                          data = {'page': res.get('page'),
                                  'total': res.get('last'),
                                  'records': res.get('records'), 'rows': rows}
                          return HttpResponse(json.dumps(data), content_type="application/json")
        return  render(request, 'supplier.html',menu_list(request))






@auth
def in2out(request):
    if request.method == 'POST':
        print(request.POST.get('name'))
        return HttpResponse(json.dumps({'status':'success'}), content_type="application/json")
    elif request.method == 'GET':
        obj = models.Company_info.objects.all()
        tmp = {'info':obj}
        tmp.update(menu_list(request))
        return  render(request, 'stock_inquiry.html',tmp)




@auth
def assets(request):
    #固定资产视图
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
                # print(obj)

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
         print(page)
         obj = models.Reserves.objects.get(id=int(page))
         print(obj)
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




def write_data():
    data = xlrd.open_workbook(r'D:\DDIT\db_server\1111111.xlsx')
    table = data.sheet_by_index(0)
    nrows = table.nrows
    cols = table.ncols
    t = 0

    for i in range(0, int(nrows)):
        if t > 1:

                info = (table.row_values(i))
                name = info[4]
                Type = '台式机'
                CPU = info[5]
                memory = info[7]
                Bios = info[6]
                MAC = info[2]
                SN =info[-1]
                NET =info[13]
                cd =info[12]
                Video =info[10]
                Sound =info[11]
                Disk =info[8]
                user = info[0]
                obj = models.Dictionary.objects.get(id=3)
                arr1 = obj.arr1
                arr2 = obj.arr2
                arr3 = int(obj.arr3)
                new_arr3 = arr3 +1
                models.Dictionary.objects.update(arr3=str(new_arr3).zfill(6))
                No = '%s-%s-%s%s'%(arr1,arr2,str((datetime.datetime.now().year)),str(new_arr3).zfill(6))
               # print(No)
              #  No =    arr3.zfill(6)
              #  print(No)
               # print(info[9])
                #print(name,Type,CPU,memory,Bios,MAC,SN,NET,cd,Video,Sound,Disk)

                obj = models.host_info.objects.create(name=name,type=Type,CPU=CPU,Memory=memory,Bios=Bios,MAC=MAC,SN=SN,Sound=Sound,Disk=Disk,CDrom=cd,NETWORK=NET,Video=Video)
                models.Reserves.objects.create(name='办公电脑',Type=1,asset_No=No,price=0,company=0,contacts='无',manger_user=info[0],status=1,info_id=obj.id)
                #models.host_info.objects.create(name=info[4],type='显示器',Display=info[9])
        t += 1
#write_data()