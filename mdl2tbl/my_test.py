import os
import pymysql
##############################
# GET_TBL
##############################
def get_tbl(p_tbl_nm = "GD"):
    conn = None    
    try:
        #conn = pymysql.connect(host='localhost', user='wsyou', password='wsyou',db='test', charset='utf8')
        conn = pymysql.connect(host='127.0.0.1', port = 3409, user='b2_dba', password='qwer1234',db='dbadev', charset='utf8')
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
)
  and table_schema like concat('ellt',lower(%(tbl_nm)s),'%%')
  AND table_name like concat(lower(%(tbl_nm)s),'%%')
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
    return None
##############################
# TEST START 
##############################
if __name__ == "__main__":
    rows = get_tbl("GD")
    for row in rows:
        print(row)