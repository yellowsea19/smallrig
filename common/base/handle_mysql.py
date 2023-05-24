#!/usr/bin/python3
# -*- coding:utf-8 -*-

import pymysql
from common.base.handle_yaml import HandleYaml
import json

do_yaml = HandleYaml(r"conf/base.yaml")
class HandleMysql:
    """执行sql语句
    """

    def __init__(self):
        self.conn = pymysql.connect(host=do_yaml.get_data("mysql", "host"),
                                    user=do_yaml.get_data("mysql", "user"),
                                    password=do_yaml.get_data("mysql", "password"),
                                    database=do_yaml.get_data("mysql", "db"),
                                    port=do_yaml.get_data("mysql", "port"),
                                    charset="utf8")
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)


    def get_data(self, sql, args=None):
        """查询数据库数据返回数据
        """
        self.cursor.execute(sql, args=args)
        self.conn.commit()
        return self.cursor.fetchone()
        # return self.cursor.fetchall()



    def delete_data(self, sql, args=None):
        """删除数据库数据返回数据
        """
        delete_company = ""
        for (i, j) in zip(do_yaml.get_all_data("company"), range(len(do_yaml.get_all_data("company")))):
            delete_company += (do_yaml.get_all_data("company")[i])+"','"
        sql = sql % delete_company
        self.cursor.execute(sql, args=args)
        self.conn.commit()
        return self.cursor.fetchone()


    def delete_data1(self, sql, args=None):
        """根据SQL删除数据
        """
        self.conn.ping(reconnect=True)
        self.cursor.execute(sql, args=args)
        self.conn.commit()
        return self.cursor.fetchone()

    def update_data(self, sql, args=None):
        """根据SQL更新数据
        """
        # print(args)
        self.conn.ping(reconnect=True)
        self.cursor.execute(sql, args=args)
        self.conn.commit()
        return self.cursor.fetchone()

do_mysql = HandleMysql()

if __name__ == '__main__':
    do_mysql = HandleMysql()
    sql="select id from `smallrig-mall-product`.web_class where class_name = %s and site_code = %s order by create_time desc"
    result = do_mysql.get_data(sql,args=("aa","bb"))
    print(result)
