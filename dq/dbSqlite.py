import sqlite3

class Conn():
    def __init__(self,db=":memory:"):
        self.db = db
        self.conn = None
        self.cols = None
        self.curType = 'dict'
        self.param_replace = False
        self.cols = None        

    def dbConn(self):
        self.conn = sqlite3.connect(self.db)

    def execute(self,sql,sql_params ={}):
        curs = self.conn.cursor()        
        try:
            self.cols = None
            # dictionary  형태로 출려하게함.
            if self.curType == 'dict':
                self.conn.row_factory = sqlite3.Row
            else :
                self.conn.row_factory = None
            curs.execute(sql,sql_params)
            rows = curs.fetchall()
            try:
                self.cols = [i[0] for i in curs.description]
            except Exception as e:
                self.cols = None
            return rows
        finally:
            curs.close()
        return None

    def executemany(self,sql,sql_params):
        try:
            curs = self.conn.cursor()      
            curs.executemany(sql,sql_params)
            return len(sql_params)
        finally:
            curs.close()
        return None

    def select_db(self,schema):
        return None

    def commit(self):
        self.conn.commit()

    def close(self):
        if self.conn is not None:
            self.conn.close()