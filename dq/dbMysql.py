# -*- coding: utf-8 -*-
import os
import sys
import pymysql
from functools import reduce
from sshtunnel import SSHTunnelForwarder
from mdl2tbl import conn_info
##############################

##############################
class Ssh:
    def __init__(self,db):
        self.db = db
        self.server_info = conn_info.server_infos[db]
        self.TUNNEL_FLAG = 0
        self.tunnel = None       

    def MakeTunnel(self,bastion_ip,bastion_user,bastion_pwd,endpoint):
        '''ssh터널을 생성함'''
        tunnel=SSHTunnelForwarder(
            (bastion_ip, 22),
            ssh_username=bastion_user,
            ssh_password=bastion_pwd,
            remote_bind_address=(endpoint, 3306)
        )
        return tunnel

    def start(self):
        try:
            server_info = self.server_info
            self.tunnel = self.MakeTunnel(server_info["source_bastion_ip"],server_info["source_bastion_user"],server_info["source_bastion_pwd"],server_info["source_endpoint"])
            self.tunnel.start()
            self.TUNNEL_FLAG = 1
        except Exception as e:
            print(e)
            return False
        return True
    
    def stop(self):
        if (self.TUNNEL_FLAG == 1):
            self.tunnel.stop()
        return True

class Conn():
    def __init__(self,db):
        self.db = db
        self.server_info = conn_info.server_infos[db]
        self.ssh = Ssh(db)
        self.conn = None

    def sshDbConn(self):
        server_info = self.server_info
        self.conn = pymysql.connect(host='127.0.0.1', port=self.ssh.tunnel.local_bind_port, user=server_info["source_db_user"], password=server_info['source_db_pwd'], charset='UTF8')  
        return True 

    def dbConn(self):
        server_info = self.server_info
        self.conn = pymysql.connect(host=server_info["source_endpoint"], port=server_info["source_db_port"], user=server_info["source_db_user"], password=server_info['source_db_pwd'], charset='UTF8')  
        return True 


    def execute(self,sql,sql_params ={}):
        try:
            curs = self.conn.cursor(pymysql.cursors.DictCursor)          
            #curs = self.conn.cursor()  
            # % string 오류 해결 
            sqlStr = str.replace(sql,'%','%%')        
            curs.execute(sqlStr,sql_params)
            rows = curs.fetchall()
            return rows
        finally:
            curs.close()
        return None

    def select_db(self,schema):
        return self.conn.select_db(schema)

    def commit(self):
        self.conn.commit()

    def close(self):
        if self.conn is not None:
            self.conn.close()
        if (self.ssh is not None):
            self.ssh.stop()

def get_db_sch_nm(p_db_nm,p_sch_nm,env='dev'):
    db_map = {
    # env =tst
     'elltgdtst' : 'ellttst1'
    ,'elltdptst' : 'ellttst1'
    ,'elltprtst' : 'ellttst2'
    ,'elltchtst' : 'ellttst2'
    ,'elltmbtst' : 'ellttst2'
    ,'elltettst' : 'ellttst3'
    ,'elltomtst' : 'ellttst3'
    ,'elltpytst' : 'ellttst3'
    ,'elltlotst' : 'ellttst3'
    ,'elltcctst' : 'ellttst4'
    ,'elltsetst' : 'ellttst4'
    # env_tst           
    ,'elltgdprd' : 'elltprd1'
    ,'elltdpprd' : 'elltprd1'
    ,'elltprprd' : 'elltprd2'
    ,'elltchprd' : 'elltprd2'
    ,'elltmbprd' : 'elltprd2'
    ,'elltetprd' : 'elltprd3'
    ,'elltomprd' : 'elltprd3'
    ,'elltpyprd' : 'elltprd3'
    ,'elltloprd' : 'elltprd3'
    ,'elltccprd' : 'elltprd4'
    ,'elltseprd' : 'elltprd4'
    }
    sch_nm = p_sch_nm if env == 'dev' else str.replace(p_sch_nm,'dev',env)     
    db_nm = p_db_nm if env == 'dev' else db_map[sch_nm]
    return(db_nm,sch_nm)            