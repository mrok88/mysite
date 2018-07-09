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
from .forms import CompForm, FilesForm, ContactFormSet, TableNameForm,AttrNameForm,ColNameForm
############################## bootstrap 3 ##############################
from django.views.generic.base import TemplateView
from django.contrib import messages
######################################################################################
from . import ora_test as Ora
from .ora_test import get_mdl
from .my_test import get_tbl,get_cd_list
from .comp import mk_dict,mk_comp
from . import comp_aurora as Aurora
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

#ajax return function 
def cd_list(request):
    # context = { 'message' : [
    #                         {'CD_NM': '신청', 'CD': '110'},
    #                         {'CD_NM': '응모', 'CD': '120'},
    #                         {'CD_NM': '당첨', 'CD': '130'},
    #                         {'CD_NM': '당첨취소', 'CD': '140'},
    #                         {'CD_NM': '당첨대기', 'CD': '150'},
    #                         {'CD_NM': '제세공과금 입금요청', 'CD': '160'},
    #                         {'CD_NM': '제세공과금 입금완료', 'CD': '170'},
    #                         {'CD_NM': '당첨확정', 'CD': '175'},
    #                         {'CD_NM': '지급요청', 'CD': '180'},
    #                         {'CD_NM': '경품발송', 'CD': '190'},
    #                         {'CD_NM': '지급완료', 'CD': '200'},
    #                     ] ,
    #             'ret'  : 'OK'
    #         }
    cd = request.GET['cd']
    rows = get_cd_list(cd)
    context = { 'message' : rows,
                'ret'  : 'OK'
            }    
    return HttpResponse(json.dumps(context), content_type="application/json")    

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
            self.form_class.yws_gets['title'] = "테이블정의서(" + gets['subjArea'] + ")"
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
            self.form_class.yws_gets['title'] = "컬럼정의서 (" + gets['tblNm'] + ")"
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

class Djbs09FormView(FormView):
    template_name = 'mdl2tbl/djbs09.html'    
    def get_context_data(self, **kwargs): 
        self.form_class = CompForm   
        self.form_class.yws_gets = { 'title' : "코드 정의서" }
        self.form_class.yws_rows = Ora.get_cd_defi()
        # context를 가져온다.
        context = super(Djbs09FormView, self).get_context_data(**kwargs)
        return context

class Djbs10FormView(FormView): 
    '''속성사용테이블'''
    template_name = 'mdl2tbl/djbs10.html'    
    def get_context_data(self, **kwargs):
        # form_class에 기본 get값을 설정한다.            
        self.form_class = AttrNameForm
        gets = self.request.GET
        # yws_gets에 get값들을 복제한다.
        self.form_class.yws_gets = gets.copy()
        self.form_class.yws_gets['title'] = "속성사용테이블"
        # 특정 default값을 가져와서 설정한다.
        for ( pk , val ) in gets.items():            
            self.form_class.base_fields[pk].initial =  val
            #print('pk:val',pk,val)
        # subjArea(subject Area) 입력값이 있으면 수행을 한다.
        if ( len(gets) > 0 and 'attrNm' in gets ):
            self.form_class.yws_gets['title'] = "속성사용테이블 (" + gets['attrNm'] + ")"
            self.form_class.yws_rows = Ora.get_attr_use_tbl(gets['attrNm'])
        else:
            self.form_class.yws_rows = {}

        # context를 가져온다.
        context = super(Djbs10FormView, self).get_context_data(**kwargs)
        return context

class Djbs11FormView(FormView): 
    '''컬럼사용테이블'''
    template_name = 'mdl2tbl/djbs11.html'    
    def get_context_data(self, **kwargs):
        # form_class에 기본 get값을 설정한다.            
        self.form_class = ColNameForm
        gets = self.request.GET
        # yws_gets에 get값들을 복제한다.
        self.form_class.yws_gets = gets.copy()
        self.form_class.yws_gets['title'] = "컬럼사용테이블"
        # 특정 default값을 가져와서 설정한다.
        for ( pk , val ) in gets.items():            
            self.form_class.base_fields[pk].initial =  val
            #print('pk:val',pk,val)
        # subjArea(subject Area) 입력값이 있으면 수행을 한다.
        if ( len(gets) > 0 and 'colNm' in gets ):
            self.form_class.yws_gets['title'] = "컬럼사용테이블 (" + gets['colNm'] + ")"
            self.form_class.yws_rows = Ora.get_col_use_tbl(gets['colNm'])
        else:
            self.form_class.yws_rows = {}

        # context를 가져온다.
        context = super(Djbs11FormView, self).get_context_data(**kwargs)
        return context

class Djbs12FormView(FormView): 
    '''컬럼비교(DEV<=>TST)'''
    template_name = 'mdl2tbl/djbs12.html'    
    def get_context_data(self, **kwargs):
        # form_class에 기본 get값을 설정한다.            
        self.form_class = CompForm
        gets = self.request.GET
        # yws_gets에 get값들을 복제한다.
        self.form_class.yws_gets = gets.copy()
        self.form_class.yws_gets['title'] = "AURORA(dev<=>tst)비교"
        # 특정 default값을 가져와서 설정한다.
        for ( pk , val ) in gets.items():            
            self.form_class.base_fields[pk].initial =  val
            #print('pk:val',pk,val)
        # subjArea(subject Area) 입력값이 있으면 수행을 한다.
        if ( len(gets) > 0 and 'subjArea' in gets ):
            self.form_class.yws_gets['title'] = "AURORA(dev<=>tst)비교 (" + gets['subjArea'] + ")"
            self.form_class.yws_gets['submitUrl'] = 'djbs12'
            self.form_class.yws_rows = Aurora.comp_dev_tst(gets['subjArea'])
        else:
            self.form_class.yws_rows = {}

        # context를 가져온다.
        context = super(Djbs12FormView, self).get_context_data(**kwargs)
        return context

class Djbs13FormView(FormView): 
    '''컬럼비교(DEV<=>TST)'''
    template_name = 'mdl2tbl/djbs12.html'    
    def get_context_data(self, **kwargs):
        # form_class에 기본 get값을 설정한다.            
        self.form_class = CompForm
        gets = self.request.GET
        # yws_gets에 get값들을 복제한다.
        self.form_class.yws_gets = gets.copy()
        self.form_class.yws_gets['title'] = "AURORA인덱스(dev<=>tst)비교"
        # 특정 default값을 가져와서 설정한다.
        for ( pk , val ) in gets.items():            
            self.form_class.base_fields[pk].initial =  val
            #print('pk:val',pk,val)
        # subjArea(subject Area) 입력값이 있으면 수행을 한다.
        if ( len(gets) > 0 and 'subjArea' in gets ):
            self.form_class.yws_gets['title'] = "AURORA인덱스(dev<=>tst)비교 (" + gets['subjArea'] + ")"
            self.form_class.yws_gets['submitUrl'] = 'djbs13'
            self.form_class.yws_rows = Aurora.comp_idx_dev_tst(gets['subjArea'])
        else:
            self.form_class.yws_rows = {}

        # context를 가져온다.
        context = super(Djbs13FormView, self).get_context_data(**kwargs)
        return context 


def erd_pview(request,pk="%"):
    if (pk == None or len(pk) <= 2) :
        pk = '%'
    #rs1 = Ora.get_PView('판촉_이벤트[PR]','캠페인')
    rs1 = Ora.get_PView('데이터품질[DQ]','데이터품질')
    mdlId = rs1[0]['MDL_ID']
    cnvasId = rs1[0]['CNVAS_ID']
    #print(mdlId,cnvasId)
    rs = Ora.get_PView2(mdlId,cnvasId)
    # 테이블을 출력하기 좋게 format을 수정 시작 
    tbls = []
    rows = []
    zidx = 1
    for row in rs:
        seq = row['NODE_SEQ']
        if seq == None:
            seq = -1
            ypos, xpos = row['DRAW_ITEM_ORGIN_COORD'].split(',')
            r = row['EXCOL05']
            entNm =  r.split(',')[0] if ( ',' in r ) else ""
            cols = {'TBL_NM' : row['TXT'],'ENT_NM' : entNm, 'XPOS' : xpos , 'YPOS' : ypos , 'ZIDX' : zidx }
            tbls.append({'cols' : cols , 'rows':rows})
            zidx += 1
            rows = []         
        else :
            r = row['EXCOL02']
            mark,colNm,dt,dt_len,*dummy = r.split(',') if ( ',' in r ) else ["","","","",""]
            r = row['EXCOL07']
            AttrNm =  r.split(',')[0] if ( ',' in r ) else ""
            if dt in ( 'INT','INTEGER','BIGINT','DECIMAL','SMALLINT'):
                rgb = "rgb(255, 200, 200)"
            elif dt in ( 'CHAR','VARCHAR','TEXT'):
                rgb = "rgb(238, 238, 170)"
            elif dt in ( 'DATE','TIME','DATETIME'):
                rgb = "rgb(238, 216, 170)"
            else:
                rgb = "rgb(250, 250, 250)"
            row1 = { 'SEQ' : seq , 'MARK' : mark , 'COL_NM' : colNm, 'DT' : dt+dt_len, 'ATTR_NM' : AttrNm, 'RGB': rgb }     
            rows.append(row1)
    # 테이블을 출력하기 좋게 format을 수정 종료
    print(len(tbls))    
    return render(request, 'mdl2tbl/erd.html', {'tbls' : tbls })
