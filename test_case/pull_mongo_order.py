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
from jsonpath_ng import jsonpath, parse
from bson import ObjectId

from pull_order import pull_order,pull_rma_order,pull_order_fee,pull_order_return_fee

class TestMongoDB(unittest.TestCase):
    def setUp(self,env='test'):
        # self.client = MongoClient("mongodb://192.168.133.235:27017/?directConnection=true")
        # self.client = MongoClient("mongodb://smallrig:smallrig@192.168.133.233:27017/?authMechanism=DEFAULT&authSource=admin")

        # self.client = MongoClient("mongodb://smallrig:smallrig@192.168.133.210:27017/?authMechanism=DEFAULT")
        # self.db = self.client['smallrig']  # use your database name here
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


    def test_pull_mongo_order_to_oms_1(self,platformId=59,env='test'):
        """根据订单号批量清洗
        """
        db_list = ["return_order_struct"]
        for db in db_list:
            print(
                "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]
            # order_id_list  = [4035246940209648254,4035246985912160894,4035246029464310398,4035246029464179326]
            output_data = []
            order_type = []
            # for order_id in order_id_list:
            query = {
                    # "orderId": f"{order_id}",
                    "insertTime": {"$gte": "2024-09-01 00:00:00", "$lte": "2024-09-09 23:59:59"},
                     "platformId": platformId,
                     "finishFlag": True,
                     # "order.return_status":"RETURN_OR_REFUND_REQUEST_CANCEL"
                    # "order.order_id":"576685435687506558"
                     }

            results = collection.find(query).sort('insertTime', pymongo.DESCENDING)
            status_dict =  {
                            "RETURN_OR_REFUND_REQUEST_PENDING": "买家已发起退货或退款请求。该请求正在等待卖家或平台的审核",
                            "REFUND_OR_RETURN_REQUEST_REJECT": "卖方拒绝买方的退货或退款请求",
                            "AWAITING_BUYER_SHIP": "退货请求已获批准。卖家正在等待买家将批准的商品运送给卖家",
                            "BUYER_SHIPPED_ITEM": "买家已将批准的物品运送给卖家",
                            "REJECT_RECEIVE_PACKAGE": "卖家检查了退回的物品并拒绝了退货包裹",
                            "RETURN_OR_REFUND_REQUEST_SUCCESS": "退货/退款请求已获得批准。买家将获得退款",
                            "RETURN_OR_REFUND_REQUEST_CANCEL": "请求已被买家或系统取消",
                            "RETURN_OR_REFUND_REQUEST_COMPLETE": "退货/退款已成功处理。买家已退款",
                            "REPLACMENT_REQUEST_PENDING": "买家已发起换货请求。该请求正在等待卖家审核",
                            "REPLACMENT_REQUEST_REJECT": "卖家拒绝买家的换货请求",
                            "REPLACMENT_REQUEST_REFUND_SUCCESS": "由于库存不足，买家的换货请求已通过退款解决",
                            "REPLACMENT_REQUEST_CANCEL": "买家取消了换货请求",
                            "REPLACMENT_REQUEST_COMPLETE": "卖家已批准买家的换货请求，平台将生成新订单供卖家履行"
                        }

            for k in results:
                k = self.handle_objectid(k)
                print(k)
                print(k['orderId'])
                print(k['order']['return_status'])
                print(status_dict[k['order']['return_status']])
                if k['order']['return_status'] not in order_type:
                    order_type.append(k['order']['return_status'])

                # sql = "select rma_status  from t_rma_order where platform_rma_code = '%s'"%order_id
                # res = self.query(sql)
                # print(res[0][0])
                output_data.append({"orderId":k['orderId'],"return_status":k['order']['return_status'],"中文翻译":status_dict[k['order']['return_status']]})
            # # 创建 DataFrame
            # df = pd.DataFrame(output_data)
            # # 输出到 Excel 文件
            # excel_file = '0912.xlsx'
            # df.to_excel(excel_file, index=False)
            #     pull_rma_order(env='test',id=k['_id'],platformId=59)
            print(order_type)
            print(len(order_type))


    def test_sumaitong(self,orderId="8182962096940031"):
        """验证速卖通代发仓库按ships from 分仓，
        """
        # db_list = ["aliexpress_order_struct","allegro_order_struct","douyin_order_struct","jd_manual_order_struct","jd_pop_order_struct","kuaishou_order_struct","lazada_order_struct","leqimall_order_struct","pdd_order_struct","shopee_order_struct","taobao_order_struct","tmall_order_struct","wechat_order_struct","youzan_order_struct","ebay_order_struct","amazon_order_struct"]
        db_list = ["aliexpress_order_struct",]
        order_list = []
        for db in db_list:
            print( "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]  # use your collection name here
            # query = {"$and":[{"order.gmtUpdate":{"$gte":"2023-10-01 00:00:00","$lte":"2023-11-01 23:59:59"}},{"finishFlag":true}]}
            # results= collection.find({ "orderId":"8181863319278236" }).sort('insertTime',pymongo.DESCENDING) # get a single document
            results= collection.find({"$and":[{"order.gmtUpdate":{"$gte":"2024-07-16 00:00:00","$lte":"2024-08-16 23:59:59"}},{"finishFlag":True}]}).sort('insertTime',pymongo.DESCENDING) # get a single document
            for k in results:
                k = self.handle_objectid(k)
                print(k)
                # skus = k['orderDetail']['item_list']
                # for sku in skus:
                #     print(sku['item_sku'])
                # print(json.dumps(k,ensure_ascii=False))
                warehouse_type_list = []
                # try:
                #     for warehouse in k['orderFee']['target']['childOrderList']:
                #         try:
                #             if warehouse['logisticsWarehouseType'] not in warehouse_type_list:
                #                 warehouse_type_list.append(warehouse['logisticsWarehouseType'])
                #         except:
                #             # print(k['orderId']," 自发")
                #             pass
                #     if len(warehouse_type_list) > 1 :
                #         raise KeyError("订单存在混仓？")
                #     elif len(warehouse_type_list) < 1:
                #         pass
                #         # print(k['orderId']," 自发?")
                #     elif len(warehouse_type_list) ==1:
                #         if warehouse_type_list[0] == 'cainiaoInternationalWarehouse':
                #             #拿到所有的ship_from
                #             ship_from_list = []
                #             for ship_from_tmp_list in k['orderFee']['target']['childOrderExtInfoList']:
                #                 tmp =  json.loads(ship_from_tmp_list['sku'])
                #                 # print(tmp['sku'])
                #                 for ship_from in tmp['sku']:
                #                     if ship_from['pName'] == 'Ships From':
                #                         # print(ship_from['pValueId'])
                #                         if ship_from['pValue'] not in ship_from_list:
                #                             ship_from_list.append(ship_from['pValue'])
                #             print(ship_from_list)
                #             if len(ship_from_list) < 1 :
                #                 body =json.loads(k['orderFee']['body'])
                #                 if k['order']['orderStatus'] == 'FINISH' and body['aliexpress_trade_new_redefining_findorderbyid_response']['target']['logistics_status'] != 'BUYER_ACCEPT_GOODS':
                #                     pass
                #                 else:
                #                     print(k['orderId']," : 异常订单，没有ships_from,呆在草稿")
                #             if len(ship_from_list) >1 :
                #                 if 'China' in ship_from_list:
                #                     pass
                #                 else : raise KeyError("订单号：%s 存在多个 ship_from ? "%k['orderId'])
                #             if len(ship_from_list) == 1:
                #                 if ship_from_list[0] == 'Russian Federation':
                #                     # pass
                #                     print(k['orderId'],':艾姆勒俄罗斯仓')
                #                 elif ship_from_list[0] == 'SPAIN' or ship_from_list[0] == 'spain':
                #                     print(k['orderId'],':速卖通西班牙海外仓')
                #                     # pass
                #                 elif ship_from_list[0] == 'China' or ship_from_list[0] == 'CN' or ship_from_list[0] == 'CHINA':
                #                     # pass
                #                     print(k['orderId'],':速卖通香港优选仓(SmallRig)')
                #                 else:
                #                     body =json.loads(k['orderFee']['body'])
                #                     if k['order']['orderStatus'] == 'FINISH' and body['aliexpress_trade_new_redefining_findorderbyid_response']['target']['logistics_status'] != 'BUYER_ACCEPT_GOODS':
                #                         pass
                #                     else:
                #                         print(ship_from_list)
                #                         raise KeyError('订单号： %s 未找到仓库'%k['orderId'])
                # except :
                #     pass
    def test_return_haiwai(self,platformId=45,env='test'):
        """ 洗RMA单
        速卖通：45  lazada:39  shopee:34   ebay:31
        """
        db_list = ["return_order_struct"]
        for db in db_list:
            print(
                 "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]
            query = {"insertTime": {"$gte": "2024-05-23 00:00:00", "$lte": "2024-07-02 23:59:59"},
                     "platformId": platformId,
                     "finishFlag":True
                     }

            results = collection.find(query).sort('insertTime',pymongo.ASCENDING)
            for k in results:
                k = self.handle_objectid(k)
                print(k)
                # pull_rma_order(env=env, id=k['_id'], platformId=platformId)

    def test_return_wdt(self,platformId=59,env='test'):
        """ 洗RMA单
        速卖通：45  lazada:39  shopee:34   ebay:31
        """
        db_list = ["ebay_order_struct"]
        for db in db_list:
            print(
                 "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]
            query = {"insertTime": {"$gte": "2024-08-18 00:00:00", "$lte": "2024-08-27 23:59:59"},
                     # "platformId": 39,
                     "finishFlag":True
                     }

            results = collection.find(query).sort('insertTime',pymongo.ASCENDING)
            for k in results:
                k = self.handle_objectid(k)
                print(k)
                # # if 'TK' in k['orderId']:
                # #     pull_rma_order(env='test', id=k['_id'], platformId=platformId)
                # pull_rma_order(env=env, id=k['_id'], platformId=platformId)




    def test_return(self,type = 2):
        """1  洗订单   2 洗RMA单"""
        db_list = ["return_order_struct"]
        # db_list = ["aliexpress_order_struct"]
        for db in db_list:
            print(
                 "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]
            page_size = 10  # 每页的记录数
            page_number = 1  # 起始页码
            query = {
                "insertTime": {"$gte": "2024-05-01 00:00:00", "$lte": "2024-06-01 23:59:59"},
                "platformId": 39,
                "finishFlag": True
                # "orderId": "6329181164014452"
            }
            is_more_data = True
            while is_more_data :
                results = collection.find(query).skip((page_number - 1) * page_size).limit(page_size).sort('insertTime',pymongo.ASCENDING)
                results_list = list(results)
                if len(results_list) == 0:
                    print("没有更多数据了，退出循环")
                    is_more_data = False
                    break
                # 处理当前页的数据
                for k in results_list:
                    k = self.handle_objectid(k)
                    print(k)
                    if type == 1:
                        pull_order(env='uat', id=k['_id'], platformId=k['platformId'])
                    if type == 2:
                        pull_rma_order(env='uat', id=k['_id'], platformId=k['platformId'])

                print("第%s页结束" % page_number)
                page_number += 1
                results.close()




                # if 'TK' in k['orderId']  :
                #     print(json.dumps(k,ensure_ascii=False))
                #     source_code_list = k['order']['srcTids'].split(',')
                #     print(k['insertTime'])
                #     print(k['_id'])
                #     print(k['orderId'])
                #     print(k['order']['tradeNoList'])
                #     print(source_code_list)
                #     print('------------------------')

    def test_pull_mongo_to_oms(self,platformId=34,env='test'):
        """推送MONGO进订单OMS"""
        from  pull_order import pull_order
        db_list = ["tiktok_order_struct"]
        for db in db_list:
            print( "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]
            total_count = collection.count_documents({ "insertTime": { "$gte": "2024-08-01 00:00:00" ,"$lte": "2024-09-30 23:59:59" },
                                                       "finishFlag":True
                                                       })
            # 定义每页显示的数据量和要查询的页数
            per_page = 1000
            page_number = 1
            # 计算要跳过的文档数量
            skip_count = (page_number - 1) * per_page
            pages = math.ceil(total_count / per_page)
            print(pages)
            print(total_count)
            query = { "insertTime": { "$gte": "2024-01-01 00:00:00" ,"$lte": "2024-05-25 23:59:59" },
                      "finishFlag": True
                      }
            num = 1
            order_list = []
            for i in range(0,pages+1):
                results = collection.find(query).skip(i).limit(per_page).sort('insertTime', pymongo.DESCENDING)  # get a single document
                # print(results)
                for k in results:
                    k = self.handle_objectid(k)
                    print(num)
                    num = num+1
                    # print(k)
                    if k['orderId'] not in order_list:
                        if k['finishFlag'] ==True:
                            if k['platformId'] == 44:
                                k['platformId'] = -2

                            pull_order(env=env, id=k['_id'], platformId=k['platformId'])
                            # print(num)
                            # num = num + 1
                            order_list.append(k['orderId'])
                        else:
                            print(k['_id']," : 跳过不完整订单")

            print("总数：",num)

    def test_lazada(self,orderId="8182962096940031"):
        from  pull_order import pull_order
        db_list = ["return_order_struct"]
        for db in db_list:
            print( "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]
            total_count = collection.count_documents({ "insertTime": { "$gte": "2024-01-25 00:00:00" ,"$lte": "2024-05-25 23:59:59" } })
            # 定义每页显示的数据量和要查询的页数
            per_page = 1000
            page_number = 2
            # 计算要跳过的文档数量
            skip_count = (page_number - 1) * per_page
            pages = math.ceil(total_count / per_page)
            print(pages)
            print(total_count)
            query = { "insertTime": { "$gte": "2024-05-25 00:00:00" ,"$lte": "2024-05-25 23:59:59" } }
            num = 1
            order_list = []
            for i in range(1,pages+1):
                results = collection.find(query).skip(i).limit(per_page).sort('insertTime', pymongo.DESCENDING)  # get a single document
                # print(results)
                for k in results:
                    k = self.handle_objectid(k)
                    # print(k)
                    if k['platformId'] == 39:
                        for j in k['order']['reverse_order_lines']:
                            print(k['order']['trade_order_id'])
                            print(k['_id'])
                            print(j['reverse_status'])
                            print('----------')



    def test_wdt(self,orderId="8182962096940031"):
        from  pull_order import pull_order,pull_rma_order
        db_list = ["return_order_struct"]
        for db in db_list:
            print( "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]
            total_count = collection.count_documents({ "insertTime": { "$gte": "2024-05-27 00:00:00" ,"$lte": "2024-05-27 23:59:59" } })
            # 定义每页显示的数据量和要查询的页数
            per_page = 1000
            page_number = 2
            # 计算要跳过的文档数量
            skip_count = (page_number - 1) * per_page
            pages = math.ceil(total_count / per_page)
            print(pages)
            print(total_count)
            query = { "insertTime": { "$gte": "2024-05-27 00:00:00" ,"$lte": "2024-05-27 23:59:59" } }
            num = 1
            order_list = []
            for i in range(1,pages+1):
                results = collection.find(query).skip(i).limit(per_page).sort('insertTime', pymongo.DESCENDING)  # get a single document
                # print(results)
                for k in results:
                    k = self.handle_objectid(k)

                    # print(json.dumps(k))
                    if 'TK' in  k['orderId'] :
                        # pull_rma_order(env='test', id=k['_id'], platformId=200)
                        try:
                            # print(k)
                            print(k['orderId'])
                            # print(k['returnOrder']['expressCode'])
                            print(k['orderLines']['0']['sourceOrderCode'])
                        except:
                            pass

    def test_ebay_0829(self):

        db_list = ["ebay_order_struct"]
        for db in db_list:
            print(
                "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]
            query = {"insertTime": {"$gte": "2024-11-08 08:00:02", "$lte": "2024-11-08 23:59:59"},
                     "platformId": 31,
                     "finishFlag": True
                     }
            total_count = collection.count_documents(query)


            results = collection.find(query).sort('insertTime', pymongo.ASCENDING)
            total_price_num = []
            sellersku_tax = []
            sellersku_discount = []
            for k in results:
                k = self.handle_objectid(k)
                print(k['orderId'])
                for i in k['order']['data']['transactionArray']['transaction']:
                    # if i['quantityPurchased'] !=1:
                    #     raise ValueError
                    try:
                        tax = i['eBayCollectAndRemitTaxes']['totalTaxAmount']['value']
                    except KeyError:
                        tax = 0
                    print("transactionPrice :",Decimal(i['transactionPrice']['value']))
                    try:
                        print("原产品总价：",i['sellerDiscounts']['originalItemPrice']['value'])
                        total_price_num.append(i['sellerDiscounts']['originalItemPrice']['value'])
                    except KeyError:
                        pass

                    try:
                        if len(i['sellerDiscounts']['sellerDiscount'] )>1:
                            raise  ValueError
                        print("sellerSku店铺优惠：",i['sellerDiscounts']['sellerDiscount'][0]['itemDiscountAmount']['value'])
                        sellersku_discount.append(i['sellerDiscounts']['sellerDiscount'][0]['itemDiscountAmount']['value'])
                    except  KeyError :
                        pass
                    try:
                        print("产品税",i['eBayCollectAndRemitTaxes']['totalTaxAmount']['value'])
                        sellersku_tax.append(i['eBayCollectAndRemitTaxes']['totalTaxAmount']['value'])

                    except KeyError:
                        pass
                    print('********************************************************************************')
            print("mongo 总数： ", total_count)
            print("原产品总价匹配总数：",len(total_price_num))
            print("sellerSku店铺优惠匹配总数：",len(total_price_num))
            print("产品税：",len(sellersku_tax))


    def test_amazon(self,platformId=30,env='test'):
        db_list = ["amazon_order_struct"]
        for db in db_list:
            print(
                "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]
            query = {"insertTime": {"$gte": "2024-08-22 00:00:00", "$lte": "2024-08-22 23:59:59"},
                     "platformId": platformId,
                     # "channelKey": 'channel_31',
                     "finishFlag": True
                     }

            results = collection.find(query).sort('insertTime', pymongo.ASCENDING)
            for k in results:
                k = self.handle_objectid(k)
                print(k)


    def test_lazada_0926(self,platformId=39,env='test'):
        """lazada RMA申请金额
        """
        db_r = 'return_order_struct'
        collection_r = self.db[db_r]

        query_r = {"insertTime": {"$gte": "2024-08-10 00:00:00", "$lte": "2024-09-24 23:59:59"},
                 "platformId": platformId,
                 # "orderId": "442278720115096",
                 "finishFlag": True
                 }
        results_r = collection_r.find(query_r).sort('insertTime', pymongo.ASCENDING)
        for k in results_r:
            k = self.handle_objectid(k)
            # pull_rma_order(env='test', id=k['_id'], platformId=39)
            print("平台退货退款单号：",k['orderId'])
            source_code =k['order']['trade_order_id']
            print("平台订单号：",source_code)
            seller_sku_dict = {}
            for sku in k['orderDetail']['reverseOrderLineDTOList']:
                seller_sku = sku['seller_sku_id']
                seller_sku_dict[f"{seller_sku}"] = sku['refund_amount']/100
            # print(seller_sku_dict)
            db = "lazada_order_struct"
            collection = self.db[db]
            query = {
                     "orderId":f"{source_code}",
                     "finishFlag": True
                     }

            results = collection.find(query).sort('insertTime', pymongo.DESCENDING).limit(1)
            for k in results:
                k = self.handle_objectid(k)
                # print(k['orderDetail']['data'])

                for j in k['orderDetail']['data']:
                    if str(j['sku']) in seller_sku_dict:
                        platforn_discount = Decimal(j['voucher_platform']) + Decimal(j['shipping_fee_discount_platform'])
                        print(j['voucher_platform'])
                        print(j['shipping_fee_discount_platform'])
                        print(seller_sku_dict[f"{j['sku'] }"])
                        # print(platforn_discount)
                        seller_sku_dict[f"{j['sku'] }"] =Decimal(seller_sku_dict[f"{j['sku'] }"]) + Decimal(platforn_discount)
                        seller_sku_dict[f"{j['sku'] }"]  = seller_sku_dict[f"{j['sku'] }"] .quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            print(seller_sku_dict)
            print('---------------------------------------------------')



    def test_shopee_0926(self,platformId=34,env='test'):
        """shopee RMA清洗逻辑
        """
        db_list = ["return_order_struct"]
        for db in db_list:
            print(
                "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]
            query = {"insertTime": {"$gte": "2024-09-23 00:00:00", "$lte": "2024-09-23 23:59:59"},
                     "platformId": platformId,
                     # "channelKey": 'channel_31',
                     "finishFlag": True
                     }

            results = collection.find(query).sort('insertTime', pymongo.ASCENDING)
            for k in results:
                k = self.handle_objectid(k)
                # pull_rma_order(env='test', id=k['_id'], platformId=34)
                # print(k)
                print("平台退货退款单号：",k['orderId'])
                source_code = k['orderDetail']['order_sn']
                print("订单号：",source_code)
                sku_list = []
                return_list = []
                for sku in k['orderDetail']['item']:
                    sku_list.append(sku['variation_sku'])
                    return_list.append({sku['variation_sku']:sku['refund_amount']})

                db = "shopee_order_struct"
                collection_order = self.db[db]
                query_order = {"orderId":source_code,
                               "finishFlag": True
                         }
                res = collection_order.find(query_order).sort('insertTime', pymongo.DESCENDING).limit(1)
                order_sku_list = []
                # order_discount_list = []
                for j in res:
                    for order_sku in j['orderFee']['order_income']['items']:
                        order_sku_list.append(order_sku['model_sku'])
                        # order_discount_list.append({order_sku['item_sku']:(float(order_sku['discount_from_coin'])+float(order_sku['discount_from_voucher_shopee']))/order_sku['quantity_purchased']})
                        for sku in k['orderDetail']['item']:
                            if order_sku['model_sku'] == sku['variation_sku']:
                                # print(sku['item_sku'])
                                # print(sku['refund_amount'])
                                discount = (Decimal(order_sku['discount_from_coin']) + Decimal(order_sku['discount_from_voucher_shopee'])) / Decimal(order_sku['quantity_purchased'])
                                apply_money = Decimal(sku['refund_amount']) + discount*Decimal(sku['amount'])
                                print({sku['variation_sku']: apply_money})

                                print({"sku['refund_amount']": sku['refund_amount']}, {"order_sku['discount_from_voucher_shopee']": order_sku['discount_from_voucher_shopee']},{"order_sku['discount_from_coin']": order_sku['discount_from_coin']})
                    if len(sku_list) == len(order_sku_list):
                        print("全退")

                        print("运费：",j['orderFee']['order_income']['buyer_paid_shipping_fee'])
                    else :
                        print("部分退")


                print("------------------------------------------------------------------------")


    def test_TTS(self,platformId=59):
        db_list = ["tiktok_order_struct"]
        for db in db_list:
            print(
                "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]
            query = {"insertTime": {"$gte": "2024-10-27 00:00:00", "$lte": "2024-10-30 23:59:59"},
                     "platformId": platformId,
                     # "channelKey": 'channel_31',
                     "finishFlag": True
                     }

            results = collection.find(query).sort('insertTime', pymongo.ASCENDING)
            for k in results:
                k = self.handle_objectid(k)
                # print(k)
                pull_order(env='uat',id=k['_id'],platformId=platformId)
                # print("订单号： ",k['orderId'])
                # for data in k['orderDetail']['data']['orders']:
                #     for j in data['line_items']:
                #         total_price = j ['original_price']
                #         seller_discount = j ['seller_discount']
                #         seller_sku = j ['seller_sku']
                #         if len(j['item_tax']) == 1:
                #             tax_amount = j['item_tax'][0].get('tax_amount')
                #         else: raise KeyError('item_tax')
                #         # print("原产品总价",total_price)
                #         # print('seller sku店铺优惠',seller_discount)
                #         # print('产品税',tax_amount)
                #         mysql_res =  self.query(f"select * from t_order_item_cost where source_code = '{k['orderId']}' and external_sku = '{seller_sku}'")
                #         if mysql_res:
                #             mysql_total_price = mysql_res[0]['origin_price']
                #             mysql_seller_discount = mysql_res[0]['coupon_fee']
                #             mysql_tax_amount = mysql_res[0]['product_tax']
                #             if float(total_price) != float(mysql_total_price):
                #                 print("订单号： ", k['orderId'])
                #                 print("seller_sku: ",seller_sku)
                #                 print(f"原产品总价不正确，数据库为 {mysql_total_price},实际应该为{total_price}")
                #             if float(seller_discount) != float(mysql_seller_discount):
                #                 print("订单号： ", k['orderId'])
                #                 print("seller_sku: ", seller_sku)
                #                 print(f"店铺优惠不正确，数据库为 {mysql_seller_discount},实际应该为{seller_discount}")
                #             if float(tax_amount) != float(mysql_tax_amount):
                #                 print("订单号： ", k['orderId'])
                #                 print("seller_sku: ", seller_sku)
                #                 print(f"产品税不正确，数据库为 {mysql_tax_amount},实际应该为{tax_amount}")
                #         print('---------------------------------')




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

                    # print(k['orderFee']['order_income']['shopee_shipping_rebate'])
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





    def tearDown(self):
        self.client.close()

if __name__ == "__main__":
    unittest.main()
