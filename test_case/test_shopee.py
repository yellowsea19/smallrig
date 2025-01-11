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

    def test_pull_mongo_order_to_oms(self,platformId=45,env='uat'):
        db_list = ["aliexpress_order_struct"]
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


    def test_order_shopee(self):
        """
        F1 ERP V6.0.27_20241128 【平台账单收入项目】shopee订单其他收入字段清洗逻辑调整

        """

        db_list = ["shopee_order_struct"]
        for db in db_list:
            print(
                "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]
            total_count = collection.count_documents(
                {"insertTime": {"$gte": "2024-11-19 00:00:00", "$lte": "2024-11-19 23:59:59"}})
            # 定义每页显示的数据量和要查询的页数
            per_page = 1000
            page_number = 1
            # 计算要跳过的文档数量
            skip_count = (page_number - 1) * per_page
            pages = math.ceil(total_count / per_page)
            print(pages)
            print(total_count)
            query = {"insertTime": {"$gte": "2024-11-19 00:00:00", "$lte": "2024-11-19 23:59:59"}}
            for i in range(1, pages + 1):
                results = collection.find(query).skip(i).limit(per_page).sort('insertTime',
                                                                              pymongo.DESCENDING)  # get a single document
                for k in results:
                    k = self.handle_objectid(k)

                    shipping_rebate = k.get('orderFee').get('order_income').get('shopee_shipping_rebate')


                    other_income = k.get('orderFee').get('order_income').get('buyer_paid_shipping_fee')

                    if Decimal(other_income) > 0:
                        if shipping_rebate != 0:
                            print(k['orderId'])
                            print(shipping_rebate)
                        shipping_rebate = 0
                        print(shipping_rebate)
                    else:
                        # print(shipping_rebate)
                        pass

                    print('--------------------------- end ----------------')


    def test_order_1212(self,platformId=34,env='uat'):
        """
        F1 ERP V6.0.28_20241212 【平台账单收入项目】shopee平台取值调整
        """
        db_list = ["shopee_order_struct"]
        for db in db_list:
            print(
                "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]
            query = {"insertTime": {"$gte": "2024-08-15 00:00:00", "$lte": "2024-11-29 23:59:59"},
                     "platformId": platformId,
                     "finishFlag": True
                     }

            results = collection.find(query).sort('insertTime', pymongo.ASCENDING)
            for k in results:
                k = self.handle_objectid(k)
                # print(k)
                # buyer_paid_shipping_fee
                buyer_paid_shipping_fee = jsonpath(k,'$.orderFee.order_income.buyer_paid_shipping_fee')

                #其它收入取值
                other_income = jsonpath(k, '$.orderFee.order_income.shopee_shipping_rebate')
                # 确保 other_income 是一个列表
                if other_income and isinstance(other_income, list):
                    # 将所有元素转换为 Decimal 类型并求和
                    other_income = sum(Decimal(value) for value in other_income if value is not None)
                    if other_income != 0:
                        print(k['orderId'])
                        print("other_income : ",other_income)
                        print('buyer_paid_shipping_fee : ', buyer_paid_shipping_fee)
                        print('--------------------------- end ----------------')
                else:
                    print("No valid data found for other_income.")

    def test_rma_1212(self,platformId=34,env='uat'):
        """
        F1 ERP V6.0.28_20241212 【平台账单收入项目】shopee平台RMA实退取值调整
        """
        db_list = ["return_order_struct"]
        for db in db_list:
            print(
                "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]
            query = {"insertTime": {"$gte": "2024-08-24 00:00:00", "$lte": "2024-11-29 23:59:59"},
                     "platformId": platformId,
                     # "orderId":"2410150MGTP4V15",
                     "finishFlag": True
                     }

            results = collection.find(query).sort('insertTime', pymongo.ASCENDING)
            for k in results:
                k = self.handle_objectid(k)
                rma_status = jsonpath(k,'$.order.status')[0]
                if rma_status == 'ACCEPTED':
                    order_sn_source = jsonpath(k,'$.order.order_sn')[0]
                    order_db = 'shopee_order_struct'
                    order_collection = self.db[order_db]
                    order_query = {"finishFlag": True, "orderId": order_sn_source}
                    order_results = order_collection.find(order_query).sort('insertTime', DESCENDING).limit(1)
                    # 获取结果中的第一条数据
                    order_result = next(order_results, None)
                    order_result = self.handle_objectid(order_result)
                    if order_result != None:
                        print('退货退款单号： ', k['orderId'])
                        print(rma_status)
                        print("平台订单号 order_sn_source ：", order_sn_source)
                        # print(order_result)
                        #获取RMA单中所有的sellersku 和数量
                        rma_sellersku = jsonpath(k,'$.order.item[*].variation_sku')
                        print("RMA中的SKU",rma_sellersku)
                        rma_qty = jsonpath(k, '$.order.item[*].amount')
                        # print("RMA中的数量", rma_qty)
                        rma_sku = dict(zip(rma_sellersku,rma_qty))
                        order_sellersku = jsonpath(order_result,'$.orderDetail.item_list[*].model_sku')
                        order_qty = jsonpath(order_result,'$.orderDetail.item_list[*].model_quantity_purchased')
                        print('订单中的SKU: ',order_sellersku)
                        # print('订单中的SKU数量: ',order_qty)
                        order_sku = dict(zip(order_sellersku,order_qty))
                        res = all(key in rma_sku and rma_sku[key] == order_sku[key] for key in order_sku)
                        #订单中的平台优惠
                        discount_from_voucher_shopee = jsonpath(order_result,'$.orderFee.order_income.items[*].discount_from_voucher_shopee')
                        discount_from_coin = jsonpath(order_result,'$.orderFee.order_income.items[*].discount_from_coin')
                        sum_discount_from_voucher_shopee = sum(Decimal(x) for x in discount_from_voucher_shopee)
                        sum_discount_from_coin = sum(Decimal(x) for x in discount_from_coin)
                        print('平台优惠 discount_from_voucher_shopee ： ',discount_from_voucher_shopee)
                        print('平台优惠 discount_from_coin ： ',discount_from_coin)

                        if res:
                            print("全退")
                            #cost表数据库中取运费字段和其他收入字段
                            sql = """
                                select * from t_order_cost where base_id in  (select id from t_order_base where source_code = '%s' and order_status != 6)
                                  """ % order_sn_source
                            res = self.query(sql)
                            shipping_fee_list = []
                            other_income_list = []
                            for i in res :
                                shipping_fee = i['shipping_fee']
                                print('shipping_fee:',shipping_fee)
                                shipping_fee_list.append(shipping_fee)
                                other_income = i['other_income']
                                print('other_income',other_income)
                                other_income_list.append(other_income)
                            son_actual_refund = jsonpath(k,'$.orderDetail.item[*].refund_amount')

                            actual_refund = sum(Decimal(x) for x in son_actual_refund) + sum_discount_from_voucher_shopee+sum_discount_from_coin+sum(shipping_fee_list) + sum(other_income_list)
                            print("实退 ：",actual_refund)
                            print('------------------------------------ end ------------------------------------------')

                        else:
                            print("部分退")
                            son_actual_refund = jsonpath(k, '$.orderDetail.item[*].refund_amount')
                            print(son_actual_refund)
                            print('------------------------------------ end ------------------------------------------')


                else:
                    pass


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






