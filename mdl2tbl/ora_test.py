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
    return get_qry("SELECT * FROM DA05.컬럼정의서 where schema like lower(:tbl_nm)||'%' ",{'tbl_nm': p_tbl_nm})    



##############################
# GET_ENC
# 암호화 대상에 대한 정보  
##############################
def get_enc_list():
    return get_qry("SELECT * FROM DA05.암호화대상여부")

##############################
# GET_MASKING
# 마스킹 대상에 대한 정보  
##############################
def get_mask_list():
    return get_qry("SELECT * FROM DA05.마스킹대상여부")
     
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