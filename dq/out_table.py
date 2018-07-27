from dq.dbMysql import Conn as Conn

def trace_out_table(p_table_nm,env):
    conn = Conn('elltdev')
    try:
        conn.ssh.start()
        conn.sshDbConn()
        conn.param_replace = False

        sql1 = """
        select 'ORIG' DVS_CD,TABLE_SCHEMA from information_schema.tables where table_name = %(tbl_nm)s
        UNION ALL
        select 'COPY' DVS_CD,TABLE_SCHEMA from information_schema.tables where table_name = %(cpy_nm)s 
        """

        tbl_nm = 'GD_GOODS'
        cpy_nm = tbl_nm + '_OUT'
        conn.curType = 'dict'

        rows1 = conn.execute(sql1,{'tbl_nm' : tbl_nm , 'cpy_nm' : cpy_nm })

        conn.curType = 'list'
        sql2 = "SELECT col"
        sql2 += "\n".join([ ", MAX(CASE WHEN sch = '%s' THEN pos END ) %s" % (row['TABLE_SCHEMA'],row['TABLE_SCHEMA']) for row in rows1])
        sql2 += """     
        from (
        select TABLE_SCHEMA sch,COLUMN_NAME col, COLUMN_TYPE col_type, ORDINAL_POSITION pos from information_schema.columns where table_name = %(tbl_nm)s
        union all
        select TABLE_SCHEMA sch,COLUMN_NAME col, COLUMN_TYPE col_type, ORDINAL_POSITION pos from information_schema.columns where table_name = %(cpy_nm)s
        ) a
        group by col
        order by 2"""

        rows2 = conn.execute(sql2,{'tbl_nm' : tbl_nm , 'cpy_nm' : cpy_nm })
        rets = { 'ret' : "OK" , 'rows' : rows2, 'cols' : conn.cols }
    except Exception as e:
        rets = { 'ret' : "NOT_OK" , 'rows' : None, 'cols' : None }

    finally:
        conn.close()
    return rets