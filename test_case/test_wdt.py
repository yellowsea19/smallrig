import requests
from pymongo import DESCENDING
import time
from decimal import Decimal, ROUND_HALF_UP
import pandas as pd
import pymysql
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


    def test_rma_order_ty_1212(self,platformId=53,env='uat'):
        """
        F1 ERP V6.0.28_20241212 【平台账单收入项目】 -- 抖音，需求有变更，优惠放在整单维度
        """
        db_list = ["return_order_struct"]
        for db in db_list:
            print(
                "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]
            query = {"insertTime": {"$gte": "2024-09-27 17:42:00", "$lte": "2024-12-29 23:59:59"},
                     "platformId": platformId,
                     "orderId":"TK2412080042",
                     "finishFlag": True
                     }

            results = collection.find(query).sort('insertTime', pymongo.ASCENDING)
            for k in results:
                k = self.handle_objectid(k)
                # print(k['orderId'])
                if k['order']['status'] == 90:
                    refundtype = jsonpath(k,'$.order.type')[0]
                    if refundtype != 1:
                        print(k['orderId'])
                        #从退货退款单中查出平台订单号
                        source_code = jsonpath(k, '$.order.srcTids')[0]
                        print("平台订单号：", source_code)
                        #从原始订单中查询最新的一条报文
                        order_db = 'wdt_origin_order_struct'
                        order_collection = self.db[order_db]
                        order_query = {"finishFlag": True, "orderId": source_code}
                        order_results = order_collection.find(order_query).sort('insertTime', DESCENDING).limit(1)
                        # 获取结果中的第一条数据
                        order_result = next(order_results, None)
                        order_result = self.handle_objectid(order_result)
                        print("退货退款单ID：",k['_id'])
                        # print("平台订单ID：",order_result['_id'])
                        # 退换单实际退款金额
                        actualRefundAmount = jsonpath(k, "$.order.actualRefundAmount")[0]
                        print("actualRefundAmount :", actualRefundAmount)
                        #sellersku维度实退金额计算
                        for i in k['order']['detailList']:
                            print("SKU : ",i['specNo'])
                            #订单oid
                            oid = i['oid']
                            # sellersku申请金额
                            sellersku_refundAmount = i['refundAmount']
                            if k['order']['fromType'] == 0:
                                # 订单维度退款金额
                                return_amount = k['order']['guaranteeRefundAmount']
                            elif k['order']['fromType'] == 1 or k['order']['fromType'] == 2:
                                return_amount = k['order']['directRefundAmount']
                            else:
                                raise ValueError
                            try:
                                for j in order_result['order']['tradeOrders']:
                                    if j['oid'] == i['oid']:
                                        sellersku_platform_discount = 0
                                        for jj in order_result['order']['discountList']:
                                            if jj['type'] == 'promotion_platform_amount':
                                                if jj['oid'] != "":
                                                    sellersku_platform_discount = jj['amount']
                                                    print("sellersku_platform_discount : ",sellersku_platform_discount)


                                        sellerSku_refund = Decimal(actualRefundAmount) * Decimal(sellersku_refundAmount) / Decimal(return_amount) + Decimal(sellersku_platform_discount)
                                        print("实退：", sellerSku_refund)
                            except TypeError:pass

                        print('---------------------- end ---------------------')



    def test_rma_order_pdd_1212(self,platformId=52,env='uat'):
        """
        F1 ERP V6.0.28_20241212  --
        """
        db_list = ["return_order_struct"]
        for db in db_list:
            print(
                "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]
            query = {"insertTime": {"$gte": "2024-09-27 17:42:00", "$lte": "2024-11-29 23:59:59"},
                     "platformId": platformId,
                     "orderId":"TK2411030145",
                     "finishFlag": True
                     }

            results = collection.find(query).sort('insertTime', pymongo.ASCENDING)
            for k in results:
                k = self.handle_objectid(k)
                # print(k['orderId'])
                if k['order']['status'] == 90:
                    refundtype = jsonpath(k,'$.order.type')[0]
                    if refundtype != 1:
                        print(k['orderId'])
                        #从退货退款单中查出平台订单号
                        source_code = jsonpath(k, '$.order.srcTids')[0]
                        print("平台订单号：", source_code)
                        #从原始订单中查询最新的一条报文
                        order_db = 'wdt_origin_order_struct'
                        order_collection = self.db[order_db]
                        order_query = {"finishFlag": True, "orderId": source_code}
                        order_results = order_collection.find(order_query).sort('insertTime', DESCENDING).limit(1)
                        # 获取结果中的第一条数据
                        order_result = next(order_results, None)
                        order_result = self.handle_objectid(order_result)
                        print("退货退款单ID：",k['_id'])
                        # print("平台订单ID：",order_result['_id'])
                        # 退换单实际退款金额
                        actualRefundAmount = jsonpath(k, "$.order.actualRefundAmount")[0]
                        print("actualRefundAmount :", actualRefundAmount)
                        #订单维度实退金额计算
                        platform_discount = 0
                        try :
                            for i in order_result['order']['discountList']:
                                if i['type'] == 'platform_discount':
                                    platform_discount = i['amount']

                            refund = Decimal(actualRefundAmount) + Decimal(platform_discount)
                            print("实退金额： ",refund)
                        except TypeError:
                            pass
                    print('---------------------- end ---------------------')


    def test_Fix_rma(self):
        """
        修复历史数据
        """
        url = "http://192.168.133.223:15010/rmaOrder/v1/fixRmaRefundAmount"
        headers = { 'Content-Type': 'application/json'}
        data = {
                "platformId": 53,
                "createTimeBegin": "2024-07-01 10:00:00",
                "createTimeEnd": "2024-12-12 10:00:00",
                "platformRmaCodes": [
                    "146523114750100635"
                ]
            }
        res = requests.post(url=url,headers=headers,json=data)
        print(res.text)

    def test_pull_rma(self,platform_rma_code='TK2501070171'):
        """
        清洗RMA单，如果RMA单对应的订单不存在，则会先清洗订单，然后清洗RMA单
        如果RMA单已经存在，则会先删除，再重新清洗
        """
        db_list = ["return_order_struct"]
        for db in db_list:
            print(
                "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]
            query = {
                "orderId": f'{platform_rma_code}',
                "finishFlag": True
            }

            results = collection.find(query).sort('insertTime', pymongo.DESCENDING)
            try:
                # 取出最新的一条RMA数据
                k = next(results)
                print("退货退款单号： ", k['orderId'], "----", k['_id'])

                # 获取订单号
                source_code = jsonpath(k, '$.order.srcTids')[0]
            except KeyboardInterrupt:
                print("mongo中无该退货退款单数据 ： ", platform_rma_code)
            except StopIteration:
                print("mongo中无该退货退款单数据 ： ", platform_rma_code)

            try:
                order_db = "wdt_order_struct"
                # 清洗订单数据
                order_query = {"orderDetail.srcTradeNo": f'{source_code}',
                               "finishFlag": True}
                collection_order = self.db[order_db]
                order_result = collection_order.find(order_query).sort('insertTime', pymongo.DESCENDING)
                order_id = next(order_result)['_id']

                print(order_id)
                pull_order(env=self.env, id=order_id, platformId=200)
                time.sleep(3)
                del_rma_order_sql = 'delete from t_rma_order where wdt_rma_code = "%s"' % platform_rma_code
                self.delete(del_rma_order_sql)
                pull_rma_order(env=self.env, id=k['_id'], platformId=200)
            except UnboundLocalError:
                print("mongo 中没有订单数据的版本，订单号： ", source_code)
            except StopIteration:
                print("mongo 中没有订单数据的版本，订单号： ", source_code)