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
    #vrfy
    url(r'^vrfys', views.vrfy_list, name='vrfy_list'),
    url(r'^vrfy/create$', views.vrfy_create, name='vrfy_new'),
    url(r'^vrfy/update/(?P<pk>\d+)', views.vrfy_update, name='vrfy_edit'),
    url(r'^vrfy/delete/(?P<pk>\d+)', views.vrfy_delete, name='vrfy_delete'),
    # 오로가 검증대상을 일괄로 수행해줌   
    # curl -d env=dev http://localhost:8001/dq/vrfy/tasks_aurora/
    url(r'^vrfy/tasks_aurora/', views.vrfy_tasks_aurora, name='vrfy_tasks_aurora'),  

    url(r'^vrfy/tasks/', views.vrfy_tasks, name='vrfy_tasks'),    
    url(r'^vrfy/job/(?P<pk>\d+)', views.vrfy_job, name='vrfy_job'),
    url(r'^vrfy/run/(?P<pk>\d+)', views.vrfy_run, name='vrfy_run'),
    #vrfyLog 
    url(r'^vrfyLog_ajax/', views.vrfyLog_ajax, name='vrfyLog_ajax'),     
    url(r'^vrfyLogs', views.vrfyLog_list, name='vrfyLog_list'),   
    #ilm(information lifecycle mgmt.)
    url(r'^ilms', views.ilm_list, name='ilm_list'),
    url(r'^ilm/create$', views.ilm_create, name='ilm_new'),
    url(r'^ilm/update/(?P<pk>\d+)', views.ilm_update, name='ilm_edit'),
    url(r'^ilm/delete/(?P<pk>\d+)', views.ilm_delete, name='ilm_delete'),
    
    #task
    url(r'^tasks', views.tasks, name='tasks'),
    #vrfyCmd
    url(r'^vrfy_Cmds', views.vrfy_Cmd_list, name='vrfy_Cmd_list'),
    url(r'^vrfy_Cmd/create$', views.vrfy_Cmd_create, name='vrfy_Cmd_new'),
    url(r'^vrfy_Cmd/update/(?P<pk>\d+)', views.vrfy_Cmd_update, name='vrfy_Cmd_edit'),
    url(r'^vrfy_Cmd/delete/(?P<pk>\d+)', views.vrfy_Cmd_delete, name='vrfy_Cmd_delete'),       
]