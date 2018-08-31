"""
====================================
 :mod: Mysql 관련  모듈 
====================================
.. moduleauthor:: 유원석 <wsyou@wizbase.co.kr>

설명
=====

Mysql을 터널링을 통하여 접속하고 수행할 수 있도록함.

참고
====

관련 링크:
 * http://10.131.81.103:8001/dq/vrfys

관련 작업자
===========

 * 유원석 (Wonseok You)

작업일지
--------

 * 2018.08.01 wsyou : 초기함수 정의
 """
import os
import sys
import pymysql
from functools import reduce
from sshtunnel import SSHTunnelForwarder
from mdl2tbl import conn_info
##############################
class Ssh:
    """
    SSH 터널링 관리 클래스    
    sshtunnel 모듈을 사용하여 터널링관리하는 클래스
    예제 :

        ssh = Ssh(db)
        ssh.start()
        ...
        ssh.stop()
    """
    def __init__(self,db):
        self.db = db
        self.server_info = conn_info.server_infos[db]
        self.TUNNEL_FLAG = 0
        self.tunnel = None       

    def MakeTunnel(self,bastion_ip,bastion_user,bastion_pwd,endpoint):
        """바스쳔 서버를 통해서 SSH 터널을 생성하고 그 값을 돌려줍니다.
        :param string bastion_ip: 바스천서버 IP
        :param string bastion_user: 바스천서버 사용자계정
        :param string bastion_pwd: 바스천서버 사용자 패스워드        
        :returns: 바스천서버접속을 통한 SSH 터널을 return 합니다. 
        """
        tunnel=SSHTunnelForwarder(
            (bastion_ip, 22),
            ssh_username=bastion_user,
            ssh_password=bastion_pwd,
            remote_bind_address=(endpoint, 3306)
        )
        return tunnel

    def start(self):
        """바스천 서버를 통한 SSH 터닐링를 수행합니다.
        :returns: 정상 수행시 True , 오류시 False.
        """
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
        """바스천 서버를 통한 SSH 터닐링를 종료합니다.
        :returns: 정상 수행시 True
        """
        if (self.TUNNEL_FLAG == 1):
            self.tunnel.stop()
        return True
##############################
class SshDummy:
    """
    SSH 터널링 관리 더미 클래스    
    sshtunnel 모듈을 사용하여 터널링관리하는 클래스
    예제 :

        ssh = SshDummy(db)
        ssh.start()
        ...
        ssh.stop()
    """
    def __init__(self,db):
        pass    

    def MakeTunnel(self,bastion_ip,bastion_user,bastion_pwd,endpoint):
        """바스쳔 서버를 통해서 SSH 터널을 생성하고 그 값을 돌려줍니다.
        :param string bastion_ip: 바스천서버 IP
        :param string bastion_user: 바스천서버 사용자계정
        :param string bastion_pwd: 바스천서버 사용자 패스워드        
        :returns: 바스천서버접속을 통한 SSH 터널을 return 합니다. 
        """
        pass
    
    def start(self):
        """바스천 서버를 통한 SSH 터닐링를 수행합니다.
        :returns: 정상 수행시 True , 오류시 False.
        """
        pass

    def stop(self):
        """바스천 서버를 통한 SSH 터닐링를 종료합니다.
        :returns: 정상 수행시 True
        """
        pass
##############################
class Conn():
    """
    Mysql Connection관리 
    pymysql 모듈을 사용하여 mysql 커넥션을 관리함.
    예제 :

        conn = Conn(p_db_nm)
        conn.ssh.start()
        conn.sshDbConn()
        conn.param_replace = False  # SQL STRING % 관련해서 무시함. 
        conn.curType = 'list'       # 'list', 'dict' 중에 sql resultset을 list형태로 return함 
        ...   
        sql2 = "SELECT ..." 
        rows2 = conn.execute(sql2,{'tbl_nm' : tbl_nm , 'cpy_nm' : cpy_nm })
        ...
        conn.close()
    """    
    def __init__(self,db):
        self.db = db
        self.server_info = conn_info.server_infos[db]
        self.ssh = SshDummy(db)
        self.conn = None
        self.curType = 'dict'
        self.param_replace = True
        self.cols = None

    def sshDbConn(self):
        """ssh 터널링을 이용하여 db접속을 수행함.
        :returns: 정상 수행시 True
        """
        server_info = self.server_info
        self.conn = pymysql.connect(host='127.0.0.1', port=self.ssh.tunnel.local_bind_port, user=server_info["source_db_user"], password=server_info['source_db_pwd'], charset='UTF8')  
        return True 

    def dbConn(self):
        """ssh 터널링 없이 일반적인 db접속을 수행함.
        :returns: 정상 수행시 True
        """
        server_info = self.server_info
        self.conn = pymysql.connect(host=server_info["source_endpoint"], port=server_info["source_db_port"], user=server_info["source_db_user"], password=server_info['source_db_pwd'], charset='UTF8')  
        return True 


    def execute(self,sql,sql_params ={}):
        """sql을 수행하고 resultset을 list or dict형태로 return함 
        :returns: 정상수행시 resultset, 오류시 None
        """
        try:
            self.cols = None
            if (self.curType == 'dict'):
                curs = self.conn.cursor(pymysql.cursors.DictCursor)
            else :
                curs = self.conn.cursor()
            #curs = self.conn.cursor() 
            # % string 오류 해결 
            if self.param_replace :
                sqlStr = str.replace(sql,'%','%%')        
            else:
                sqlStr = sql
            curs.execute(sqlStr,sql_params)
            rows = curs.fetchall()
            try: 
                self.cols = [i[0] for i in curs.description]
            except Exception as e :
                pass
            return rows
        finally:
            curs.close()
        return None

    def select_db(self,schema):
        """Mysql에서 database를 선택함.
        """
        return self.conn.select_db(schema)

    def commit(self):
        """commit명령을 수행함.
        """
        self.conn.commit()

    def close(self):
        """DB Connection을 끊고 ssh터널링이 있을경우 해당 자원을 해제함.
        """
        if self.conn is not None:
            self.conn.close()
        if (self.ssh is not None):
            self.ssh.stop()
##############################
def get_db_sch_nm(p_db_nm,p_sch_nm,env='dev'):
    """스키마명으로 통해서 해당 db접속 서버명을 가져옴.
    :Todo: 향후 별도 파일이나 메터 관리로 분리 고려
    :returns: 정상수행시 (db명,스카마명)
    """
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