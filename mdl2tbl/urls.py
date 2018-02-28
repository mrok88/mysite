# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views
############################## bootstrap 3 ##############################
from .views import HomePageView
######################################################################################

app_name='mdl2tbl'
urlpatterns = [
    #url(r'^$', views.HomePageView.as_view(), name='home'),  
    url(r'home/(?P<pk>\w*)', views.home , name='home'),   
    url(r'form/', views.form , name='form'),        
    url(r'test/', views.tbl_list, name='tbl_list'),
    url(r'comp/(?P<pk>\w*)', views.comp_list, name='comp_list'),       
]