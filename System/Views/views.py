from django.shortcuts import render ,HttpResponse
from db_server import models
from DDIT import Paging
import json,datetime

class CJsonEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime.datetime):
			return obj.strftime('%Y-%m-%d %H:%M:%S')
		elif isinstance(obj, datetime):
			return obj.strftime("%Y-%m-%d")
		else:
			return json.JSONEncoder.default(self, obj)





def firewall(request):

    return render(request,'port.html',models.menu_info)


def firewall_list(request):

    return render(request,'port_list.html',models.menu_info)

def vm(request):





    return render(request, 'create_host.html',models.menu_info)




def host_list(request):
    if request.method =='POST':
        obj = models.Server_info.objects.all()
        res = Paging.page_list(request,obj)
        print(res.get('data'))
        rows = []
        for i in res.get('data') :
            tmp = {}
            tmp.update({'id':i.id,'name':i.name,'IP':i.IP,'server':i.server,'OS':i.OS,'desric':i.desric,'status':i.status,'create_at':(i.create_at).strftime('%Y-%m-%dT%H:%M:%S'),'update_at':(i.update_at).strftime('%Y-%m-%dT%H:%M:%S')})
            rows.append(tmp)
        data = {'page':res.get('page'),
                'total':res.get('last'),
                'records':res.get('records'),'rows':rows}
        print(data)
        return HttpResponse(json.dumps(data),content_type="application/json")
    return render(request,'host_list.html',models.menu_info)