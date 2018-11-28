from django.urls import path
from django.conf.urls import include,url
from System.Views import views

urlpatterns = [
    url('firewall.html/',views.firewall,name='firewall'),
    url('vm_host.html/',views.vm,name='vm'),
    url('host_list.html/',views.host_list,name='host_list'),
    url('port_list.html/',views.firewall_list,name='port_list'),
]
