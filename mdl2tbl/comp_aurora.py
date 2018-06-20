# -*- coding: utf-8 -*-
import os
import sys
import pymysql
from functools import reduce
from sshtunnel import SSHTunnelForwarder
from . import conn_info
#import conn_info
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
def aurora_qry( db , sql, sql_params = {} ):
    '''query와 파라미터를 전달해서 sql수행하는 함수'''
    conn = None
    TUNNEL_FLAG = 0    
    try:
        #conn = pymysql.connect(host='127.0.0.1', port = 3409, user='b2_dba', password='qwer1234',db='dbadev', charset='utf8')
        server_info = conn_info.server_infos[db]
        source_tunnel = MakeTunnel(server_info["source_bastion_ip"],server_info["source_bastion_user"],server_info["source_bastion_pwd"],server_info["source_endpoint"])
        TUNNEL_FLAG = 1
        source_tunnel.start()
        #conn = pymysql.connect(host='127.0.0.1', port = 4309, user='b2_dba', password='qwer1234',db='ltcmdba', charset='utf8')
        conn = pymysql.connect(host='127.0.0.1', port=source_tunnel.local_bind_port, user=server_info["source_db_user"], password=server_info['source_db_pwd'], charset='UTF8')            
        try:
            #curs = conn.cursor(pymysql.cursors.DictCursor)          
            curs = conn.cursor()          
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

def compare_table(source_table_list,target_table_list):
    if len(source_table_list)==0:
        print("소스테이블없음")
        return "",""
    elif len(target_table_list)==0:
        print("타겟테이블없음")
        return "",""
    ret = []
    #print("###### 테이블 비교 ##########")
    #print("table_name,engine,row_format,table_collation,table_comment")
    target_not_exists = "''"
    source_not_exists = "''"
    for source_table in source_table_list:
        sametable_flag=0
        for target_table in target_table_list:
            if source_table[0] == target_table[0]:
                sametable_flag=1
                if source_table != target_table:
                    src_str = source_table[0] + ',' + source_table[4]
                    tgt_str = target_table[0] + ',' + target_table[4]
                    # print("소스: "+ src_str )
                    # print("타겟: "+ tgt_str )
                    ret.append({ 'TYP' : 'TBL', 'SRC' : src_str , 'TGT' : tgt_str , 'ETC' : '' })
        if sametable_flag==0:
            target_not_exists=target_not_exists+",'"+source_table[0]+"'"
            # print(source_table[0] + " 테이블 타겟에 없음")
            src_str = source_table[0] + ',' +  source_table[4]
            tgt_str = " 테이블 타겟에 없음"
            ret.append({ 'TYP' : 'TBL', 'SRC' : src_str , 'TGT' :  tgt_str , 'ETC' : ''})
                    
    for target_table in target_table_list:
        sametable_flag=0
        for source_table in source_table_list:
            if source_table[0] == target_table[0]:
                sametable_flag=1
        if sametable_flag==0:
            source_not_exists=source_not_exists+",'"+target_table[0]+"'"
            # print(target_table[0] + " 테이블 소스에 없음")
            src_str = " 테이블 소스에 없음"
            tgt_str = target_table[0] + ',' + target_table[4]
            ret.append({ 'TYP' : 'TBL', 'SRC' : src_str , 'TGT' :  tgt_str, 'ETC' : '' })
            
    #print("###### 테이블 비교 종료##########")
    return target_not_exists,source_not_exists,ret

def compare_column(source_column_list,target_column_list):
    
    #print("###### 컬럼 비교 ##########")
    #print("table_name,column_name,column_type,collation_name,column_comment,column_default")
    i=0
    ret = []
    for source_column in source_column_list:
        samecolumn_flag=0
        for target_column in target_column_list:
            if source_column[0] == target_column[0] and source_column[1] == target_column[1]:
                samecolumn_flag=1
                if source_column != target_column:
                    src_str = str(source_column[0]) + ',' + str(source_column[1]) + ',' + str(source_column[2]) + ','+ str(source_column[3]) + ',' + str(source_column[4])+ ',' + str(source_column[5])+ ',' + str(source_column[6])
                    tgt_str = str(target_column[0]) + ',' + str(target_column[1]) + ',' + str(target_column[2]) + ','+ str(target_column[3]) + ',' + str(target_column[4])+ ',' + str(target_column[5])+ ',' + str(target_column[6])
                    # print("#소스: "+ src_str)
                    # print("#타겟: "+ tgt_str)
                    if(str(source_column[6]) == "YES"):
                        null_option=" NULL"
                    else:
                        null_option="NOT NULL"
                    # print("ALTER TABLE "+ source_column[0] + " CHANGE COLUMN `"+ source_column[1] + "` "   )
                    etc_str = "ALTER TABLE "+ source_column[0] + " CHANGE COLUMN `"+ source_column[1] + "` " 
                    # print("`" + source_column[1] + "` "+ str(source_column[2]) + " " + null_option )
                    if(str(source_column[5]) !=  "None" ):
                        # print("default " + str(source_column[5]) )
                        etc_str += "default " + str(source_column[5])
                    # print(" comment '" + str(source_column[4]) + "';" )
                    etc_str += " comment '" + str(source_column[4]) + "';"
                    ret.append({ 'TYP' : 'COL', 'SRC' : src_str , 'TGT' :  tgt_str, 'ETC' : etc_str })
        if samecolumn_flag==0:
            # print("#"+source_column[0] + ":"+source_column[1] + " 컬럼 타겟에 없음")
            src_str = source_column[0] + ":"+source_column[1]
            tgt_str = " 컬럼 타겟에 없음"
            if(str(source_column[6]) == "YES"):
                null_option=" NULL"
            else:
                null_option="NOT NULL"

            # print('ALTER TABLE '+ source_column[0] + " ADD COLUMN "+ source_column[1] + " " + str(source_column[2]) + " " + null_option )
            etc_str = 'ALTER TABLE '+ source_column[0] + " ADD COLUMN "+ source_column[1] + " " + str(source_column[2]) + " " + null_option
            if(str(source_column[5]) !=  "None" ):
                # print(" default " + str(source_column[5]) )
                etc_str += " default " + str(source_column[5])
            # print(" comment '" + str(source_column[4]) + "'" )
            etc_str += " comment '" + str(source_column[4]) + "'"
            # print(" AFTER `" + source_column_list[i-1][1] + "`;")
            etc_str += " AFTER `" + source_column_list[i-1][1] + "`;"
            ret.append({ 'TYP' : 'COL', 'SRC' : src_str , 'TGT' :  tgt_str, 'ETC' : etc_str })


        i=i+1
    
    for target_column in target_column_list:
        samecolumn_flag=0
        for source_column in source_column_list:
            if source_column[0] == target_column[0] and source_column[1] == target_column[1]:
                samecolumn_flag=1
        if samecolumn_flag==0:
            # print("#"+target_column[0] + ":"+target_column[1] +" 컬럼 소스에 없음")
            src_str = " 컬럼 소스에 없음"
            tgt_str = target_column[0] + ":"+target_column[1]          
            # print("ALTER TABLE "+target_column[0] + " drop column `" + target_column[1] + "`;")
            etc_str = "ALTER TABLE "+target_column[0] + " drop column `" + target_column[1] + "`;"
            ret.append({  'TYP' : 'COL', 'SRC' : src_str , 'TGT' :  tgt_str, 'ETC' : etc_str })
    # print("###### 컬럼 비교 종료##########")
    return ret

def chk_tbl_list(source_db,source_schema,target_db,target_schema):
        table_list_query = "select upper(table_name),engine,row_format,table_collation,table_comment from information_schema.tables where table_schema='%s'"            
        #테이블리스트
        server_info = conn_info.server_infos[source_db]

        sql_string = (table_list_query%(source_schema))  
        source_table_list = aurora_qry(source_db,sql_string)
        # print("============= 소스테이블리스트 =============")
        # for tbl in source_table_list:
        #     print(tbl)
        server_info = conn_info.server_infos[target_db]
        sql_string = (table_list_query%(target_schema))  
        target_table_list = aurora_qry(target_db,sql_string)
        # print("============= 타겟테이블리스트 =============")
        # for tbl in source_table_list:
        #     print(tbl)
        target_not_exists,source_not_exists,ret = compare_table(source_table_list,target_table_list)
        return target_not_exists,source_not_exists,ret

def chk_col_list(source_db,source_schema,source_not_exists,target_db,target_schema,target_not_exists):
    # print("="*30 + " target_not_exists " + "="*30)
    # print(target_not_exists)
    column_list_query = "select upper(table_name),upper(column_name),column_type,collation_name,column_comment,column_default,is_nullable from information_schema.columns where table_schema='%s' and table_name not in (%s) order by table_schema,table_name,ordinal_position"            
    sql_string = (column_list_query%(source_schema,target_not_exists))
    # print(sql_string)  
    source_column_list= aurora_qry(source_db,sql_string)
    # print("="*30 + " source_not_exists " + "="*30)
    # print(source_not_exists)        
    sql_string =  (column_list_query%(target_schema,source_not_exists))
    target_column_list = aurora_qry(target_db,sql_string)
    ret = compare_column(source_column_list,target_column_list)
    return ret

def comp_dev_tst(subjArea):
    db_map = map_dev_tst(subjArea)
    if ( len(db_map) < 1 ) :
        return [{ 'TYP' : '주제영역변경필요', 'SRC' : '주제영역변경필요','TGT' :'주제영역변경필요', 'ETC' : '주제영역변경필요 '}]        
    # source_db = 'elltdev'
    # source_schema = 'elltgddev'        
    # target_db = 'ellttst1'
    # target_schema = 'elltgdtst'  
    source_db = db_map['source_db']
    source_schema = db_map['source_schema']
    target_db = db_map['target_db']
    target_schema = db_map['target_schema']
    #테이블비교      
    target_not_exists,source_not_exists,ret0 = chk_tbl_list(source_db,source_schema,target_db,target_schema)
    #print(ret0)
    #컬럼비교
    ret1 = chk_col_list(source_db,source_schema,source_not_exists,target_db,target_schema,target_not_exists)
    #print(ret1)
    return (ret0+ret1)

def map_dev_tst(subjArea):
    db_map = {  
            'elltcc' : { 'source_db' : 'elltdev' ,'source_schema' : 'elltccdev' ,'target_db' : 'ellttst4', 'target_schema' : 'elltcctst'   },
            'elltch' : { 'source_db' : 'elltdev' ,'source_schema' : 'elltchdev' ,'target_db' : 'ellttst2', 'target_schema' : 'elltchtst'   },
            'elltdp' : { 'source_db' : 'elltdev' ,'source_schema' : 'elltdpdev' ,'target_db' : 'ellttst1', 'target_schema' : 'elltdptst'   },
            'elltet' : { 'source_db' : 'elltdev' ,'source_schema' : 'elltetdev' ,'target_db' : 'ellttst3', 'target_schema' : 'elltettst'   },
            'elltgd' : { 'source_db' : 'elltdev' ,'source_schema' : 'elltgddev' ,'target_db' : 'ellttst1', 'target_schema' : 'elltgdtst'   },
            'elltmb' : { 'source_db' : 'elltdev' ,'source_schema' : 'elltmbdev' ,'target_db' : 'ellttst2', 'target_schema' : 'elltmbtst'   },
            'elltom' : { 'source_db' : 'elltdev' ,'source_schema' : 'elltomdev' ,'target_db' : 'ellttst3', 'target_schema' : 'elltomtst'   },
            'elltpy' : { 'source_db' : 'elltdev' ,'source_schema' : 'elltpydev' ,'target_db' : 'ellttst3', 'target_schema' : 'elltpytst'   },
            'elltlo' : { 'source_db' : 'elltdev' ,'source_schema' : 'elltlodev' ,'target_db' : 'ellttst3', 'target_schema' : 'elltlotst'   },
            'elltpr' : { 'source_db' : 'elltdev' ,'source_schema' : 'elltprdev' ,'target_db' : 'ellttst2', 'target_schema' : 'elltprtst'   },
            'elltsc' : { 'source_db' : 'elltdev' ,'source_schema' : 'elltscdev' ,'target_db' : 'ellttst5', 'target_schema' : 'elltsctst'   },
            'ltcmst' : { 'source_db' : 'ltcmdev' ,'source_schema' : 'ltcmstdev' ,'target_db' : 'ltcmtst1', 'target_schema' : 'ltcmsttst'   },
            'ltcmpr' : { 'source_db' : 'ltcmdev' ,'source_schema' : 'ltcmprdev' ,'target_db' : 'ltcmtst1', 'target_schema' : 'ltcmprtst'   },
            'ltcmat' : { 'source_db' : 'ltcmdev' ,'source_schema' : 'ltcmatdev' ,'target_db' : 'ltcmtst1', 'target_schema' : 'ltcmattst'   }    }  
    if ( subjArea in db_map.keys()) :
        return db_map[subjArea]
    else: 
        return {} 

def compare_index(source_index_list,target_index_list):
    ret = []
    #print("###### 인덱스 비교 ##########")
    #print("table_name,index_name,max(NON_UNIQUE) unique_flag,GROUP_CONCAT(index_name order by seq_in_index,',') index_list")
    for source_index in source_index_list:
        sameindex_flag=0
        for target_index in target_index_list:
            if source_index[0] == target_index[0] and source_index[1] == target_index[1]:
                sameindex_flag=1
                if source_index != target_index:
                    src_str = source_index[0] + ',' + source_index[1] + ',' + str(source_index[2]) + ','+ source_index[3]
                    tgt_str = target_index[0] + ',' + target_index[1] + ',' + str(target_index[2]) + ','+ target_index[3]
                    # print("#소스: "+ src_str )
                    # print("#타겟: "+ tgt_str )
                    # print("ALTER TABLE "+ source_index[0] + " drop index " + source_index[1] + ";")
                    etc_str = "ALTER TABLE "+ source_index[0] + " drop index " + source_index[1] + ";"
                    # print("ALTER TABLE "+ source_index[0] + " add index " + source_index[1] + "(" + source_index[3] + ");")
                    etc_str += "ALTER TABLE "+ source_index[0] + " add index " + source_index[1] + "(" + source_index[3] + ");"
                    ret.append({  'TYP' : 'IDX', 'SRC' : src_str , 'TGT' :  tgt_str, 'ETC' : etc_str })
        if sameindex_flag==0:
            src_str = source_index[0] + ":"+source_index[1] 
            tgt_str = " 인덱스 타겟에 없음"
            # print("#"+source_index[0] + ":"+source_index[1] + " 인덱스 타겟에 없음")
            etc_str = "ALTER TABLE "+ source_index[0] + " add index " + source_index[1] + "(" + source_index[3] + ");"
            # print("ALTER TABLE "+ source_index[0] + " add index " + source_index[1] + "(" + source_index[3] + ");")
            ret.append({  'TYP' : 'IDX', 'SRC' : src_str , 'TGT' :  tgt_str, 'ETC' : etc_str })

    for target_index in target_index_list:
        sameindex_flag=0
        for source_index in source_index_list:
            if source_index[0] == target_index[0] and source_index[1] == target_index[1]:
                sameindex_flag=1
        if sameindex_flag==0:
            src_str = " 인덱스 소스에 없음"
            tgt_str = target_index[0] + ":"+target_index[1]
            # print("#"+target_index[0] + ":"+target_index[1] +" 인덱스 소스에 없음")
            etc_str = "ALTER TABLE "+ target_index[0] + " drop index " + target_index[1] + ";"
            # print("ALTER TABLE "+ target_index[0] + " drop index " + target_index[1] + ";")
            ret.append({  'TYP' : 'IDX', 'SRC' : src_str , 'TGT' :  tgt_str, 'ETC' : etc_str })
    # print("###### 인덱스비교 종료##########")
    return ret
    
def chk_idx_list(source_db,source_schema,source_not_exists,target_db,target_schema,target_not_exists):
    index_list_query="""select upper(table_name),upper(index_name),max(NON_UNIQUE) unique_flag,GROUP_CONCAT(column_name order by seq_in_index,',') column_list
 from information_schema.STATISTICS
 where table_schema='%s' and table_name not in (%s)
 group by table_name,index_name"""
    #인덱스비교
    sql_string = (index_list_query%(source_schema,target_not_exists))  
    source_index_list= aurora_qry(source_db,sql_string)
    sql_string = (index_list_query%(target_schema,source_not_exists))  
    target_index_list = aurora_qry(target_db,sql_string)
    ret = compare_index(source_index_list,target_index_list)
    return(ret)

def comp_idx_dev_tst(subjArea):
    db_map = map_dev_tst(subjArea)
    if ( len(db_map) < 1 ) :
        return [{ 'TYP' : '데이터없음', 'SRC' : '데이터없음','TGT' :'테이터없음', 'ETC' : '데이터없음 '}]        
    source_db = db_map['source_db']
    source_schema = db_map['source_schema']
    target_db = db_map['target_db']
    target_schema = db_map['target_schema']
    #테이블비교      
    target_not_exists,source_not_exists,ret0 = chk_tbl_list(source_db,source_schema,target_db,target_schema)
    # print("=============== 테이블비교 ===============")
    # print(ret0)
    #인덱스비교
    ret2 = chk_idx_list(source_db,source_schema,source_not_exists,target_db,target_schema,target_not_exists)
    # print("=============== index비교 ===============")
    # print(ret2)
    return (ret0+ret2)

if __name__=='__main__':
    # try:
    print(sys.argv[1])
    print(comp_dev_tst(sys.argv[1]))
    # except Exception as ex:
    #     print("error!!!")
    #     print(ex)
    #     sys.exit()


