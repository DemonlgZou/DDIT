from django.urls import path
from django.conf.urls import include,url
from System.Views import views

urlpatterns = [
    url('firewall.html/',views.firewall,name='firewall'),
    url('vm_host.html/',views.vm,name='vm'),
    url('host_list.html/',views.host_list,name='host_list'),
    url('port_list.html/',views.firewall_list,name='port_list'),
    url('system_log.html/',views.log,name='system_log'),
    url('monitoring_list.html/',views.monitoring_list,name='monitoring_list'),
    url('add_monitor_host.html/',views.add_monitor_host,name='add_monitor_host'),
    url('revice_info',views.revice_info),
    url('vm_manager/list.html/',views.vm_manager,name='vm_manager'),
]
