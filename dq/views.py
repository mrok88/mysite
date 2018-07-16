###########################################################################
#     Meta-eXpress 2.1 
#     All right reserved by wonseokyou 
#     email : wonseokyou@gmail.com 
###########################################################################
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseGone
from django.shortcuts import render, redirect, get_object_or_404
import datetime
from django import forms

from django.conf import settings
# Create your views here.

from .models import Vrfy,Vrfy_Cmd
from .dbMysql import Ssh,Conn


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

########################## vrfy start ########################## 

class VrfyForm(ModelForm):
    class Meta:
        model = Vrfy
        fields = ['DB_NM', 'SCHEMA_NM', 'CLSF_NM1', 'CLSF_NM2'
                 , 'VRFY_TYPE_DTL_CD','VRFY_NM','VRFY_EXPLN'
                 ,'TABLE_HANGL_NM','TABLE_NM', 'REFRC_TABLE_HANGL_NM','REFRC_TABLE_NM'
                 ,'USE_YN','CMD_TYPE_CD','CMD_CNTS'
        ,'RGSTR_ID'
        #,'RGST_DTTM'
        ,'MODR_ID'
        #,'MODI_DTTM'
        ]
        widgets = {
            'VRFY_EXPLN' : forms.Textarea(attrs={'rows':2}),
            'CMD_CNTS' : forms.Textarea(attrs={'rows':7}),
        }

def vrfy_list(request, template_name='vrfy_list.html'):
    gets = request.GET
    #print(gets)
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

def vrfy_run(request, pk,template_name='vrfy_run.html'):    
    vrfy = get_object_or_404(Vrfy, pk=pk)
    sqlStr = vrfy.CMD_CNTS
    print("작업번호 : %s" % vrfy.VRFY_NO)
    print("작업명  : %s" % vrfy.VRFY_NM)
    print("작업내용 :\n %s" % sqlStr)
    msg = { 'result' : 'NOT_OK'}
    print(vrfy.CMD_TYPE_CD)
    if ( vrfy.CMD_TYPE_CD == 'AURORA_SQL'):
        ret = run_sql(vrfy.DB_NM,vrfy.SCHEMA_NM,sqlStr)
        print(ret)
        msg['result'] =  'OK'
        msg['ret'] = ret
    else:
        msg['result'] = 'NOT_YET'
    #print(msg)
    return render(request, template_name, {'row' : vrfy ,'msg' : msg })

def run_sql(db,schema,sqlStr):
    ret = None 
    try:
        conn = Conn(db)
        conn.ssh_start()
        conn.dbConn()
        conn.select_db(schema)
        ret = conn.execute(sqlStr)
        ret = ret[0]['CNT']
    except Exception as e:
        print(e)
    finally :
        if ( conn is not None ):
            conn.close()
        return ret
########################## vrfy end ########################## 

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