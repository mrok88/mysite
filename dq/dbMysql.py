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
    TUNNEL_FLAG = 0
    tunnel = None
    server_info = None

    def __init__(self,db):
        self.db = db
        self.server_info = conn_info.server_infos[db]        

    def MakeTunnel(self,bastion_ip,bastion_user,bastion_pwd,endpoint):
        '''ssh터널을 생성함'''
        tunnel=SSHTunnelForwarder(
            (bastion_ip, 22),
            ssh_username=bastion_user,
            ssh_password=bastion_pwd,
            remote_bind_address=(endpoint, 3306)
        )
        return tunnel

    def ssh_start(self):
        try:
            server_info = self.server_info
            self.tunnel = self.MakeTunnel(server_info["source_bastion_ip"],server_info["source_bastion_user"],server_info["source_bastion_pwd"],server_info["source_endpoint"])
            self.tunnel.start()
            self.TUNNEL_FLAG = 1
        except Exception as e:
            print(e)
            return False
        return True
    
    def ssh_stop(self):
        if (self.TUNNEL_FLAG == 1):
            self.tunnel.stop()
        return True

class Conn(Ssh):
    conn = None
    def __init__(self,db):
        super().__init__(db)

    def dbConn(self):
        server_info = self.server_info
        self.conn = pymysql.connect(host='127.0.0.1', port=self.tunnel.local_bind_port, user=server_info["source_db_user"], password=server_info['source_db_pwd'], charset='UTF8')  
        return True 

    def execute(self,sql,sql_params ={}):
        try:
            curs = self.conn.cursor(pymysql.cursors.DictCursor)          
            #curs = self.conn.cursor()          
            curs.execute(sql,sql_params)
            rows = curs.fetchall()
            return rows
        finally:
            curs.close()
        return None

    def select_db(self,schema):
        return self.conn.select_db(schema)

    def close(self):
        if self.conn is not None:
            self.conn.close()
        if (self.TUNNEL_FLAG == 1):
            self.tunnel.stop()
            self.TUNNEL_FLAG = 0