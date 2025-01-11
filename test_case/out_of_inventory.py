
"""
F1 ERP V6.0.27_20241128 【订单列表】新增【缺货明细（含旺店通）】表单
"""
import logging
import math
from logs.log import *
from decimal import Decimal
import unittest
import pymysql
import copy
import pandas as pd



class out_of_invertory(unittest.TestCase):

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

    def query(self, sql, params=None):
        self.cursor.execute(sql, params)
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

    def compare_dictionaries(dict1, dict2):
        differences = {}
        for key in dict1.keys():
            if key in dict2:
                if dict1[key] != dict2[key]:
                    differences[key] = (dict1[key], dict2[key])
            else:
                differences[key] = (dict1[key], None)

        for key in dict2.keys():
            if key not in dict1:
                differences[key] = (None, dict2[key])

        return differences



    def test_out_of_inventory_wdt(self):
        wdt_datas = self.read_excel_data(r'E:\ERP\F1 ERP V6.0.27_20241128\2024_11_27_11_09_16.xlsx')
        wdt_out_inv = []
        product_list = []
        for wdt_data in wdt_datas:
            product_code = wdt_data['货品编号']
            if product_code is not None and not (isinstance(product_code, float) and math.isnan(product_code)):
                wdt_out_inv.append({"product_code": product_code, "quantity": wdt_data['待审核量']})
                product_list.append(product_code)
        print("product_list",product_list)
        # 查询乐其库存需发货数量
        if product_list:  # 确保 product_list 不为空
            placeholders = ', '.join(['%s'] * len(product_list))
            leqi_inv_sql = f"""
                            SELECT product_code,SUM(t2.product_quantity) as quantity
                            FROM t_order_base t1
                            LEFT JOIN t_order_sys_item t2 ON t1.id = t2.base_id AND t1.del_flag=1 AND t2.del_flag = 1
                            WHERE t1.warehouse_id = 57 AND (t1.order_status=2 OR t1.order_status = 7) AND t2.product_code IN ({placeholders})
                            GROUP BY t2.product_code
                            """
            # print(leqi_inv_sql)
            leqi_inv_results = self.query(leqi_inv_sql, tuple(product_list))
            # print(leqi_inv_results)
            for i in leqi_inv_results:
                for j in wdt_out_inv:
                    # print(j)
                    if i['product_code'] == j['product_code'] :

                        need_send_inv_total = i['quantity'] + Decimal(j['quantity'])
                        sql = "select sum(stock_out_num) as total from t_out_of_stock_detail where warehouse_id = 57 and product_code = '%s' group by product_code"%i['product_code']
                        result = self.query(sql)[0]
                        product_inv_sql = "select sum(product_num) as total from t_product_inventory where warehouse_id = 57 and  product_id = (select id from t_product where del_flag = 1 and  product_code = '%s')group by product_id"%i['product_code']

                        product_inv_result = self.query(product_inv_sql)
                        if len(product_inv_result) == 0:
                            product_inv_result = 0
                        else:
                            product_inv_result = product_inv_result[0]['total']


                        if Decimal(need_send_inv_total)  - Decimal(product_inv_result)  == Decimal(result['total'])  :
                            pass
                        else:
                            if Decimal(j['quantity']) +Decimal(need_send_inv_total) - Decimal(product_inv_result)>0:
                                print(i['product_code'],":数据对不上")
                                print("旺店通待审核量：",j['quantity'])
                                print("乐其库存需发总量 ： ",need_send_inv_total)
                                print("乐其库存在库数量： ",product_inv_result)
                                print("数据库差额：",result['total'])
                                print("旺店通待审核量 +乐其库存需发总量 - 乐其库存在库数量 = : ",Decimal(j['quantity']) +Decimal(need_send_inv_total) - Decimal(product_inv_result) )

                        # print("result: ",result)
                        print("--------------------------------------------------------------- ",)

        else:
            print("No valid product codes found.")







