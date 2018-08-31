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
    고객명 대상 컬럼목록
    '''
    return get_qry("SELECT * FROM DA05.고객명")    

##############################
def get_man_col():
    '''
    개인정보 대상 컬럼목록
    '''
    return get_qry("SELECT * FROM DA05.개인정보")   
##############################
def get_cd_defi():
    '''
    코드정의서
    '''
    return get_qry("SELECT * FROM DA05.코드정의서")  

##############################
# GET_ATTR_USE_TBL
# 컬럼 사용 테이블
##############################
def get_attr_use_tbl(p_attr_nm = "GD"):
    return get_qry("""SELECT A.ATTR_NM, A.COL_NM,       
      A.DT ,     
      A.TBL_NMS
FROM DA05.컬럼사용테이블 A
WHERE ATTR_NM LIKE :attr_nm """,{'attr_nm': p_attr_nm})

##############################
# GET_COL_USE_TBL
# 컬럼 사용 테이블
##############################
def get_col_use_tbl(p_col_nm = "GD"):
    return get_qry("""SELECT A.ATTR_NM, A.COL_NM,
      A.DT ,     
      A.TBL_NMS
FROM DA05.컬럼사용테이블 A
WHERE COL_NM LIKE :col_nm """,{'col_nm': p_col_nm})

##############################
# GET_PVIEW
# 물리모델 테이블 목록 
# ##############################
def get_PView(p_MDL_NM = "판촉_이벤트[PR]", p_STRU_NM = '외부참조' ):
    return get_qry("""SELECT M.MDL_ID, M.MDL_NM, C.STRU_ID, C.STRU_NM 
     , P.CANVAS_ID CNVAS_ID 
FROM   (SELECT *
        FROM   DA05.DAM_MDL_INFO M
        WHERE  AVAL_END_DT = '99991231235959'
         AND   MDL_NM = '""" + p_MDL_NM + """' ) M
    ,  (SELECT * 
        FROM DAM_MDL_CONTAINER
        WHERE AVAL_END_DT = '99991231235959'
         AND  STRU_NM = '""" + p_STRU_NM + """' ) C
    ,  (SELECT *  
        FROM DAM_PANE
        WHERE AVAL_END_DT = '99991231235959'
        AND TGT_DB_ID IS NOT NULL  ) P
WHERE M.MDL_ID = C.MDL_ID
AND C.MDL_ID = P.MDL_ID AND C.STRU_ID =  P.SBJ_FLD_ID 
""")

##############################
# GET_PVIEW
# 물리모델 컬럼 목록
##############################
def get_PView2(p_MDL_ID = "fd6e456a-347c-4c08-90bd-506e96e0e2fc" , p_CNVAS_ID = "587cb8ca-dcf5-49c0-8c72-c9a8989bee69"):
    sql = """WITH BAS AS (
    SELECT *
    FROM DAG_DRAWITEM
    WHERE  AVAL_END_DT = '99991231235959'
    AND MDL_ID = '""" + p_MDL_ID + """'
    AND CNVAS_ID = '""" + p_CNVAS_ID + """'
    )
SELECT 
CNVAS_ID,EXTRN_OBJ_ID,BASEVAL_ITEM_ID,TXT,NODE_SEQ,EXCOL02,EXCOL05,EXCOL07
, DRAW_ITEM_ORGIN_COORD, DRAW_ITEM_RECT, FNT, FNT_COLOR
FROM BAS
START WITH CLSS_DSTNCT_CD = '6'
CONNECT BY NOCYCLE PRIOR DRAW_ITEM_ID = BASEVAL_ITEM_ID
ORDER BY BASEVAL_ITEM_ID, node_seq NULLS LAST"""
    return get_qry(sql)

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