from django import forms
from db_server.models import *



class firewall_port(forms.Form):
    # 验证前端传入的开放端口的表单数据类型
   proposer = forms.CharField()  #申请人
   desc = forms.CharField()
   dept = forms.CharField()
   host_ip = forms.GenericIPAddressField()
   type = forms.CharField()
   inside_port = forms.IntegerField()
   outside_port = forms.IntegerField()
   start_time = forms.DateField()
   end_time = forms.DateField()
   on_line = forms.CharField()
   

class create_vm(forms.Form):
    #验证前端传入的创建新虚拟机的表单数据类型
    proposer = models.CharField(max_length=128, verbose_name='申请人')
    dept = models.CharField(max_length=128, verbose_name='申请人部门')
    name = models.UUIDField(verbose_name='机器名')
    host_ip = models.GenericIPAddressField(verbose_name='宿主机IP地址', null=True)
    vm_ip = models.GenericIPAddressField(verbose_name='虚拟机IP地址', null=True)
    cpus = models.SmallIntegerField(verbose_name='CPU个数')
    memory = models.SmallIntegerField(verbose_name='内存大小')
    disk = models.CharField(verbose_name='硬盘大小', max_length=128)
    type = models.CharField(verbose_name='机器类型', max_length=128)
    os_type = models.CharField(verbose_name='机器类型', max_length=128)
    end_time = models.DateField(verbose_name='到期日期', null=True)
    on_line = models.BooleanField(verbose_name='永久生效')
    
    
class add_project(forms.Form):
        father_name = forms.CharField()
        pid = forms.CharField()
        child_name = forms.CharField()
        step = forms.CharField()
        desc = forms.CharField()
        Manage = forms.CharField()
        manager = forms.CharField()
        operator = forms.CharField()
        date_time = forms.CharField()
        service2in = forms.CharField()
        service2out = forms.CharField()
        