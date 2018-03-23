import os
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
############################## json ##############################
import json
############################## forms ##############################
from django.views.generic import FormView
from .forms import CompForm, FilesForm, ContactFormSet
############################## bootstrap 3 ##############################
from django.views.generic.base import TemplateView
from django.contrib import messages
######################################################################################
from .ora_test import get_mdl,get_capa
from .my_test import get_tbl
from .comp import mk_dict,mk_comp
#import ora_test
#import my_test

######################################################################################

# Create your views here.
def tbl_list(request):
    print("HELLO WOLRD")
    rows1 = get_mdl()
    return render(request, 'mdl2tbl/test.html', {'rows': rows1})

def comp_dict(pk="%"):
    if (pk == None or len(pk) <= 2 ) :
        pk = '%'        
    rows1 = get_mdl(pk)
    d1 = mk_dict(rows1)

    rows2 = get_tbl(pk)
    d2 = mk_dict(rows2)

    comp = mk_comp(d1,d2) 
    return comp

def comp_list(request,pk="%"):
    if (pk == None or len(pk) <= 2) :
        pk = '%'        
    rows1 = get_mdl(pk)
    d1 = mk_dict(rows1)

    rows2 = get_tbl(pk)
    d2 = mk_dict(rows2)

    comp = mk_comp(d1,d2)
    return render(request, 'mdl2tbl/comp.html', {'rows': comp })


def form_by_field(request,pk="%"):
    if (pk == None or len(pk) != 2) :
        pk = '%'  
    form = { 'subject' : '서브젝트' , 'message' : '메세지'}
    return render(request,'mdl2tbl/form_by_field.html',{'form' : form })


class HomePageView(TemplateView):
    template_name = 'mdl2tbl/home.html'
    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        messages.info(self.request, 'hello http://example.com')
        return context    

class DefaultFormView(FormView):
    template_name = 'mdl2tbl/form.html'
    form_class = CompForm()        


class Djbs01FormView(FormView):
    template_name = 'mdl2tbl/djbs01.html'    
    def get_context_data(self, **kwargs):
        # form_class에 기본 get값을 설정한다.            
        self.form_class = CompForm
        gets = self.request.GET
        # yws_gets에 get값들을 복제한다.
        self.form_class.yws_gets = gets.copy() 
        # 특정 default값을 가져와서 설정한다.
        for ( pk , val ) in gets.items():            
            self.form_class.base_fields[pk].initial =  val
            #print('pk:val',pk,val)
        # subjArea(subject Area) 입력값이 있으면 수행을 한다.
        if ( len(gets) > 0 and 'subjArea' in gets ):
            self.form_class.yws_rows = comp_dict(gets['subjArea'])
        else:
            self.form_class.yws_rows = {}
        # context를 가져온다.
        context = super(Djbs01FormView, self).get_context_data(**kwargs)
        return context

class Djbs02FormView(FormView):
    template_name = 'mdl2tbl/djbs02.html'    
    def get_context_data(self, **kwargs):
        # form_class에 기본 get값을 설정한다.            
        self.form_class = CompForm
        gets = self.request.GET
        # yws_gets에 get값들을 복제한다.
        self.form_class.yws_gets = gets.copy() 
        # 특정 default값을 가져와서 설정한다.
        for ( pk , val ) in gets.items():            
            self.form_class.base_fields[pk].initial =  val
            #print('pk:val',pk,val)
        # subjArea(subject Area) 입력값이 있으면 수행을 한다.
        if ( len(gets) > 0 and 'subjArea' in gets ):
            self.form_class.yws_rows = get_capa(gets['subjArea'])
        else:
            self.form_class.yws_rows = {}

        # context를 가져온다.
        context = super(Djbs02FormView, self).get_context_data(**kwargs)
        return context        