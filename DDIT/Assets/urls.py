from django.conf.urls import url
from Assets.Views import views
urlpatterns = [


    url('supplier.html/', views.supplier,name='supplier'), #供货商查询
    url('add.html/', views.in2out,name='in2out'),   #出入库管理
    url('assets_list.html/', views.assets,name='assets'), #固定资产查询
    url('consumable.html/', views.consumable,name='consumable'),  #易耗品查询
    url('assets_log.html/', views.select,name='asset_log'), ####库存查询表
    url('info_list.html/(?P<page>\d+)$',views.info_list,name ='info_list'),
    url('add_type.html/', views.add_type,name='add_type'),
]
