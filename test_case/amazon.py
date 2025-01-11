
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



    def test_amazon(self ,platformId=30 ,env='test'):
        """
        F1 ERP V6.0.28_20241212
       平台拉单增加补偿机制
        """
        db_list = ["amazon_order_struct"]
        for db in db_list:
            print(
                "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]
            query = {"insertTime": {"$gte": "2024-12-09 17:45:00", "$lte": "2024-12-29 23:59:59"},
                     "platformId": platformId,
                     "finishFlag": True
                     }

            results = collection.find(query).sort('insertTime', pymongo.DESCENDING)
            tmp_dict = {}
            for k in results:
                k = self.handle_objectid(k)

                if k['orderId'] not in tmp_dict:
                    tmp_dict[f"{k['orderId']}"] = k['updatedTime']
                elif k['updatedTime'] != tmp_dict[f"{k['orderId']}"]:
                    print("单据重复但无需处理 ： ",k['orderId'],k['updatedTime'],'-------------->', tmp_dict[f"{k['orderId']}"])

                else:
                    print("单据重复： %s"%k['orderId'])
            print(tmp_dict)
            print("总数 ：",len(tmp_dict))


    def test_20250109(self):
        """
        修复历史数据平台确认收入
        """
        url = "http://192.168.133.223:15010/api/oms/orderStatus"
        headers = {'Content-Type': 'application/json'}
        data = {
            "platformId":30,
            "manual":"true",
            "sendTimeBegin":"2024-01-01 00:00:00",
            "sendTimeEnd":"2025-02-01 00:00:00",
            "orderCodes":["SO24042905365"]
        }
        res = requests.post(url=url, headers=headers, json=data)
        print(res.text)

    def test_2025010903(self):
        """
        修复历史数据店铺优惠
        """
        url = "http://192.168.133.223:15010/init/v1/modifyAmazonCouponFee"
        headers = {'Content-Type': 'application/json'}
        data ={
                "platformIds":[30],
                "orderTimeBegin":"2024-01-01 00:00:00",
                "orderTimeEnd":"2025-02-01 00:00:00",
                # "orderStatus":[4,9],
                "source":1,
                "orderCodes": ["SO24120907985"],
                "orderAttribute":1
            }
        res = requests.post(url=url, headers=headers, json=data)
        print(res.text)


    def test_2025010902(self ,platformId=30 ,env='test'):
        db_list = ["amazon_order_struct"]
        for db in db_list:
            print(
                "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]
            query = {"insertTime": {"$gte": "2024-12-09 17:45:00", "$lte": "2024-12-29 23:59:59"},
                     "platformId": platformId,

                     "finishFlag": True
                     }

            results = collection.find(query).sort('insertTime', pymongo.DESCENDING)
            for k in results:
                k = self.handle_objectid(k)
                order_status =  jsonpath(k,"$..promotionDiscount")
                print(k['orderId'])
                # print(order_status)
                itemTax = jsonpath(k,"$..itemTax.amount")
                print("itemTax: ",itemTax)
                shippingTax = jsonpath(k, "$..shippingTax.amount")
                print("shippingTax: ", shippingTax)
                giftWrapTax = jsonpath(k, "$..giftWrapTax.amount")
                print("giftWrapTax: ", giftWrapTax)
