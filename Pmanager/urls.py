from django.conf.urls import url
from Pmanager.Views import views
urlpatterns = [


    url('project_list.html/', views.pm_list,name='project_list'), #供货商查询
    url('work_hours.html/', views.pm_work,name='work_hours'),   #出入库管理
    url('project_add.html/', views.pm_add,name='add_project'),   #出入库管理
    url('period_list.html/', views.pm_period,name='period_list'),   #出入库管理

    # url('supplier.html/', views.supplier,name='supplier'),
]
