from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseGone
from django.shortcuts import render, redirect, get_object_or_404
import datetime
from django import forms

from django.conf import settings
# Create your views here.

from .models import Vrfy,Vrfy_Cmd


app_name ='dq'
def dummy(request, template_name='dummy.html'):
    data = {}
    data['object_list'] = getattr(settings, "BASE_DIR", None)
    data['app_name'] = app_name
    return render(request, template_name, data)

def base(request, template_name='base.html'):
    data = {}
    data['object_list'] = getattr(settings, "BASE_DIR", None)
    return render(request, template_name, data)

########################## vrfy ########################## 

class VrfyForm(ModelForm):
    class Meta:
        model = Vrfy
        fields = ['DB_NM', 'SCHEMA_NM', 'CLSF_NM1', 'CLSF_NM2', 'TABLE_NM', 'TABLE_HANGL_NM','PRESER_PRD_DDNUM','VRFY_TYPE_CD','VRFY_CNTS','BKUP_YN','USE_YN'
        ,'RGSTR_ID'
        #,'RGST_DTTM'
        ,'MODR_ID'
        #,'MODI_DTTM'
        ]

def vrfy_list(request, template_name='vrfy_list.html'):
    gets = request.GET
    print(gets)
    if ( 'qry' in gets ) :
        qry = gets['qry']
    else:
        qry = ''
    if (qry == None or len(qry) <= 2):
        vrfys = Vrfy.objects.all()
    else:
        vrfys = Vrfy.objects.filter(TABLE_NM__startswith=qry)
    data = {}
    data['object_list'] = vrfys
    data['gets'] = gets
    return render(request, template_name, data)

def vrfy_create(request, template_name='vrfy_form.html'):
    form = VrfyForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('dq:vrfy_list')
    return render(request, template_name, {'form':form})

def vrfy_update(request, pk,template_name='vrfy_form.html'):    
    vrfy = get_object_or_404(Vrfy, pk=pk)
    form = VrfyForm(request.POST or None, instance=vrfy)
    if form.is_valid():
        form.save()
        return redirect('dq:vrfy_list')
    return render(request, template_name, {'form':form,'row' : vrfy })

def vrfy_delete(request, pk):
    vrfy= get_object_or_404(Vrfy, pk=pk)    
    if vrfy != None :
        vrfy.delete()
        return redirect('dq:vrfy_list')
    return HttpResponse(status=405)


########################## vrfy_Cmd ########################## 
class vrfy_CmdForm(ModelForm):
    class Meta:
        model = Vrfy_Cmd
        fields = [ 'VRFY_NO','VRFY_SEQ', 'AUTO_CK_YN', 'CMD_DVS_CD', 'CMD_TYPE_CD', 'CMD_CNTS','DTL_VRFY_YN'
        ,'RGSTR_ID'
        #,'RGST_DTTM'
        ,'MODR_ID'
        #,'MODI_DTTM'
        ]

def vrfy_Cmd_list(request, template_name='vrfy_Cmd_list.html'):
    gets = request.GET
    if ( 'qry' in gets ) :
        qry = gets['qry']
    else:
        qry = ''
    if (qry == None or len(qry) <= 2):
        vrfy_Cmds = Vrfy_Cmd.objects.all()
    else:
        vrfys = Vrfy.objects.filter(TABLE_NM__startswith=qry)
        vrfy_Cmds = []
        for row in vrfys:
            vrfy_Cmds.extend(Vrfy_Cmd.objects.filter(VRFY_NO=row))
    data = {}
    data['object_list'] = vrfy_Cmds
    data['gets'] = gets
    return render(request, template_name, data)

def vrfy_Cmd_create(request, template_name='vrfy_Cmd_form.html'):
    form = vrfy_CmdForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('dq:vrfy_Cmd_list')
    return render(request, template_name, {'form':form})

def vrfy_Cmd_update(request, pk,template_name='vrfy_Cmd_form.html'):    
    vrfy_Cmd = get_object_or_404(Vrfy_Cmd, pk=pk)
    form = vrfy_CmdForm(request.POST or None, instance=vrfy_Cmd)
    if form.is_valid():
        form.save()
        return redirect('dq:vrfy_Cmd_list')
    return render(request, template_name, {'form':form,'row' : vrfy_Cmd })

def vrfy_Cmd_delete(request, pk):
    vrfy_Cmd = get_object_or_404(Vrfy_Cmd, pk=pk)    
    if vrfy_Cmd != None :
        vrfy_Cmd.delete()
        return redirect('dq:vrfy_Cmd_list')
    return HttpResponse(status=405)   