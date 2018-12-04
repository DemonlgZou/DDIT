from django.shortcuts import  redirect,render
from db_server.models import *
def auth(func):
	# 负责做用户登陆认证的方法
	def inner(request, *args, **kwargs):
		request.session.clear_expired()
		try:
			if request.session.exists(request.COOKIES['sessionid']) is False:
				return redirect('/login.html')
			else:
				return func(request, *args, **kwargs)
		except KeyError:
			return redirect('/login.html')
	return inner



def menu_list(request):
    #####根据用户角色分配动态菜单#####
    tmp =[]
    user_id= request.session.get('user_id',None)
    if user_id !=None:
        menu = Role2Menu.objects.filter(rid=user_id).all().order_by('id')
        list1 = Menu.objects.filter(menu__in=menu).all().order_by('id')
        for i in menu:
            i.menu.id
            tmp.append(i.menu.id)
        list2 = Menu.objects.filter(top_no__in=tmp).all().order_by('id')
        return {'top':list1,'child':list2}
    else:
        return render(request,'login.html')


def Fliter_1(request, Mod):
    # 等于 不等于 或者 属于 不属于 匹配查询
    if request.POST.get('searchOper') == 'eq':
        obj = Mod.filter(
            **{request.POST.get('searchField'): request.POST.get('searchString')}).all().order_by('id')

    elif request.POST.get('searchOper') == 'ne':
        obj = Mod.filter(
            ~models.Q(**{request.POST.get('searchField'): request.POST.get('searchString')})).all().order_by('id')
    elif request.POST.get('searchOper') == 'in':
        q1 = models.Q()
        q1.connector = 'OR'
        tmp_list = request.POST.get('searchString').split(' ')
        for i in tmp_list:
            q1.children.append((request.POST.get('searchField'), i))
        obj = Mod.filter(q1).all().order_by('id')
    elif request.POST.get('searchOper') == 'ni':
        q1 = models.Q()
        q1.connector = 'OR'
        tmp_list = request.POST.get('searchString').split(' ')
        for i in tmp_list:
            q1.children.append(
                (request.POST.get('searchField'), i))
        obj = Mod.filter(~q1).all().order_by('id')
    return obj



def Fliter_2(request,Mod):
    # ID 相关的小于，大于 ，小于等于，大于等于###
    if request.POST.get('searchOper') == 'lt':
        obj = Mod.filter(id__lt=request.POST.get('searchString')).all().order_by('id')
    elif request.POST.get('searchOper') == 'le':
        obj = Mod.filter(id__lte=request.POST.get('searchString')).all().order_by('id')
    elif request.POST.get('searchOper') == 'gt':
        obj = Mod.filter(
            id__gt=request.POST.get('searchString')).all().order_by('id')

    elif request.POST.get('searchOper') == 'ge':
        obj = Mod.filter(
            id__gte=request.POST.get('searchString')).all().order_by('id')
    return obj

search_rules = {'rules1':['eq','ne','in','ni'],'rules2':['lt','le','gt','ge'],'rules3':['bw','bn','ew','en','cn','nc']}