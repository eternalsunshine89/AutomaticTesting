import pymysql
from config import *


class DB(object):
    def __init__(self):
        try:
            self.conn = pymysql.connect(host=db_host,
                                        port=db_port,
                                        user=db_user,
                                        passwd=db_passwd,
                                        db=db)
            print('数据库已连接')
            self.cur = self.conn.cursor()
        except Exception as e:
            logging.error(e)

    def __del__(self):  # 析构函数，实例删除时触发
        self.cur.close()
        self.conn.close()
        print('数据库已断开')

    def query(self, sql):
        self.cur.execute(sql)
        print(self.cur.fetchall())
        return self.cur.fetchall()

    def exec(self, sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e)

    def insert(self, table, params):
        pass


if __name__ == '__main__':
    d = DB()
