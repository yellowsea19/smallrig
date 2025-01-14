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

    def tearDown(self):
        self.cursor.connection.close()
        self.client.close()  # 关闭 MongoDB 连接

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



    def test_pull_rma_to_order(self,platformId=45,platform_rma_code='14250703537440482'):
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
                elif platformId == 45:
                    order_db ="aliexpress_order_struct"
                    source_code = jsonpath(k,'$.order.parent_order_id')[0]
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




    def test_init_aliexpress(self,platformId = 45, platform_rma_code = '14250703537440482'):
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
                "orderId": f'{platform_rma_code}',
                "finishFlag": True
            }

            results = collection.find(query).sort('insertTime', pymongo.DESCENDING)
            try:
                # 取出最新的一条RMA数据
                k = next(results)
                print("退货退款单号： ", k['orderId'], "----", k['_id'])

                # 获取订单号

                order_db = "aliexpress_order_struct"
                source_code = jsonpath(k, '$.order.parent_order_id')[0]
                print("平台订单号： ", source_code)
            except KeyboardInterrupt:
                print("mongo中无该退货退款单数据 ： ", platform_rma_code)
            except StopIteration:
                print("mongo中无该退货退款单数据 ： ", platform_rma_code)

            try:
                # 清洗订单数据
                order_query = {"orderId": f'{source_code}',
                               "finishFlag": True}
                collection_order = self.db[order_db]
                order_result = collection_order.find(order_query).sort('insertTime', pymongo.DESCENDING)
                order_info = next(order_result)
                order_id =order_info['_id']

                print(order_id)
                receiveStatus = jsonpath(order_info,'$.orderFee.target.logisticInfoList[*].receiveStatus')
                if len(receiveStatus) != 1:
                    raise KeyError("logisticInfoList 有多个值")
                receiveStatus = receiveStatus[0]
                print(receiveStatus)
                if receiveStatus == "received":
                    buyer_return_logistics_company = jsonpath(order_info,'$.orderDetail.aliexpress_issue_detail_get_response.result_object.buyer_return_logistics_company')
                    print("buyer_return_logistics_company ： ",buyer_return_logistics_company)
                    if buyer_return_logistics_company :
                        print("RMA类型: 退货 & 退款")
                        print("退款类型：已发货退货退款")
                        print("退货类型: 客户退件")
                    else:
                        print("RMA类型: 退款")
                        print("退款类型：已发货仅退款")
                else:
                    print("RMA类型: 退货 & 退款")
                    print("退款类型：已发货退货退款")
                    print("退货类型: 物流退件")

                # pull_order(env=self.env, id=order_id, platformId=platformId)
                # time.sleep(3)
                # del_rma_order_sql = 'delete from t_rma_order where platform_rma_code = "%s"' % platform_rma_code
                # self.delete(del_rma_order_sql)
                # pull_rma_order(env=self.env, id=k['_id'], platformId=platformId)
            except UnboundLocalError:
                print("mongo 中没有订单数据的版本，订单号： ", source_code)
            except StopIteration:
                print("mongo 中没有订单数据的版本，订单号： ", source_code)

