import time
from decimal import Decimal, ROUND_HALF_UP
import pandas as pd
import pymysql,requests
import unittest
from datetime import datetime
import pymongo
from pymongo import MongoClient
import json
import math
from jsonpath import jsonpath
from bson import ObjectId

from pull_order import pull_order,pull_rma_order,pull_order_fee,pull_order_return_fee

class TestMongoDB(unittest.TestCase):
    def setUp(self,env='test'):
        self.env = env
        if self.env == 'test':
            self.client = MongoClient(
                "mongodb://smallrig:smallrig@192.168.133.223:27017/?authMechanism=SCRAM-SHA-1&authSource=smallrig&directConnection=true")
            self.db = self.client['smallrig']

            self.urls = 'http://192.168.133.223:5555'
            self.xxl_url = 'http://192.168.133.223:19010'
            self.connection = pymysql.connect(host='192.168.133.213',  # 数据库地址
                                              user='root',  # 数据库用户名
                                              password='root',  # 数据库密码
                                              db='smallrig-platform',
                                              cursorclass = pymysql.cursors.DictCursor)  # 数据库名称
            self.cursor = self.connection.cursor()
        elif self.env == 'uat':
            self.client = MongoClient(
                "mongodb://smallrig:smallrig@192.168.133.233:27017/?authMechanism=DEFAULT&authSource=admin")
            self.db = self.client['smallrig']
            self.urls = 'https://bereal.smallrig.net'
            self.xxl_url = 'http://192.168.133.232:19010'
            self.connection = pymysql.connect(host='192.168.133.233',  # 数据库地址
                                              user='root',  # 数据库用户名
                                              password='Leqi!2022',  # 数据库密码
                                              db='smallrig-platform',
                                              cursorclass = pymysql.cursors.DictCursor)  # 数据库名称
            self.cursor = self.connection.cursor()




    def query(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

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

    def test_connection(self):
        self.assertIsNotNone(self.db)



    def handle_objectid(self,data):
        """递归转换 MongoDB 数据，将所有 ObjectId 转化为字符串"""
        if isinstance(data, dict):
            for key, value in data.items():
                data[key] = self.handle_objectid(value)
        elif isinstance(data, list):
            for index, item in enumerate(data):
                data[index] = self.handle_objectid(item)
        elif isinstance(data, ObjectId):
            return str(data)
        return data

    def test_pull_mongo_order_to_oms(self,platformId=59,env='test'):
        db_list = ["tiktok_order_struct"]
        for db in db_list:
            print(
                "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]
            query = {"insertTime": {"$gte": "2024-08-15 00:00:00", "$lte": "2024-09-00 23:59:59"},
                     "platformId": platformId,
                     "finishFlag": True
                     }

            results = collection.find(query).sort('insertTime', pymongo.ASCENDING)
            for k in results:
                k = self.handle_objectid(k)
                print(k)
                pull_order(env=env, id=k['_id'], platformId=platformId)
                # pull_order_fee(env=env, id=k['_id'], platformId=platformId)
                # pull_order_return_fee(env=env, id=k['_id'], platformId=48)


    def test_actual_refund(self,platformId=59,env='test'):
        """
        F1 ERP V6.0.28_20241212
       【平台账单收入项目】TikTok实退金额逻辑更新
        """
        db_list = ["return_order_struct"]
        for db in db_list:
            print(
                "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]
            query = {"insertTime": {"$gte": "2024-12-01 00:00:00", "$lte": "2024-12-29 23:59:59"},
                     "platformId": platformId,
                     # "orderId":"4035249681856041903",
                     "finishFlag": True
                     }

            results = collection.find(query).sort('insertTime', pymongo.ASCENDING)
            for k in results:
                k = self.handle_objectid(k)
                print(k['orderId'])
                actual_refund_path = '$.order.return_line_items'
                order_status = jsonpath(k,'$..return_status')
                print("状态：",order_status)
                order_source_code = jsonpath(k, '$.order.order_id')
                print("平台订单号：", order_source_code)
                if order_status[0] == 'RETURN_OR_REFUND_REQUEST_CANCEL':
                    print("实退： 0")
                else:
                    refund_total_path = '$.order.return_line_items[*].refund_amount.refund_total'
                    refund_total = jsonpath(k, refund_total_path)
                    if refund_total:
                        refund_total = refund_total
                    print("refund_total:",refund_total)
                    product_platform_discount_path = 'order.discount_amount[*].product_platform_discount'
                    product_platform_discount = jsonpath(k, product_platform_discount_path)
                    if product_platform_discount:
                        product_platform_discount = product_platform_discount
                    print("product_platform_discount:", product_platform_discount)

                    shipping_fee_platform_discount = '$.order.discount_amount[*].shipping_fee_platform_discount'
                    shipping_fee_platform_discount = jsonpath(k, shipping_fee_platform_discount)
                    if shipping_fee_platform_discount:
                        shipping_fee_platform_discount = shipping_fee_platform_discount
                    print("shipping_fee_platform_discount:", shipping_fee_platform_discount)
                    sku_actual_list = []
                    product_discount_sum_list = []
                    shipping_discount_sum_list = []
                    num = len(refund_total)
                    num_index = 1
                    for i in refund_total:
                        if  num_index == num :
                            product_discount_sum_list = sum(Decimal(x) for x in product_discount_sum_list)
                            shipping_discount_sum_list = sum(Decimal(x) for x in shipping_discount_sum_list)
                            sku_actual_list = sum(Decimal(x) for x in sku_actual_list)

                            refund_total = sum(Decimal(x) for x in refund_total)
                            product_platform_discount = sum(Decimal(x) for x in product_platform_discount)
                            shipping_fee_platform_discount = sum(Decimal(x) for x in shipping_fee_platform_discount)
                            sku_actual =  refund_total + product_platform_discount + shipping_fee_platform_discount - sku_actual_list
                            print("第%s个实退："%num_index,sku_actual)
                            num_index = num_index + 1
                        else:
                            i = Decimal(i)
                            product_discount_sum = sum(Decimal(x) for x in product_platform_discount)
                            refund_total_sum = sum(Decimal(x) for x in refund_total)
                            shipping_discount_sum = sum(Decimal(x) for x in shipping_fee_platform_discount)
                            # 计算 sku_actual
                            if refund_total_sum != 0:
                                sku_actual = (
                                        i
                                        + product_discount_sum * (i / refund_total_sum)
                                        + shipping_discount_sum * (i / refund_total_sum)    )
                                sku_actual = round(sku_actual, 9)
                                print("第%s个实退："%num_index,sku_actual)
                                sku_actual_list.append(sku_actual)
                                product_discount_sum_list.append(product_discount_sum * (i / refund_total_sum))
                                shipping_discount_sum_list.append(shipping_discount_sum * (i / refund_total_sum))


                            else:
                                print("Error: refund_total_sum is zero.")
                            num_index = num_index + 1



                print("--------------------------- end --------------------------------")


    def test_Fix_rma(self):
        """
        修复历史数据
        """
        url = "http://192.168.133.223:15010/rmaOrder/v1/fixRmaRefundAmount"
        headers = { 'Content-Type': 'application/json'}
        data = {
                "platformId": 59,
                "createTimeBegin": "2024-07-01 10:00:00",
                "createTimeEnd": "2024-12-12 10:00:00",
                "platformRmaCodes": [
                    "4035257547448684586"
                ]
            }
        res = requests.post(url=url,headers=headers,json=data)
        print(res.text)

    def test_pull_rma_to_order(self,platformId=34,platform_rma_code='24060406651HRPA'):
        """
        清洗RMA单--
        根据退货退款单号，找到订单号，清洗订单号，然后若退货退款单号存在，则先删再清洗
        """
        db_list = ["return_order_struct"]
        for db in db_list:
            print(
                "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]
            query = {
                     "platformId": platformId,
                     "orderId":f'{platform_rma_code}',
                     "finishFlag": True
                     }

            results = collection.find(query).sort('insertTime', pymongo.DESCENDING)
            try:
                #取出最新的一条RMA数据
                k = next(results)
                print("退货退款单号： ",k['orderId'],"----",k['_id'])

                #获取订单号
                if platformId == 59:
                    order_db = "tiktok_order_struct"
                    source_code  = jsonpath (k,'$.order.order_id')[0]
                elif platformId == 34:
                    order_db = "shopee_order_struct"
                    source_code = jsonpath(k, '$.order.order_sn')[0]
                elif platformId == 39:
                    order_db = "lazada_order_struct"
                    source_code = jsonpath(k, '$.order.trade_order_id')[0]
                print("平台订单号： ",source_code)
            except KeyboardInterrupt:
                print("mongo中无该退货退款单数据 ： ",platform_rma_code)
            except StopIteration:
                print("mongo中无该退货退款单数据 ： ", platform_rma_code)

            try:
                #清洗订单数据
                order_query = {"orderId":f'{source_code}',
                                "finishFlag": True}
                collection_order = self.db[order_db]
                order_result = collection_order.find(order_query).sort('insertTime', pymongo.DESCENDING)
                order_id = next(order_result)['_id']

                print(order_id)
                pull_order(env=self.env,id=order_id,platformId=platformId)
                time.sleep(3)
                del_rma_order_sql = 'delete from t_rma_order where platform_rma_code = "%s"'%platform_rma_code
                self.delete(del_rma_order_sql)
                pull_rma_order(env=self.env,id=k['_id'],platformId=platformId)
            except UnboundLocalError:
                print("mongo 中没有订单数据的版本，订单号： ",source_code)
            except StopIteration :
                print("mongo 中没有订单数据的版本，订单号： ", source_code)


