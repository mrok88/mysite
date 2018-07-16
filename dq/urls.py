# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views
############################## bootstrap 3 ##############################
######################################################################################

app_name ='dq'
urlpatterns = [
    url(r'^dummy', views.dummy, name='dummy'),    
    url(r'^base', views.base, name='base'),

    url(r'^$', views.base, name='base'),     
    #vrfy test용
    url(r'^vrfys', views.vrfy_list, name='vrfy_list'),
    url(r'^vrfy/create$', views.vrfy_create, name='vrfy_new'),
    url(r'^vrfy/update/(?P<pk>\d+)', views.vrfy_update, name='vrfy_edit'),
    url(r'^vrfy/delete/(?P<pk>\d+)', views.vrfy_delete, name='vrfy_delete'),
    url(r'^vrfy/run/(?P<pk>\d+)', views.vrfy_run, name='vrfy_run'),

    #vrfyCmd test용
    url(r'^vrfy_Cmds', views.vrfy_Cmd_list, name='vrfy_Cmd_list'),
    url(r'^vrfy_Cmd/create$', views.vrfy_Cmd_create, name='vrfy_Cmd_new'),
    url(r'^vrfy_Cmd/update/(?P<pk>\d+)', views.vrfy_Cmd_update, name='vrfy_Cmd_edit'),
    url(r'^vrfy_Cmd/delete/(?P<pk>\d+)', views.vrfy_Cmd_delete, name='vrfy_Cmd_delete'),       
]