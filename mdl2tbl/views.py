import os
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone


############################## bootstrap 3 ##############################
from django.views.generic.base import TemplateView
from django.contrib import messages
######################################################################################
from .ora_test import get_mdl
from .my_test import get_tbl
#import ora_test
#import my_test

def mk_dict(rows):
    d = {}
    for row in rows: 
        k1 = row['SCHEMA'] + '|' + row['TBL_NM']+ '|' + row['COL_NM']
        d[k1] = row
        #print(k1, d[k1])
    return d

def mk_comp(d1,d2):
    comp = []
    for pk in d1.keys():
        #같은 컬럼이 존재하면 처리한다.
        if pk in d2:
            pk_print = True 
            rstr = ""        
            for col in ['DT','NULLABLE','DEFT'] :
                if d1[pk][col] != d2[pk][col]:  
                    if pk_print == True :
                        #print(pk,'='*(80-len(pk)))
                        pk_print = False                            
                    #print("%40s : %15s <=> %15s " % (col,d1[pk][col],d2[pk][col]))
                    rstr  += ("%40s : %15s <=> %15s " % (col,d1[pk][col],d2[pk][col])) + "<br>"
            if pk_print == False and len(rstr) > 0:
                comp.append ( { 'SCHEMA' : d1[pk]['SCHEMA'], 'TBL_NM' : d1[pk]['TBL_NM'] , 'COL_NM' : d1[pk]['COL_NM'] , 'DIFF' : rstr })
    return comp
######################################################################################

# Create your views here.
def tbl_list(request):
    print("HELLO WOLRD")
    rows1 = get_mdl()
    return render(request, 'mdl2tbl/test.html', {'rows': rows1})

def comp_list(request,pk="%"):
    if (pk == None or len(pk) != 2) :
        pk = '%'        
    rows1 = get_mdl(pk)
    d1 = mk_dict(rows1)

    rows2 = get_tbl(pk)
    d2 = mk_dict(rows2)

    comp = mk_comp(d1,d2)
    return render(request, 'mdl2tbl/comp.html', {'rows': comp })

def home(request,pk="%"):
    if (pk == None or len(pk) != 2) :
        pk = '%'        
    rows1 = get_mdl(pk)
    d1 = mk_dict(rows1)

    rows2 = get_tbl(pk)
    d2 = mk_dict(rows2)

    comp = mk_comp(d1,d2) 
    return render(request,'mdl2tbl/home.html',{'rows': comp })

def form(request,pk="%"):
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