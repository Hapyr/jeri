from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from bilanzkreisspiel.views import *

from . import views

urlpatterns = [
    url(r'^$', views.gamestart, name='gamestart'),
]