# coding=utf-8
import sys

import pymysql


class MySQL(object):
    # 初始化时连接数据库
    def __init__(self, host='localhost', user='root', passwd='admin123', db='test', port=3306):
        try:
            self.conn = pymysql.connect(
                host=host,
                port=port,
                user=user,
                passwd=passwd,
                db=db,
                charset='utf8'
            )
        except Exception as e:
            print("连接数据库失败：\n %s" % e)
            sys.exit()
        else:
            print('连接数据库成功')
            self.cur = self.conn.cursor()

    # 断开数据库连接
    def close(self):
        self.cur.close()
        self.conn.close()

    # 操作数据库
    def sql(self, command):
        # command参数是需要执行的数据库指令
        """
        创建表：create table + 表名
        向已存在表中插入数据：insert into……values
        删除已存在的表：drop table + 表名
        更新表中数据：update……set
        查询表中数据：select * from
        """
        try:
            res = self.cur.execute(command)
            print(res)
            if res:
                if "select" or "SELECT" in command:
                    pass
                else:
                    self.conn.commit()
                    print("改动已提交")
            else:
                if "select" or "SELECT" in command:
                    pass
                else:
                    self.conn.rollback()
                    print("改动提交失败，已回滚")
        except Exception as e:
            print("数据库指令错误")


if __name__ == "__main__":
    mysql = MySQL()
