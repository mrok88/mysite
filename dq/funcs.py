# 공통 함수 및 클래스 
import datetime,pytz,re #  날짜를 파싱하기위한 정규식 처리 

TIME_ZONE = 'Asia/Seoul'

def get_datetime_range(dates):
    if dates == '' :
        return None,None,[]
    p = re.compile('\d{4}-\d{2}-\d{2}')
    dt_ary = p.findall(dates)
    date1 = get_datetime(dt_ary[0])
    date2 = get_datetime(dt_ary[1],False)
    return date1,date2,dt_ary

def get_date(dt_str):
    dt = None
    try:
        p = re.compile('(\d{4})-(\d{2})-(\d{2})')
        m = p.findall(dt_str)
        dt = datetime.date(int(m[0][0]), int(m[0][1]), int(m[0][2]))
    except Exception as e :
        print(e)        
    finally : 
        return dt

def get_datetime(dt_str,isStart = True):
    dt = None
    try:
        p = re.compile('(\d{4})-(\d{2})-(\d{2})')
        m = p.findall(dt_str)
        if isStart :
            dt = datetime.datetime(int(m[0][0]), int(m[0][1]), int(m[0][2]),0,0,0,0000000, tzinfo=pytz.timezone(TIME_ZONE))
        else :
            dt = datetime.datetime(int(m[0][0]), int(m[0][1]), int(m[0][2]),23,59,59,999999, tzinfo=pytz.timezone(TIME_ZONE))
    except Exception as e :
        print(e)        
    finally : 
        return dt