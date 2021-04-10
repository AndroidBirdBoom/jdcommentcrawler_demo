import pymysql


class Crawler:

    def __init__(self, host, user, paswd, db):
        self.host = host
        self.user = user
        self.passwd = paswd
        self.db = db
        self.conn = None
        self.cursor = None
        self.initsql(host, user, paswd, db)

    def initsql(self, host, user, passwd, db):
        self.conn = pymysql.connect(host=host, user=user, password=passwd, db=db, port=3306)
        self.cursor = self.conn.cursor()

    def insert_sql(self, sql, *args):
        try:
            if sql is not None:
                self.cursor.execute(sql, args)
                self.conn.commit()
        except:
            self.conn.rollback()

    def query_sql(self, sql):
        results = None
        try:
            if sql is not None:
                self.cursor.execute(sql)
                results = self.cursor.fetchall()

        except:
            self.conn.rollback()

        return results

    def close(self):
        self.cursor.close()
        self.conn.close()
