from dq.dbMysql import Conn as Conn

#sqlite 관련  merge Connection 처리
from dq.dbSqlite import Conn as mConn
DB_LIST = { 'dev' : ['ltcmdev','elltdev'] 
          , 'tst' : ['ltcmtst1','ellttst1','ellttst2','ellttst3','ellttst4','ellttst6']
          , 'prd' : ['ltcmprd1','elltprd1','elltprd2','elltprd3','elltprd4','elltprd6']          
          }
DB_LIST['all'] = list(DB_LIST['dev'])
DB_LIST['all'].extend(DB_LIST['tst'])
DB_LIST['all'].extend(DB_LIST['prd'])
def trace_out_table(p_table_nm,env):
    ldb = localDb()
    ldb.dbConn()  
    print('table_nm=>',p_table_nm,'env=>',env)
    try:  
        if env in ( 'dev','tst','prd','all') : 
            dbs = DB_LIST[env]
            ldb.cols = None              
            for db in dbs:
                rets1 = trace_out_table0(db,p_table_nm)       
                if ldb.cols == None :  
                    ldb.cols = rets1['cols']
                    ldb.create()
                cnt  = ldb.insert(rets1['rows'])
                ldb.lconn.commit()
                #print('cnt=>', cnt)             
                ldb.oschs.extend(rets1['osch'])
                ldb.schs.extend(rets1['schs'])
                #print('schs=>',ldb.schs)
            rows_all = ldb.select()
            cols_all = ldb.lconn.cols
            #print(cols_all)
            colspans = [ ( '' , 1 ) ]
            env_list = [1 for i in cols_all if 'dev' == i[-3:] ]
            if sum(env_list) > 0  :
                colspans.append(('dev',sum(env_list))) 
            env_list = [1 for i in cols_all if 'tst' == i[-3:] ]
            if sum(env_list) > 0 :
                colspans.append(('tst',sum(env_list))) 
            env_list = [1 for i in cols_all if 'prd' == i[-3:] ]            
            if sum(env_list) > 0 :
                colspans.append(('prd',sum(env_list))) 
            #print(colspans)
            rets = { 'ret' : "OK" , 'rows' : rows_all, 'cols' : cols_all, 'colspans' : colspans }   
        else :
            rets = { 'ret' : "NOT_OK" , 'rows' : None, 'cols' : None , 'colspans' : None }
    except Exception as e :
        print(e)
        rets = { 'ret' : "NOT_OK" , 'rows' : None, 'cols' : None , 'colspans' : None }
    finally: 
        ldb.close() 
        return rets


def trace_out_table0(p_db_nm,p_table_nm):
    conn = Conn(p_db_nm)
    try:
        conn.ssh.start()
        conn.sshDbConn()
        conn.param_replace = False

        sql1 = """
        select 'ORIG' DVS_CD,TABLE_SCHEMA from information_schema.tables where table_name = %(tbl_nm)s 
        and ( table_schema like 'ellt%%' or  table_schema like 'ltcm%%' )
        and ( table_schema not like 'elltetl%%' and table_schema not like 'elltmig%%')
        UNION ALL
        select 'COPY' DVS_CD,TABLE_SCHEMA from information_schema.tables where table_name = %(cpy_nm)s 
        and ( table_schema like 'ellt%%' or  table_schema like 'ltcm%%' )
        and ( table_schema not like 'elltetl%%' and table_schema not like 'elltmig%%')
        """

        tbl_nm = p_table_nm
        cpy_nm = tbl_nm + '_OUT'
        conn.curType = 'dict'

        rows1 = conn.execute(sql1,{'tbl_nm' : tbl_nm , 'cpy_nm' : cpy_nm })
        
        my_schs = [ row['TABLE_SCHEMA'] for row in rows1 if row['DVS_CD'] == 'COPY' ]
        my_osch = [ row['TABLE_SCHEMA'] for row in rows1 if row['DVS_CD'] == 'ORIG' ]
        # sqlite 에 저장한 결과를 가져오는 방법으로 처리하고자함.
        

        conn.curType = 'list'

        sql2 = """SELECT *
         from (
         select TABLE_SCHEMA sch,COLUMN_NAME col, COLUMN_TYPE col_type, ORDINAL_POSITION pos from information_schema.columns where table_name = %(tbl_nm)s
         and ( table_schema like 'ellt%%' or  table_schema like 'ltcm%%' )
         and ( table_schema not like 'elltetl%%' and table_schema not like 'elltmig%%')
         union all
         select TABLE_SCHEMA sch,COLUMN_NAME col, COLUMN_TYPE col_type, ORDINAL_POSITION pos from information_schema.columns where table_name = %(cpy_nm)s
         and ( table_schema like 'ellt%%' or  table_schema like 'ltcm%%' )
         and ( table_schema not like 'elltetl%%' and table_schema not like 'elltmig%%')
         ) a        
        order by 1,2"""        

        rows2 = conn.execute(sql2,{'tbl_nm' : tbl_nm , 'cpy_nm' : cpy_nm })
        rets = { 'ret' : "OK" , 'rows' : rows2, 'cols' : conn.cols , 'schs' : my_schs, 'osch' : my_osch }
    except Exception as e:
        rets = { 'ret' : "NOT_OK" , 'rows' : None, 'cols' : None , 'schs' : None }
    finally:
        conn.close()
    return rets

class localDb():
    def __init__(self,p_tbl_nm = "orig_copy"):
        self.tbl_nm = p_tbl_nm
        self.cols = None
        self.lconn = mConn("ldb.sqlite3")
        self.oschs = []
        self.schs = []
        return

    def dbConn(self):
        return self.lconn.dbConn()

    def make_create(self):
        sql3 = "create table " + self.tbl_nm + " ("
        sql3 += ''.join([ ',' + r + ' varchar(100) ' for r in self.cols])[1:]
        sql3 += ")"
        return sql3

    def create(self):
        create_sql = self.make_create()
        #print("create_sql=>",create_sql)
        drop_sql = "drop table if exists " + self.tbl_nm 
        print("drop_sql=>",drop_sql)
        self.lconn.execute(drop_sql)
        self.lconn.execute(create_sql)
        self.oschs = []
        self.schs = []
        return True

    def make_insert(self):
        sql4 = "insert into  " + self.tbl_nm + "  ("
        sql4 += ''.join([ ',' + r for r in self.cols])[1:]
        sql4 += ') values ('
        sql4 += ''.join([ ',?' for r in self.cols])[1:]
        sql4 += ')'
        return sql4

    def insert(self,rows2):        
        self.lconn.curType = 'list'
        insert_sql = self.make_insert()
        return self.lconn.executemany(insert_sql,rows2)

    def select(self):
        self.lconn.curType = 'list'
        sql2 = "SELECT col"
        #dev,tst,prd순서로 컬럼을 나열한다.
        # print('oschs=>',self.oschs)
        # print('schs=>',self.schs)
        for env in ['dev','tst','prd']:
            sub_schs = [i for i in self.oschs if env == i[-3:]]
            sql2 += "\n".join([ ", MAX(CASE WHEN sch = '%s' THEN pos END ) %s" % (sch,sch) for sch in sub_schs])
            sub_schs = sorted([i for i in self.schs if env == i[-3:]])
            sql2 += "\n".join([ ", MAX(CASE WHEN sch = '%s' THEN pos END ) %s" % (sch,sch) for sch in sub_schs])
        sql2 += """     
        from """ + self.tbl_nm + """ a
        group by col
        order by cast( """ + self.oschs[0] + " as int )"
        rows2 = self.lconn.execute(sql2)
        return rows2

    def close(self):
        if ( self.lconn is not None):
            self.lconn.close()

def matrix_out_table():
    conn = Conn('meta')
    try:
        #conn.ssh.start()
        conn.dbConn()
        conn.select_db('elltDQtst')
        conn.param_replace = False

        sql1 = """
 SELECT SRC
	 ,GROUP_CONCAT(CASE WHEN TGT = 'AT' THEN TABLE_NM END order by TABLE_NM SEPARATOR '<BR>' ) AT
	 ,GROUP_CONCAT(CASE WHEN TGT = 'CC' THEN TABLE_NM END order by TABLE_NM SEPARATOR '<BR>' ) CC
	 ,GROUP_CONCAT(CASE WHEN TGT = 'CH' THEN TABLE_NM END order by TABLE_NM SEPARATOR '<BR>' ) CH
	 ,GROUP_CONCAT(CASE WHEN TGT = 'CM' THEN TABLE_NM END order by TABLE_NM SEPARATOR '<BR>' ) CM
	 ,GROUP_CONCAT(CASE WHEN TGT = 'DP' THEN TABLE_NM END order by TABLE_NM SEPARATOR '<BR>' ) DP
	 ,GROUP_CONCAT(CASE WHEN TGT = 'ET' THEN TABLE_NM END order by TABLE_NM SEPARATOR '<BR>' ) ET
	 ,GROUP_CONCAT(CASE WHEN TGT = 'GD' THEN TABLE_NM END order by TABLE_NM SEPARATOR '<BR>' ) GD
	 ,GROUP_CONCAT(CASE WHEN TGT = 'MB' THEN TABLE_NM END order by TABLE_NM SEPARATOR '<BR>' ) MB
	 ,GROUP_CONCAT(CASE WHEN TGT = 'OM' THEN TABLE_NM END order by TABLE_NM SEPARATOR '<BR>' ) OM
	 ,GROUP_CONCAT(CASE WHEN TGT = 'OMBQ' THEN TABLE_NM END order by TABLE_NM SEPARATOR '<BR>' ) OM_BQ
	 ,GROUP_CONCAT(CASE WHEN TGT = 'PR' THEN TABLE_NM END order by TABLE_NM SEPARATOR '<BR>' ) PR
	 ,GROUP_CONCAT(CASE WHEN TGT = 'SC' THEN TABLE_NM END order by TABLE_NM SEPARATOR '<BR>' ) SC
	 ,GROUP_CONCAT(CASE WHEN TGT = 'SE' THEN TABLE_NM END order by TABLE_NM SEPARATOR '<BR>' ) SE
FROM (
SELECT
  concat('<span onClick="run_vrfy(''',TABLE_NM,''');" class="yws_pnt" >',TABLE_NM,'</span>') TABLE_NM,
  SUBSTR(TABLE_NM,1,2) SRC,
  UPPER(replace(JSON_EXTRACT(TABLE_COPY_EXPLN, CONCAT('$.TGT[', idx, ']')),'"','')) AS TGT
FROM dq_tablecopy
JOIN ( 
  SELECT  0 AS idx UNION ALL
  SELECT  1 AS idx UNION ALL
  SELECT  2 AS idx UNION ALL
  SELECT  3 AS idx UNION ALL
  SELECT  4 AS idx UNION ALL
  SELECT  5 AS idx UNION ALL
  SELECT  6 AS idx UNION ALL
  SELECT  7 AS idx UNION ALL
  SELECT  8 AS idx UNION ALL
  SELECT  9 AS idx UNION ALL
  SELECT  10 AS idx UNION ALL
  SELECT  11 AS idx UNION ALL
  SELECT  12 AS idx UNION ALL
  SELECT  13 AS idx UNION ALL
  SELECT  14 AS idx UNION ALL
  SELECT  15 AS idx UNION ALL
  SELECT  16 AS idx UNION ALL
  SELECT  17 AS idx UNION ALL
  SELECT  18 AS idx UNION ALL
  SELECT  19 AS idx UNION ALL
  SELECT  20
  ) AS indexes
WHERE JSON_EXTRACT(TABLE_COPY_EXPLN, CONCAT('$.TGT[', idx, ']')) IS NOT NULL
ORDER BY TABLE_NM
) A
GROUP BY SRC
ORDER BY SRC
        """
        tbl_nm = 'GD_GOODS'
        cpy_nm = tbl_nm + '_OUT'
        conn.curType = 'list'
        rows1 = conn.execute(sql1)
        rets = { 'ret' : "OK" , 'rows' : rows1, 'cols' : conn.cols }
    except Exception as e:
        rets = { 'ret' : "NOT_OK" , 'rows' : None, 'cols' : None }

    finally:
        conn.close()
    return rets    