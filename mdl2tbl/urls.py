# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views
############################## bootstrap 3 ##############################
from .views import HomePageView,DefaultFormView,Djbs01FormView,Djbs02FormView
######################################################################################

app_name='mdl2tbl'
urlpatterns = [
    url(r'^$',  Djbs02FormView.as_view(), name='djbs02'),  
    url(r'form_by_field', views.form_by_field , name='form_by_field'), 
    url(r'djbs01', Djbs01FormView.as_view(), name='djbs01'),
    url(r'djbs02', Djbs02FormView.as_view(), name='djbs02'),     
    url(r'form', DefaultFormView.as_view(), name='form'),
    url(r'test/', views.tbl_list, name='tbl_list'),
    url(r'comp/(?P<pk>\w*)', views.comp_list, name='comp_list'),       
]