###########################################################################
#     Meta-eXpress 2.1 
#     All right reserved by wonseokyou 
#     email : wonseokyou@gmail.com 
###########################################################################
import os
import sys
import cx_Oracle
from . import conn_info
##############################
# GET_QRY
# 쿼리와 파라미터를 받아서 Dict 형태로 return한다 
# 없을 경우 None을 return한다 
##############################
def get_qry(sql,sql_params = {} ):
    server_info = conn_info.server_infos['da05']  
    dsn = cx_Oracle.makedsn(server_info['source_endpoint'], server_info['source_endpoint_port'], server_info['source_endpoint_sid'])
    os.putenv('NLS_LANG', '.UTF8')
    conn = None    
    try:
        conn = cx_Oracle.connect(server_info['source_db_user'], server_info['source_db_pwd'], dsn)
        try:
            curs = conn.cursor()
            curs.execute(sql,sql_params)
            recs = curs.fetchall()
            rows = []
            for rec in recs:
                row = dict(zip([d[0] for d in curs.description], rec))
                rows.append(row)            
            return rows
        finally:
            curs.close()
    finally:
        if conn is not None:
            conn.close()
    return None
##############################
# GET_MDL
# 모델 데이터타입, NULL여부, DEFAULT값 가져오기 
##############################
def get_mdl(p_tbl_nm = "GD"):
    return get_qry("SELECT * FROM DA05.모델비교 where schema like lower(:tbl_nm)||'%'",{'tbl_nm': p_tbl_nm}) 
   
##############################
# GET_CAPA
# 테이블 용량 및 Lift Cycle 관리 정보 
##############################
def get_capa(p_tbl_nm = "GD"):
    return get_qry("SELECT * FROM DA05.데이터수명주기 where schema like lower(:tbl_nm)||'%' ",{'tbl_nm': p_tbl_nm})    

##############################
# GET_DEFI
# 테이블 용량 및 정의서
##############################
def get_defi(p_tbl_nm = "GD"):
    return get_qry("SELECT * FROM DA05.테이블정의서 where schema like lower(:tbl_nm)||'%' ",{'tbl_nm': p_tbl_nm})    

##############################
# GET_DEFI_COL
# 컬럼 정의서
##############################
def get_defi_col(p_tbl_nm = "GD"):
    return get_qry("""SELECT A.MDL_NM, A.ENT_NM, A.TBL_NM, A.COL_NM,A.ATTR_NM, A.DT, A.NULLABLE, A.DEFT
,ROW_NUMBER() OVER ( PARTITION BY MDL_NM, TBL_NM ORDER BY ENT_TYPE, ORD ) POS
,A.DEFI
FROM DA05.컬럼정의서 A
WHERE TBL_NM = upper(:tbl_nm)""",{'tbl_nm': p_tbl_nm})    



##############################
def get_enc_list():
    '''
    암호화 대상에 대한 정보
    '''
    #return get_qry("SELECT * FROM DA05.암호화대상여부")
    return get_qry("SELECT * FROM DA05.암호화")

##############################
def get_mask_list():
    '''
    마스킹 대상에 대한 정보  
    '''
    #return get_qry("SELECT * FROM DA05.마스킹대상여부")
    return get_qry("SELECT * FROM DA05.마스킹")

##############################
def get_emp_col():
    '''
    직원명 대상 컬럼목록
    '''
    return get_qry("SELECT * FROM DA05.직원명")    

##############################
def get_cust_col():
    '''
    곡객명 대상 컬럼목록
    '''
    return get_qry("SELECT * FROM DA05.고객명")    

##############################
def get_cd_defi():
    '''
    코드정의서
    '''
    return get_qry("SELECT * FROM DA05.코드정의서")  

##############################
# TEST START 
##############################
if __name__ == "__main__":
    sa = "CC"
    for arg in sys.argv[1:]:
        sa = arg  
    rows = get_mdl(sa)
    #rows = get_capa("GD")
    for row in rows:
        print(row)
    #tbls = set(row['TBL_NM'] for row in rows)
    #print(tbls)