
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
    def setUp(self,env='uat'):
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



    def test_lazada(self ,platformId=39 ,env='test'):
        """
        F1 ERP V6.0.30_20241226
       【订单列表】改造lazada订单确认收入逻辑
        """
        db_list = ["lazada_order_struct"]
        for db in db_list:
            print(
                "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]
            query = {"insertTime": {"$gte": "2024-10-26 00:00:00", "$lte": "2024-12-29 23:59:59"},
                     "platformId": platformId,
                     # "orderId":"933209613936224",
                     "finishFlag": True
                     }

            results = collection.find(query).sort('insertTime', pymongo.DESCENDING)

            for k in results:
                print(k['orderId'])
                print(k['_id'])
                k = self.handle_objectid(k)
                for i in k['orderDetail']['data']:
                    print("sellerSku : ",i['sku'])
                    print("状态       ：",i['status'])
                print("---------------------------------- end ----------------------------------------------------")
