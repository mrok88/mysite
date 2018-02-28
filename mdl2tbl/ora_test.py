import os
import cx_Oracle
##############################
# GET_MDL
##############################
def get_mdl(p_tbl_nm = "GD"):
    dsn = cx_Oracle.makedsn("10.131.81.141", 1521, "MROK")
    os.putenv('NLS_LANG', '.UTF8')
    conn = None    
    try:
        conn = cx_Oracle.connect("MIGUSER", "mig0987", dsn)
        try:
            curs = conn.cursor()
            sql = "SELECT * FROM comp_mdl where tbl_nm like :tbl_nm||'%' and schema like 'ellt'||lower(substr(:tbl_nm,1,2))||'%'"
            curs.execute(sql,{'tbl_nm': p_tbl_nm})
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
# TEST START 
##############################
if __name__ == "__main__":
    rows = get_mdl("GD")
    for row in rows:
        print(row)