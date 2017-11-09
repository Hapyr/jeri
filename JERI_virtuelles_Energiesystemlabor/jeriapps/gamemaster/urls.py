from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.register, name='register'),
    url(r'^start_lobby$', views.start_lobby, name='start_lobby'),
    url(r'^lobby$', views.lobby, name='lobby'),
    url(r'^login_view$', views.login_view, name='login_view'),
    url(r'^logout_view$', views.logout_view, name='logout_view'),
    url(r'^all_lobbys$', views.all_lobbys, name='all_lobbys'),    
    
]
