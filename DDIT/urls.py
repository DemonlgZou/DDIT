from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
from System import Views
from Assets import Views
from DDIT import views
urlpatterns = [
    path('admin/', admin.site.urls),
    url('^system_manager/',include('System.urls')),
    url('^asserts_manager/',include('Assets.urls')),
    url('login.html/',views.login)               ,
    url('logout.html/',views.logout)   ,
    url('index.html/',views.index,name='index')
]
