from django import forms


class firewall_port(forms.Form):
    # 验证前端传入的开放端口的表单数据类型
   user = forms.CharField()  #申请人
   name = forms.CharField()
   dept = forms.CharField()
   ip = forms.GenericIPAddressField()
   Type = forms.CharField()
   port = forms.IntegerField()
   create_at = forms.DateTimeField()
   end_at = forms.DateTimeField()
   

class create_vm(forms.Form):
    #验证前端传入的创建新虚拟机的表单数据类型
    user = forms.CharField()  # 申请人
    name = forms.CharField()
    dept = forms.CharField()
    #vm_ip = forms.GenericIPAddressField()
    ip = forms.GenericIPAddressField()
    os = forms.CharField()
    cpus = forms.IntegerField()
    men = forms.IntegerField()
    Size = forms.IntegerField()
    Type = forms.CharField()
    #port = forms.IntegerField()
    create_at = forms.DateTimeField()
    end_at = forms.DateTimeField()
