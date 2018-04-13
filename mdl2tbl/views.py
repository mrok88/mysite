###########################################################################
#     Meta-eXpress 2.1 
#     All right reserved by wonseokyou 
#     email : wonseokyou@gmail.com 
###########################################################################
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
from .forms import CompForm, FilesForm, ContactFormSet, TableNameForm
############################## bootstrap 3 ##############################
from django.views.generic.base import TemplateView
from django.contrib import messages
######################################################################################
from . import ora_test as Ora
from .ora_test import get_mdl
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
    '''모델비교'''
    template_name = 'mdl2tbl/djbs01.html'    
    def get_context_data(self, **kwargs):
        # form_class에 기본 get값을 설정한다.            
        self.form_class = CompForm
        gets = self.request.GET
        # yws_gets에 get값들을 복제한다.
        self.form_class.yws_gets = gets.copy()
        self.form_class.yws_gets['title'] = "모델비교"
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
    '''데이터수명주기'''
    template_name = 'mdl2tbl/djbs02.html'    
    def get_context_data(self, **kwargs):
        # form_class에 기본 get값을 설정한다.            
        self.form_class = CompForm
        gets = self.request.GET
        # yws_gets에 get값들을 복제한다.
        self.form_class.yws_gets = gets.copy()
        self.form_class.yws_gets['title'] = "데이터수명주기"
        # 특정 default값을 가져와서 설정한다.
        for ( pk , val ) in gets.items():            
            self.form_class.base_fields[pk].initial =  val
            #print('pk:val',pk,val)
        # subjArea(subject Area) 입력값이 있으면 수행을 한다.
        if ( len(gets) > 0 and 'subjArea' in gets ):
            self.form_class.yws_rows = Ora.get_capa(gets['subjArea'])
        else:
            self.form_class.yws_rows = {}

        # context를 가져온다.
        context = super(Djbs02FormView, self).get_context_data(**kwargs)
        return context

class Djbs03FormView(FormView):
    template_name = 'mdl2tbl/djbs07.html'    
    def get_context_data(self, **kwargs): 
        self.form_class = CompForm   
        self.form_class.yws_gets = { 'title' : "암호화대상목록" }        
        self.form_class.yws_rows = Ora.get_enc_list()
        # context를 가져온다.
        context = super(Djbs03FormView, self).get_context_data(**kwargs)
        return context

class Djbs04FormView(FormView):
    template_name = 'mdl2tbl/djbs07.html'    
    def get_context_data(self, **kwargs): 
        self.form_class = CompForm   
        self.form_class.yws_gets = { 'title' : "마스킹대상목록" }
        self.form_class.yws_rows = Ora.get_mask_list()
        # context를 가져온다.
        context = super(Djbs04FormView, self).get_context_data(**kwargs)
        return context

class Djbs05FormView(FormView):
    '''테이블정의서'''
    template_name = 'mdl2tbl/djbs05.html'    
    def get_context_data(self, **kwargs):
        # form_class에 기본 get값을 설정한다.            
        self.form_class = CompForm
        gets = self.request.GET
        # yws_gets에 get값들을 복제한다.
        self.form_class.yws_gets = gets.copy()
        self.form_class.yws_gets['title'] = "테이블정의서"
        # 특정 default값을 가져와서 설정한다.
        for ( pk , val ) in gets.items():            
            self.form_class.base_fields[pk].initial =  val
            #print('pk:val',pk,val)
        # subjArea(subject Area) 입력값이 있으면 수행을 한다.
        if ( len(gets) > 0 and 'subjArea' in gets ):
            self.form_class.yws_rows = Ora.get_defi(gets['subjArea'])
        else:
            self.form_class.yws_rows = {}

        # context를 가져온다.
        context = super(Djbs05FormView, self).get_context_data(**kwargs)
        return context

class Djbs06FormView(FormView):
    '''컬럼정의서'''
    template_name = 'mdl2tbl/djbs06.html'    
    def get_context_data(self, **kwargs):
        # form_class에 기본 get값을 설정한다.            
        self.form_class = TableNameForm
        gets = self.request.GET
        # yws_gets에 get값들을 복제한다.
        self.form_class.yws_gets = gets.copy()
        self.form_class.yws_gets['title'] = "컬럼정의서"
        # 특정 default값을 가져와서 설정한다.
        for ( pk , val ) in gets.items():            
            self.form_class.base_fields[pk].initial =  val
            #print('pk:val',pk,val)
        # subjArea(subject Area) 입력값이 있으면 수행을 한다.
        if ( len(gets) > 0 and 'tblNm' in gets ):
            self.form_class.yws_rows = Ora.get_defi_col(gets['tblNm'])
        else:
            self.form_class.yws_rows = {}

        # context를 가져온다.
        context = super(Djbs06FormView, self).get_context_data(**kwargs)
        return context

class Djbs07FormView(FormView):
    template_name = 'mdl2tbl/djbs07.html'            
    def get_context_data(self, **kwargs): 
        self.form_class = CompForm   
        self.form_class.yws_gets = { 'title' : "직원명 컬럼" }
        self.form_class.yws_rows = Ora.get_emp_col()
        # context를 가져온다.
        context = super(Djbs07FormView, self).get_context_data(**kwargs)
        return context

class Djbs08FormView(FormView):
    template_name = 'mdl2tbl/djbs07.html'    
    def get_context_data(self, **kwargs): 
        self.form_class = CompForm   
        self.form_class.yws_gets = { 'title' : "고객명 컬럼" }
        self.form_class.yws_rows = Ora.get_cust_col()
        # context를 가져온다.
        context = super(Djbs08FormView, self).get_context_data(**kwargs)
        return context