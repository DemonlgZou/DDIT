from django.urls import path
from django.conf.urls import include,url
from System.Views import views

urlpatterns = [
    url('firewall.html/',views.firewall_open_port,name='firewall'),
    url('close_port/',views.firewall_close_port),
    url('vm_host.html/',views.vm,name='vm'),
    url('host_list.html/',views.host_list,name='host_list'),
    url('port_list.html/',views.firewall_list,name='port_list'),
    url('system_log.html/',views.log,name='system_log'),
    url('monitoring_list.html/',views.monitoring_list,name='monitoring_list'),
    url('add_monitor_host.html/',views.add_monitor_host,name='add_monitor_host'),
    url('server/vm_start',views.vm_start),
    url('server/vm_shutdown',views.vm_shutdown),
    url('server/vm_reboot',views.vm_reboot),
    url('vm_manager/list.html/',views.vm_manager,name='vm_manager'),
    url('ADD_WIFI_USER.html/',views.ADD_WIFI_USER,name='WIFI_USER_MANAGER'),
    url('DELETE_WIFI_USER.html/',views.DELETE_WIFI_USER),
    url('CLEAN_WIFI_USER.html/',views.CLEAN_WIFI_USER),
    url('wifi_user_list.html/',views.wifi_user_list,name='WIFI_USER_LIST'),
    url('vm_manager/list.html/',views.vm_manager,name='WIFI_USER_LOGS'),
    url('OPEN_SW_PORT.html/',views.OPEN_SW_PORT,name='OPEN_SW_PORT'),
    url('vm_manager/list.html/',views.vm_manager,name='OPEN_SW_PORT_LOGS'),
]
