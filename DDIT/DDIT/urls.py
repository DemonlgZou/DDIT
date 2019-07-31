from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url

from DDIT import views
urlpatterns = [
    path('admin/', admin.site.urls),
    url('^system_manager/',include('System.urls')),
    url('^asserts_manager/',include('Assets.urls')),
    url('^Pmanager/',include('Pmanager.urls')),
    url('login.html/',views.Login)               ,
    url('logout.html/',views.Logut)   ,
    url('index.html/',views.index,name='index'),
    url('^$',views.index,name='index')
]
