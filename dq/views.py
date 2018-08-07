###########################################################################
#     Meta-eXpress 2.1 
#     All right reserved by wonseokyou 
#     email : wonseokyou@gmail.com 
###########################################################################
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseGone, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
import datetime,pytz,re #  날짜를 파싱하기위한 정규식 처리 
from django import forms

from django.conf import settings
# Create your views here.
############################## json ##############################
import json
############################## dbConn  ##############################
from .models import * 
from .forms import *
from .dbMysql import Ssh,Conn,get_db_sch_nm
############################## task  ##############################
from django.views.decorators.csrf import csrf_exempt
from logging import getLogger
from .tasks import demo_task,vrfy_task,vrfy_task_aurora

# 쿼리 OR조건을 위해서 import 함 
from django.db.models import Q
############################## Transaction 매뉴얼관리  ##############################
from django.db import transaction, connection
############################## out 테이블관리 시작 ##############################
from .out_table import trace_out_table,matrix_out_table
############################## 공통 함수 및 class  ##############################
from .funcs import * 


app_name ='dq'
########################## 공통 함수 ########################## 
def dummy(request, template_name='dummy.html'):
    data = {}
    data['object_list'] = getattr(settings, "BASE_DIR", None)
    data['app_name'] = app_name
    return render(request, template_name, data)

def base(request, template_name='base.html'):
    data = {}
    data['object_list'] = getattr(settings, "BASE_DIR", None)
    return render(request, template_name, data)
   
########################## task start ########################## 
logger = getLogger(__name__)

@csrf_exempt
def tasks(request):
    if request.method == 'POST':
        return _post_tasks(request)
    else:
        return JsonResponse({}, status=405)

def _post_tasks(request):
    message = request.POST['message']
    logger.debug('calling demo_task. message={0}'.format(message))
    demo_task(message)
    return JsonResponse({}, status=302)
 

########################## vrfy start ########################## 

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
        vrfys = Vrfy.objects.filter(TABLE_NM = qry)
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
    '''직접 수행된 결과를 보여준다'''   
    vrfy = get_object_or_404(Vrfy, pk=pk)
    sqlStr = vrfy.CMD_CNTS
    print('*'*40)
    print("시작시간 : %s" % datetime.datetime.now() )
    print("작업번호 : %s" % vrfy.VRFY_NO)
    print("작업명  : %s" % vrfy.VRFY_NM)
    # print("작업내용 :\n %s" % sqlStr)
    msg = { 'result' : 'NOT_OK'}
    try:
        if ( vrfy.CMD_TYPE_CD == 'AURORA_SQL'):
            rets = run_sql(vrfy.DB_NM,vrfy.SCHEMA_NM,sqlStr)
            ret = rets['ret']
            print(ret)
            msg['result'] =  'OK'
            msg['ret'] = ret            
        else:
            msg['result'] = 'NOT_YET'
    except Exception as e:
        print(e)
    vrfyLog_create(vrfy,rets)
    return render(request, template_name, {'row' : vrfy ,'msg' : msg })

def run_sql(db,schema,sqlStr):
    ret = None
    strt_dttm = timezone.now()
    try:
        conn = Conn(db)
        conn.ssh.start()
        conn.sshDbConn()
        conn.select_db(schema)
        ret = conn.execute(sqlStr)
        if (len(ret) == 0 ) :
            ret = 0 # 결과가 없으면 0으로 간주함.
        elif ( 'CNT' in ret[0]  ) :
            ret = ret[0]['CNT']
        elif ('cnt' in ret[0] )  :
            ret = ret[0]['cnt'] 
        else:
            pass
    except Exception as e:
        print(e)
        ret = 'ERR'
    finally :
        if ( conn is not None ):
            conn.close()
        end_dttm = timezone.now()         
        rets = { 'ret' : ret , 'strt_dttm' : strt_dttm, 'end_dttm' : end_dttm } 
        return rets
########################## 오로라 검증 (단건 작업 수행) ########################## 
@csrf_exempt
def vrfy_tasks(request):
    '''검증TASK를 수행한 작업을 SUBMIT 한다'''
    pk = request.GET['pk']
    if request.GET.get('env'):
        env = request.GET['env']
    else:
        env = 'dev'
    vrfy = get_object_or_404(Vrfy, pk=pk)    
    if vrfy != None :       
        logger.debug('vrfy_task({0})'.format(pk))
        message = { 'VRFY_NO': vrfy.VRFY_NO 
                  , 'env'  : env
                  }
        vrfy_task(message)
        context = { 'message' : {'DB_NM' : vrfy.DB_NM
                                , 'SCHEMA_NM' : vrfy.SCHEMA_NM
                                , 'VRFY_NO': vrfy.VRFY_NO
                                , 'VRFY_NM': vrfy.VRFY_NM
                                , 'VRFY_EXPLN' : vrfy.VRFY_EXPLN
                                , 'CMD_CNTS' : vrfy.CMD_CNTS
                                , 'VRFY_RSLT_VAL' : '작업이 정상적으로 제출되었습니다.\n Log를 확인해주세요'
                                },
                    'ret'  : 'OK'
                }
    else:
        context = { 'message' : { 'DB_NM' : '데이터없음'
                                , 'SCHEMA_NM' : '데이터없음'
                                , 'VRFY_NO': 0
                                , 'VRFY_NM': '데이터없음'
                                , 'VRFY_EXPLN' : '데이터없음'
                                , 'CMD_CNTS' : '데이터없음'
                                , 'VRFY_RSLT_VAL' :'작업제출 ERROR!!!!'
                                },
                    'ret'  : 'NOT_OK'
                } 
    return HttpResponse(json.dumps(context), content_type="application/json")

def vrfy_job(pk,env='dev'):
    '''TASK에 의해 수행되면 검증번호pk 작업을 수행한다.'''    
    vrfy = get_object_or_404(Vrfy, pk=pk)
    sqlStr = vrfy.CMD_CNTS
    print('*'*40)
    print("시작시간 : %s" % datetime.datetime.now() )    
    print("작업번호 : %s" % vrfy.VRFY_NO)
    print("작업명  : %s" % vrfy.VRFY_NM)
    # print("작업내용 :\n %s" % sqlStr)
    msg = { 'ret' : 'NOT_OK'}
    dbNm , schNm = get_db_sch_nm(vrfy.DB_NM,vrfy.SCHEMA_NM,env)
    try:
        if ( vrfy.CMD_TYPE_CD == 'AURORA_SQL'):
            rets = run_sql(dbNm,schNm,sqlStr)
            ret = rets['ret']
            print("수행결과 : %s" % ret)
            print("종료시간 : %s" % datetime.datetime.now() )   
            msg['ret'] =  'OK'
            msg['run_sql_ret'] = ret
        else:
            msg['ret'] = 'NOT_YET'
            ret = -1
    except Exception as e:
        print(e)
        ret = -1
    vl = vrfyLog_create(vrfy,rets,env)
    return JsonResponse( {'ret' : msg['ret'] , 'VRFY_NO' : vrfy.VRFY_NO, 'VRFY_LOG_NO' : vl.VRFY_LOG_NO },status=302)
########################## 오로라 검증 스케쥴 ########################## 
@csrf_exempt
def vrfy_tasks_aurora(request):
    if request.method == 'POST':
        env = request.POST['env']
        print('*'*40)        
        print('env=>',env)
        print('*'*40)   
        vrfy_task_aurora({'env' : env })
        return JsonResponse({'ret' : 'OK'}, status=302)
    else:
        return JsonResponse({'ret' : 'NOK_OK'}, status=405)   

def vrfy_job_aurora(env):
    '''명령유형코드중 AURORA_SQL을 찾아서 모두 수행한다.'''
    vs = Vrfy.objects.filter(Q(CMD_TYPE_CD = 'AURORA_SQL') & Q(USE_YN = 'Y') )
    for i in vs:
        vrfy_job(i.VRFY_NO,env)
    return True        
########################## vrfy Log ##########################
def vrfyLog_list(request, template_name='vrfyLog_list.html'):
    gets = request.GET
    #print(gets)    
    qry = gets['qry'] if ( 'qry' in gets ) else ''
    dates = gets['dates'] if ( 'dates' in gets ) else '' 
    date1, date2, dt_ary = get_datetime_range(dates)
    if (qry == None or len(qry) < 1):
        if ( date1 == None or date2 == None ):
            vrfyLogs = VrfyLog.objects.all()
        else:
            vrfyLogs = VrfyLog.objects.exclude(MODI_DTTM__lt=date1).exclude(MODI_DTTM__gt=date2)            
    else:
        if ( date1 == None or date2 == None ):
            vrfyLogs = VrfyLog.objects.filter(VRFY_NO=qry)
        else:
            vrfyLogs = VrfyLog.objects.filter(VRFY_NO=qry).exclude(MODI_DTTM__lt=date1).exclude(MODI_DTTM__gt=date2)

    data = {}
    data['gets'] = gets
    ################### env 필터  ###################
    env  = gets['env'] if ( 'env' in gets ) else 'all'             
    if ( env in [ 'dev','tst','prd'] ):
        vrfyLogs = vrfyLogs.filter(SCHEMA_NM__endswith= env )
    ################### env 필터  ###################
    errYn  = gets['errYn'] if ( 'errYn' in gets ) else ''         
    if ( errYn == 'on' ):
        vrfyLogs = vrfyLogs.filter(VRFY_RSLT_VAL__gt = '0' )
    
    data['object_list'] = vrfyLogs
    if ( date1 == None or date2 == None ):
        data['dates'] = [ '', '']
    else :
        data['dates'] = dt_ary
    form = vrfyLogForm(request.GET or None )
    data['form'] = form
    return render(request, template_name, data)


def vrfyLog_create(vrfy,rets,env='dev'):
    print("Start vrfyLog save")    
    try:
        # get dbConnection
        v = vrfy
        vl = VrfyLog()
        vl.VRFY_NO = v
        vl.VRFY_NM = v.VRFY_NM
        vl.DB_NM, vl.SCHEMA_NM =  get_db_sch_nm(v.DB_NM,v.SCHEMA_NM,env)
        vl.CMD_TYPE_CD = v.CMD_TYPE_CD
        vl.CMD_CNTS = v.CMD_CNTS
        vl.VRFY_RSLT_VAL = str(rets['ret'])
        vl.STRT_DTTM = rets['strt_dttm']
        vl.END_DTTM = rets['end_dttm']
        #vl.save()
        vrfyLog_save(vl,env)        
        print("End vrfyLog save")
    except Exception as e :
        print(e)
        return None
    else : 
        return vl
        
def vrfyLog_save(vl,env='dev'):
    '''pymysql을 이용해서  log를 별도의 db session으로 저잫함.'''
    sqlTmpl = '''insert into DQ_VRFYLOG (
                    VRFY_NM
                ,CMD_TYPE_CD
                ,CMD_CNTS
                ,RGSTR_ID
                ,RGST_DTTM
                ,MODR_ID
                ,MODI_DTTM
                ,VRFY_NO_id
                ,VRFY_RSLT_VAL
                ,DB_NM
                ,SCHEMA_NM
                ) 
            VALUES ('%s','%s','%s'
                    ,'DA',convert('%s', DATETIME),'DA',convert('%s', DATETIME)
                    ,'%s','%s','%s','%s')'''
    sqlStr = sqlTmpl % (
                    vl.VRFY_NM
                ,vl.CMD_TYPE_CD
                ,str.replace(vl.CMD_CNTS,"'","''")

                ,vl.STRT_DTTM.strftime('%Y-%m-%d %H:%M:%S')
                ,vl.END_DTTM.strftime('%Y-%m-%d %H:%M:%S')

                ,(vl.VRFY_NO).VRFY_NO
                ,vl.VRFY_RSLT_VAL
                ,vl.DB_NM
                ,vl.SCHEMA_NM
                )                     
    #print(sqlStr)
    conn = Conn('meta')
    try: 
        conn.dbConn()
        conn.select_db('elltdqtst')
        conn.execute(sqlStr)
        conn.commit()
    except Exception as e :
        print(e)
    finally:
        conn.close()

########################## vrfy Log 단건조회 ##########################
def vrfyLog_ajax_view(request):
    qry = request.GET['pk']
    #print("qry=>",qry)
    obj = None
    try: 
        obj = VrfyLog.objects.get(VRFY_LOG_NO=qry)
        context = { 'message' : { 'VRFY_LOG_NO': obj.VRFY_LOG_NO 
                                , 'DB_NM' : obj.DB_NM
                                , 'SCHEMA_NM' : obj.SCHEMA_NM
                                , 'VRFY_NO': obj.VRFY_NO.VRFY_NO
                                , 'VRFY_NM': obj.VRFY_NM
                                , 'VRFY_EXPLN' : obj.VRFY_NO.VRFY_EXPLN
                                , 'CMD_CNTS' : obj.CMD_CNTS
                                , 'VRFY_RSLT_VAL' : obj.VRFY_RSLT_VAL
                                },
                    'ret'  : 'OK'
                }
    except Exception as e :
        context = { 'message' : { 'VRFY_LOG_NO': 0 
                                , 'DB_NM' : '데이터없음'
                                , 'SCHEMA_NM' : '데이터없음'
                                , 'VRFY_NO': 0
                                , 'VRFY_NM': '데이터없음'
                                , 'VRFY_EXPLN' : '데이터없음'
                                , 'CMD_CNTS' : '데이터없음'
                                , 'VRFY_RSLT_VAL' :'데이터없음'
                                },
                    'ret'  : 'NOT_OK'
                }     
    return HttpResponse(json.dumps(context), content_type="application/json")
########################## vrfy Log 수행 ##########################
def vrfyLog_ajax(request):
    qry = request.GET['pk']
    #print("qry=>",qry)
    obj = None
    try: 
        v = Vrfy.objects.get(VRFY_NO = qry)
        rets = run_sql(v.DB_NM,v.SCHEMA_NM,v.CMD_CNTS)
        ret = rets['ret']
        obj = vrfyLog_create(v,rets)
        obj.save()
        #obj = VrfyLog.objects.get(VRFY_LOG_NO=qry)
        #print(obj)
        context = { 'message' : { 'VRFY_LOG_NO': obj.VRFY_LOG_NO 
                                , 'DB_NM' : obj.DB_NM
                                , 'SCHEMA_NM' : obj.SCHEMA_NM
                                , 'VRFY_NO': obj.VRFY_NO.VRFY_NO
                                , 'VRFY_NM': obj.VRFY_NM
                                , 'VRFY_EXPLN' : obj.VRFY_NO.VRFY_EXPLN
                                , 'CMD_CNTS' : obj.CMD_CNTS
                                , 'VRFY_RSLT_VAL' : obj.VRFY_RSLT_VAL
                                },
                    'ret'  : 'OK'
                }
    except Exception as e :
        context = { 'message' : { 'VRFY_LOG_NO': 0 
                                , 'DB_NM' : '데이터없음'
                                , 'SCHEMA_NM' : '데이터없음'
                                , 'VRFY_NO': 0
                                , 'VRFY_NM': '데이터없음'
                                , 'VRFY_EXPLN' : '데이터없음'
                                , 'CMD_CNTS' : '데이터없음'
                                , 'VRFY_RSLT_VAL' :'데이터없음'
                                },
                    'ret'  : 'NOT_OK'
                }     
    return HttpResponse(json.dumps(context), content_type="application/json")
########################## 데이터 복제본 추적관리  ##########################

def tblCpy_list(request, template_name='tblCpy_list.html'):
    gets = request.GET
    #print(gets)
    if ( 'qry' in gets ) :
        qry = gets['qry']
    else:
        qry = ''
    if (qry == None or len(qry) <= 2):
        tblCpys = TableCopy.objects.all()
    else:
        tblCpys = TableCopy.objects.filter(TABLE_NM = qry)
    data = {}
    data['object_list'] = tblCpys
    data['gets'] = gets
    return render(request, template_name, data)

    
def tblCpy_list2(request, template_name='tblCpy_list2.html'):
    form = None
    try:
        rets = matrix_out_table()
        #print(request.GET)
        form = EnvForm(request.GET or None )
        #answer = ''
        #if form.is_valid():
        #    answer = form.cleaned_data.get('qry')             
        rets['form'] = form
    except Exception as e :
        print(e)
        rets = { 'ret' : "NOT_OK" , 'rows' : None, 'cols' : None , 'form' : form }    
    return render(request, template_name, rets)    

def tblCpy_create(request, template_name='tblCpy_form.html'):
    form = TableCopyForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('dq:tblCpy_list')
    return render(request, template_name, {'form':form})

def tblCpy_update(request, pk,template_name='tblCpy_form.html'):    
    tblCpy = get_object_or_404(TableCopy, pk=pk)
    form = TableCopyForm(request.POST or None, instance=tblCpy)
    if form.is_valid():
        form.save()
        return redirect('dq:tblCpy_list')
    return render(request, template_name, {'form':form,'row' : tblCpy })

def tblCpy_delete(request, pk):
    tblCpy= get_object_or_404(TableCopy, pk=pk)    
    if tblCpy != None :
        tblCpy.delete()
        return redirect('dq:tblCpy_list')
    return HttpResponse(status=405)

def tblCpy_ajax(request):
    pk = request.GET['pk']
    if request.GET.get('env'):
        env = request.GET['env']
    else:
        env = 'dev'
    try:
        #v = get_object_or_404(TableCopy, pk=pk)     
        context = trace_out_table(pk,env)
    except Exception as e :
        print(e)
        context = { 'ret' : "NOT_OK" , 'rows' : None, 'cols' : None }    
    return HttpResponse(json.dumps(context), content_type="application/json")

########################## ilm ########################## 

def ilm_list(request, template_name='ilm_list.html'):
    gets = request.GET
    #print(gets)
    if ( 'qry' in gets ) :
        qry = gets['qry']
    else:
        qry = ''
    if (qry == None or len(qry) <= 2):
        objs = Ilm.objects.all()
    else:
        objs = Ilm.objects.filter(TABLE_NM = qry)
    data = {}
    data['object_list'] = objs
    data['gets'] = gets
    return render(request, template_name, data)

def ilm_create(request, template_name='ilm_form.html'):
    form = IlmForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('dq:ilm_list')
    return render(request, template_name, {'form':form})

def ilm_update(request, pk,template_name='ilm_form.html'):    
    obj = get_object_or_404(Ilm, pk=pk)
    form = IlmForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('dq:ilm_list')
    return render(request, template_name, {'form':form,'row' : obj })

def ilm_delete(request, pk):
    obj = get_object_or_404(Ilm, pk=pk)    
    if obj != None :
        obj.delete()
        return redirect('dq:ilm_list')
    return HttpResponse(status=405)

########################## vrfy_Cmd ########################## 

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