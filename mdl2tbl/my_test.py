###########################################################################
#     Meta-eXpress 2.1 
#     All right reserved by wonseokyou 
#     email : wonseokyou@gmail.com 
###########################################################################
import os
import sys
import pymysql
from functools import reduce
from sshtunnel import SSHTunnelForwarder
from . import conn_info
##############################
# GET_TBL
# 테이블 데이터타입, NULL여부, DEFAULT값 가져오기 
##############################
def get_tbl(p_tbl_nm = "GD"):
    conn = None    
    TUNNEL_FLAG = 0    
    try:
        #conn = pymysql.connect(host='localhost', user='wsyou', password='wsyou',db='test', charset='utf8')
        if ( p_tbl_nm in ( 'ltcm','ltcmst','ltcmat', 'ltcmpr')):
            server_info = conn_info.server_infos['ltcm']
            source_tunnel = MakeTunnel(server_info["source_bastion_ip"],server_info["source_bastion_user"],server_info["source_bastion_pwd"],server_info["source_endpoint"])
            TUNNEL_FLAG = 1
            source_tunnel.start()
            conn = pymysql.connect(host='127.0.0.1', port=source_tunnel.local_bind_port, user=server_info["source_db_user"], password=server_info['source_db_pwd'], charset='UTF8')
        else :
            server_info = conn_info.server_infos['elltdev']
            source_tunnel = MakeTunnel(server_info["source_bastion_ip"],server_info["source_bastion_user"],server_info["source_bastion_pwd"],server_info["source_endpoint"])
            TUNNEL_FLAG = 1
            source_tunnel.start()
            conn = pymysql.connect(host='127.0.0.1', port=source_tunnel.local_bind_port, user=server_info["source_db_user"], password=server_info['source_db_pwd'], charset='UTF8')            
        try:
            curs = conn.cursor(pymysql.cursors.DictCursor)
            sql = """select table_schema `SCHEMA`
, upper(table_name)  TBL_NM
, upper(column_name) COL_NM
, ordinal_position POS
, COLUMN_TYPE DT
, IS_NULLABLE NULLABLE
, COLUMN_DEFAULT DEFT
from information_schema.columns a
where table_schema in ( 'x' 
,'elltdpdev'
,'elltomdev','elltpydev','elltlodev'
,'elltgddev'
,'elltchdev'
,'elltetdev'
,'elltprdev'
,'ellttmsdev'
,'elltacdev'
,'elltcmdev'
,'ltcmatdev'
,'ltcmstdev'
,'elltscdev'
,'elltccdev'
,'elltmbdev'
,'ltcmprdev'
)
  and table_schema like concat(lower(%(tbl_nm)s),'%%')
#  AND table_name like concat(lower(%(tbl_nm)s),'%%')
  and table_schema not like '%%back'
"""
            curs.execute(sql,{'tbl_nm' : p_tbl_nm})
            rows = curs.fetchall()
            return rows
        finally:
            curs.close()
    finally:
        if conn is not None:
            conn.close()
        if (TUNNEL_FLAG == 1):
            source_tunnel.stop()            
    return None
##############################
def MakeTunnel(bastion_ip,bastion_user,bastion_pwd,endpoint):
    '''ssh터널을 생성함'''
    tunnel=SSHTunnelForwarder(
        (bastion_ip, 22),
        ssh_username=bastion_user,
        ssh_password=bastion_pwd,
        remote_bind_address=(endpoint, 3306)
    )
    return tunnel
##############################
def get_qry( db , sql, sql_params = {} ):
    '''query와 파라미터를 전달해서 sql수행하는 함수'''
    conn = None
    TUNNEL_FLAG = 0    
    try:
        if ( db in ( 'ltcm','ltcmst','ltcmat', 'ltcmpr')):
            server_info = conn_info.server_infos['ltcm']
            source_tunnel = MakeTunnel(server_info["source_bastion_ip"],server_info["source_bastion_user"],server_info["source_bastion_pwd"],server_info["source_endpoint"])
            TUNNEL_FLAG = 1
            source_tunnel.start()
            #conn = pymysql.connect(host='127.0.0.1', port = 4309, user='b2_dba', password='qwer1234',db='ltcmdba', charset='utf8')
            conn = pymysql.connect(host='127.0.0.1', port=source_tunnel.local_bind_port, user=server_info["source_db_user"], password=server_info['source_db_pwd'], charset='UTF8')
        else :
            #conn = pymysql.connect(host='127.0.0.1', port = 3409, user='b2_dba', password='qwer1234',db='dbadev', charset='utf8')
            server_info = conn_info.server_infos['elltdev']
            source_tunnel = MakeTunnel(server_info["source_bastion_ip"],server_info["source_bastion_user"],server_info["source_bastion_pwd"],server_info["source_endpoint"])
            TUNNEL_FLAG = 1
            source_tunnel.start()
            #conn = pymysql.connect(host='127.0.0.1', port = 4309, user='b2_dba', password='qwer1234',db='ltcmdba', charset='utf8')
            conn = pymysql.connect(host='127.0.0.1', port=source_tunnel.local_bind_port, user=server_info["source_db_user"], password=server_info['source_db_pwd'], charset='UTF8')            
        try:
            curs = conn.cursor(pymysql.cursors.DictCursor)          
            curs.execute(sql,sql_params)
            rows = curs.fetchall()
            return rows
        finally:
            curs.close()
    finally:
        if conn is not None:
            conn.close()
        if (TUNNEL_FLAG == 1):
            source_tunnel.stop()
    return None

##############################
def get_tbl_src(p_tbl_nm = "GD"):
    '''원본테이블 데이터타입, NULL여부, DEFAULT값 가져오기'''
    sql = """select table_schema `SCHEMA`
, upper(table_name)  TBL_NM
, upper(column_name) COL_NM
, ordinal_position POS
, COLUMN_TYPE DT
, IS_NULLABLE NULLABLE
, COLUMN_DEFAULT DEFT
from information_schema.columns a
where table_schema in ( 'x' 
,'elltdpdev'
,'elltomdev','elltpydev','elltlodev'
,'elltgddev'
,'elltchdev'
,'elltetdev'
,'elltprdev'
,'ellttmsdev'
,'elltacdev'
,'elltcmdev'
,'ltcmatdev'
,'ltcmstdev'
,'elltscdev'
,'elltccdev'
,'elltmbdev'
,'ltcmprdev'
)
  and table_schema like concat(lower(%(tbl_nm)s),'%%')
  AND table_name not like '%%out'
  and table_schema not like '%%back'
"""
    rows = get_qry(p_tbl_nm,sql,{'tbl_nm' : p_tbl_nm })
    return rows
##############################
def get_tbl_out(p_tbl_nm = "GD"):
    '''복제본테이블(OUT) 데이터타입, NULL여부, DEFAULT값 가져오기''' 
    return get_qry(p_tbl_nm,"""select table_schema `SCHEMA`
, replace(upper(table_name),'_OUT','')  TBL_NM
, upper(column_name) COL_NM
, ordinal_position POS
, COLUMN_TYPE DT
, IS_NULLABLE NULLABLE
, COLUMN_DEFAULT DEFT
from information_schema.columns a
where table_schema in ( 'x' 
,'elltdpdev'
,'elltomdev','elltpydev','elltlodev'
,'elltgddev'
,'elltchdev'
,'elltetdev'
,'elltprdev'
,'ellttmsdev'
,'elltacdev'
,'elltcmdev'
,'ltcmatdev'
,'ltcmstdev'
,'elltscdev'
,'elltccdev'
,'elltmbdev'
,'ltcmprdev'
)
  and table_schema not like concat(lower(%(tbl_nm)s),'%%')
  AND table_name like '%%out'
  and table_schema not like '%%back'
""",{'tbl_nm' : p_tbl_nm})

##############################
# TEST START 
##############################
if __name__ == "__main__":
    sa = "CC"
    for arg in sys.argv[1:]:
        sa = arg
    print(sa)
    #OUT 테이블 속성 비교한는 방안
    #out_list = out테이블 목록을 가져옴[{테이블명}]
    out_list = get_qry(sa,"""select table_schema out_sch_nm,table_name out_tbl_nm, 
	   concat('ellt',lower(substr(table_name,1,2)),'dev') src_sch_nm,
       replace(table_name,'_out','') src_tbl_nm 
       from information_schema.tables 
where (table_schema like 'ellt%%dev' or table_schema like 'ltcm%%dev')
 and table_name like '%%out'""" )
    
    #out_in_list = out_list로 out테이블의 out테이블 query 를 생성함(in list로 만들음)
    out_in_list = reduce(lambda x, row : x + ",('{}','{}')".format(row['out_sch_nm'],row['out_tbl_nm']), out_list,"")
    out_in_list = "(" + out_in_list[1:] + ")"
    
    sql_base = """select table_schema `SCHEMA`
, replace(upper(table_name),'_OUT','')  TBL_NM
, upper(column_name) COL_NM
, ordinal_position POS
, COLUMN_TYPE DT
, IS_NULLABLE NULLABLE
, COLUMN_DEFAULT DEFT
from information_schema.columns a
 where (table_schema, table_name) in """
    #out_rows = out_in_list로 컬럼정보를 가지고옮 
    out_rows = get_qry(sa,sql_base + out_in_list )

    #src_in_list = out_list로 out테이블의 원본 query 를 생성함(in list로 만들음)
    src_in_list = reduce(lambda x, row : x + ",('{}','{}')".format(row['src_sch_nm'],row['src_tbl_nm']), out_list,"")
    src_in_list = "(" + src_in_list[1:] + ")"
    print(src_in_list)
     
    #src_rows = src_in_list로 컬럼정보를 가지고옮 ( { src_in_list ) )    

    # rows = get_tbl_src(sa)
    # for row in rows:
    #     print(row)
    # print("*"*80)
    # rows = get_tbl_src(sa)
    # for row in rows:
    #     print(row)