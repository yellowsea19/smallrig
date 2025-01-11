import logging

from logs.log import *

import unittest
import pymysql
import copy
import pandas as pd



class take_delivery(unittest.TestCase):

    def setUp(self, env='test'):
        self.env = env
        if self.env == 'test':
            self.urls = 'http://192.168.133.223:5555'
            self.xxl_url = 'http://192.168.133.223:19010'
            self.connection = pymysql.connect(host='192.168.133.213',  # 数据库地址
                                              user='root',  # 数据库用户名
                                              password='root',  # 数据库密码
                                              db='smallrig-platform',
                                              cursorclass = pymysql.cursors.DictCursor
                                              )  # 数据库名称

            self.cursor = self.connection.cursor()
        elif self.env == 'uat':
            self.urls = 'https://bereal.smallrig.net'
            self.xxl_url = 'http://192.168.133.232:19010'
            self.connection = pymysql.connect(host='192.168.133.233',  # 数据库地址
                                              user='root',  # 数据库用户名
                                              password='Leqi!2022',  # 数据库密码
                                              db='smallrig-platform',
                                              cursorclass=pymysql.cursors.DictCursor
                                              )  # 数据库名称
            self.cursor = self.connection.cursor()

    def tearDown(self):
        self.cursor.close()
        self.connection.close()

    def query(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def query_return_dict(self, sql):
        self.cursor.execute(sql)
        columns = [col[0] for col in self.cursor.description]
        results = []
        for row in self.cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

    def insert(self, sql):
        try:
            res = self.cursor.execute(sql)
            print(res)
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            return False

    def delete(self, sql):
        return self.insert(sql)

    def update(self, sql):
        return self.insert(sql)



    def read_excel_data(self, file_path):
        # 读取 Excel 文件
        df = pd.read_excel(file_path)
        # 将数据转换为字典列表
        data_list = []
        for index, row in df.iterrows():
            data_dict = row.to_dict()
            data_list.append(data_dict)
        return data_list



    def test_001(self):
        # 执行查询  新品
        xinpin_sql = """
                SELECT
                    p.id,
                    p.product_code AS '新品',
                    i.start_on_sale_time,
                    DATEDIFF( NOW(), i.start_on_sale_time ),
                CASE
                
                        WHEN DATEDIFF( NOW(), i.start_on_sale_time ) >= 90 THEN
                        i.start_on_sale_time ELSE DATE(
                        DATE_SUB( CURDATE(), INTERVAL 90 DAY )) 
                    END AS result 
                FROM
                    `t_product_plan_info` i,
                    t_product p 
                WHERE
                    i.start_on_sale_time IS NOT NULL 
                    AND i.del_flag = 1 
                    AND p.del_flag = 1 
                    AND p.id = i.product_id 
                    AND DATEDIFF( NOW(), i.start_on_sale_time ) > 0 
                    AND DATEDIFF( NOW(), i.start_on_sale_time ) < 60;"""
        res = self.query(xinpin_sql)
        for i in res:
            print(i)
        ## 执行查询  成长期
        cheng_chang_sql = """SELECT
                            p.id,
                            p.product_code AS '成长期',
                            i.start_on_sale_time,
                            DATEDIFF( NOW(), i.start_on_sale_time ),
                        CASE
                        
                                WHEN DATEDIFF( NOW(), i.start_on_sale_time ) >= 90 THEN
                                i.start_on_sale_time ELSE DATE(
                                DATE_SUB( CURDATE(), INTERVAL 90 DAY )) 
                            END AS result 
                        FROM
                            `t_product_plan_info` i,
                            t_product p 
                        WHERE
                            i.start_on_sale_time IS NOT NULL 
                            AND i.del_flag = 1 
                            AND p.del_flag = 1 
                            AND p.id = i.product_id 
                            AND DATEDIFF( NOW(), i.start_on_sale_time ) >= 60 
                            AND DATEDIFF( NOW(), i.start_on_sale_time ) < 120;"""
        res1 =  self.query(cheng_chang_sql)
        for i in res1:
            print(i)
        # 注意 新品与成长期，也要计入到 销量与销售额中
        res_a_sql = """SELECT
                    p.id,
                    p.product_code,
                    i.start_on_sale_time,
                    DATEDIFF( NOW(), i.start_on_sale_time )as start_on_sale_time ,
                CASE
                
                        WHEN DATEDIFF( NOW(), i.start_on_sale_time ) >= 90 THEN
                        i.start_on_sale_time ELSE DATE(
                        DATE_SUB( CURDATE(), INTERVAL 90 DAY )) 
                    END AS result 
                FROM
                    `t_product_plan_info` i,
                    t_product p 
                WHERE
                    i.start_on_sale_time IS NOT NULL 
                    AND i.del_flag = 1 
                    AND p.del_flag = 1 
                    AND p.id = i.product_id ;"""
        res_a = self.query(res_a_sql)
        data = " '在售', '升级待下架', '清仓待下架' "
        write_data = []
        for row in res_a :
            print(row)
            sqldata = """ 
                SELECT
            	sum( product_quantity ) as product_quantity,
            	sum( actual_sell_fee )  as actual_sell_fee
            FROM
            	`smallrig-report`.`t_sell_stat` 
            WHERE
            	order_time >= '%s' 
            	AND product_id = '%s' 
            	AND product_code = '%s' 
            	AND product_status_name IN (%s) 
            GROUP BY
            	product_id;""" % (row['start_on_sale_time'], row['id'], row['result'], data)
            result_sku =self.query(sqldata)
            if len(result_sku) >0:
                write_data.append({"product_id":row['id'],"product_code":row['product_code'],"pro_num":result_sku[0][0],"sell_fee":result_sku[0][1]})
            else:
                write_data.append({"product_id": row['id'], "product_code": row['product_code'], "pro_num": 0,"sell_fee": 0})
        df = pd.DataFrame(write_data)
        df.to_excel(r"E:\ERP\F1 ERP V6.0.27_20241128\aa.xlsx")


