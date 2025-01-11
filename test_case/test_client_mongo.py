import pandas as pd
import pymysql
import unittest
from datetime import datetime
import pymongo
from pymongo import MongoClient
import json
from bson import ObjectId
from pull_order import pull_order

class TestMongoDB(unittest.TestCase):
    def setUp(self):
        # self.client = MongoClient("mongodb://192.168.133.235:27017/?directConnection=true")
        # self.client = MongoClient("mongodb://smallrig:smallrig@192.168.133.233:27017/?authMechanism=DEFAULT&authSource=admin")
        self.client = MongoClient("mongodb://smallrig:smallrig@192.168.133.223:27017/?authMechanism=SCRAM-SHA-1&authSource=smallrig&directConnection=true")
        # self.client = MongoClient("mongodb://smallrig:smallrig@192.168.133.210:27017/?authMechanism=DEFAULT")
        self.db = self.client['smallrig']  # use your database name here
        self.allegro = {"BOUGHT":"已购买未结账","FILLED_IN":"填写了结账信息未付款","READY_FOR_PROCESSING":"付款完成","CANCELLED":"买家取消"}
        self.ebay = {"ACTIVE":"购买未付款","CANCELLED":"取消","COMPLETED":"支付完成","INACTIVE":"不活跃订单","CANCELPENDING":"正在取消","INPROCESS":"处理中"}
        self.shopee = {"UNPAID":"未支付","READY_TO_SHIP":"准备发货","PROCESSED":"打包完成准备发货","SHIPPED":"已发货","COMPLETED":"订单已经完成","IN_CANCEL":"订单正在取消","CANCELLED":"已取消","INVOICE_PENDING":"发票生成中","TO_CONFIRM_RECEIVE":"等待确认签收","TO_RETURN":"TO_RETURN"}
        self.lazada = {"unpaid":"未支付","pending":"待处理","canceled":"已取消","ready_to_ship":"准备发货","delivered":"已送达","returned":"已退回","shipped ":"已发货","failed":"失败","topack":"待打包","toship":"待发货","shipping and lost":"运输中遗失",}
        self.aliexpress = {"WAIT_SELLER_SEND_GOODS":"等待发货","SELLER_PART_SEND_GOODS":"部分发货","WAIT_BUYER_ACCEPT_GOODS": "等待买家收货","FUND_PROCESSING": "买卖家达成一致，资金处理中","PLACE_ORDER_SUCCESS": "等待买家付款","IN_CANCEL": "买家申请取消","IN_ISSUE": "含纠纷中的订单","IN_FROZEN": "冻结中的订单","WAIT_SELLER_EXAMINE_MONEY": "等待您确认金额","RISK_CONTROL": "订单处于风控24小时中，从买家在线支付完成后开始，持续24小时。","FINISH": "订单已关闭结束。包含取消订单、正常交易成功等情况","ARCHIVE": "交易归档"}
        self.douyin = {1: "待确认/待支付（订单创建完毕）", 105: "已支付", 2: "备货中", 101: "部分发货", 3: "已发货（全部发货）", 4: "已取消", 5: "已完成（已收货）"}
        self.wechat = {10: "待付款", 20: "待发货", 21: "部分发货", 30: "待收货", 100: "完成", 200: "全部商品售后之后，订单取消", 250: "未付款用户主动取消或超时未付款订单自动取消"}
        self.taobao = {"TRADE_NO_CREATE_PAY": "没有创建支付宝交易", "WAIT_BUYER_PAY": "等待买家付款", "WAIT_SELLER_SEND_GOODS": "等待卖家发货,即:买家已付款", "WAIT_BUYER_CONFIRM_GOODS": "等待买家确认收货,即:卖家已发货", "TRADE_BUYER_SIGNED": "买家已签收,货到付款专用", "TRADE_FINISHED": "交易成功", "TRADE_CLOSED": "付款以后用户退款成功，交易自动关闭", "TRADE_CLOSED_BY_TAOBAO": "付款以前，卖家或买家主动关闭交易", "PAY_PENDING": "国际信用卡支付付款确认中"}
        self.tmall = {"TRADE_NO_CREATE_PAY": "没有创建支付宝交易", "WAIT_BUYER_PAY": "等待买家付款", "WAIT_SELLER_SEND_GOODS": "等待卖家发货,即:买家已付款", "WAIT_BUYER_CONFIRM_GOODS": "等待买家确认收货,即:卖家已发货", "TRADE_BUYER_SIGNED": "买家已签收,货到付款专用", "TRADE_FINISHED": "交易成功", "TRADE_CLOSED": "付款以后用户退款成功，交易自动关闭", "TRADE_CLOSED_BY_TAOBAO": "付款以前，卖家或买家主动关闭交易", "PAY_PENDING": "国际信用卡支付付款确认中"}
        self.youzan =  {"WAIT_BUYER_PAY": "等待买家付款，定金预售描述：定金待付、等待尾款支付开始、尾款待付", "TRADE_PAID": "订单已支付", "WAIT_CONFIRM": "待确认，包含待成团、待接单等等。即：买家已付款，等待成团或等待接单", "WAIT_SELLER_SEND_GOODS": "等待卖家发货，即：买家已付款", "WAIT_BUYER_CONFIRM_GOODS": "等待买家确认收货，即：卖家已发货", "TRADE_SUCCESS": "买家已签收以及订单成功", "TRADE_CLOSED": "交易关闭"}
        self.leqimall =  {0: "待付款", 1: "待发货", 2: "部分发货", 3: "完全发货", 4: "确认收货", 5: "支付待确认"}
        self.ks = {0: "未知状态", 10: "待付款", 30: "已付款", 40: "已发货", 50: "已签收", 70: "订单成功", 80: "订单失败，订单整单取消会转为订单失败状态"}
        self.jdpop = {"WAIT_SELLER_STOCK_OUT": "等待出库", "WAIT_GOODS_RECEIVE_CONFIRM": "等待确认收货", "WAIT_SELLER_DELIVERY": "等待发货（只适用于海外购商家，含义为'等待境内发货'标签下的订单,非海外购商家无需使用）", "POP_ORDER_PAUSE": "POP暂停", "FINISHED_L": "完成", "TRADE_CANCELED": "取消", "LOCKED": "已锁定", "WAIT_SEND_CODE": "等待发货"}
        self.amazon = {"PendingAvailability": "预购商品,订单已下单，付款未获授权", "PENDING": "订单已下单，但付款未获授权", "UNSHIPPED": "付款已获授权，订单已准备好发货，但订单中的任何商品尚未发货", "PartiallyShipped": "订单中的一件或多件商品 [但不是全部] 已发货", "SHIPPED": "订单中的所有商品均已发货", "InvoiceUnconfirmed": "订单中的所有商品均已发货。卖家尚未向亚马逊确认发票已发送给买家", "CANCELED": "订单已取消", "Unfulfillable": "订单无法配送。此状态仅适用于多渠道配送订单。"}




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


    def test_find(self,orderId="8182962096940031"):

        db_list = ["aliexpress_order_struct","allegro_order_struct","douyin_order_struct","jd_manual_order_struct","jd_pop_order_struct","kuaishou_order_struct","lazada_order_struct","leqimall_order_struct","pdd_order_struct","shopee_order_struct","taobao_order_struct","tmall_order_struct","wechat_order_struct","youzan_order_struct","ebay_order_struct","amazon_order_struct"]
        db_list = ["aliexpress_order_struct",]
        order_list = []
        for db in db_list:
            print( "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]  # use your collection name here
            # query = {"$and":[{"order.gmtUpdate":{"$gte":"2023-10-01 00:00:00","$lte":"2023-11-01 23:59:59"}},{"finishFlag":true}]}
            results= collection.find({ "orderId":"1101960172046159" }).sort('insertTime',pymongo.DESCENDING) # get a single document
            # results= collection.find({"$and":[{"order.gmtUpdate":{"$gte":"2023-12-26 00:00:00","$lte":"2023-12-31 23:59:59"}},{"finishFlag":True}]}).sort('insertTime',pymongo.DESCENDING) # get a single document
            for k in results:
                k = self.handle_objectid(k)
                # print(json.dumps(k,ensure_ascii=False))
                warehouse_type_list = []
                try:
                    for warehouse in k['orderFee']['target']['childOrderList']:
                        try:
                            if warehouse['logisticsWarehouseType'] not in warehouse_type_list:
                                warehouse_type_list.append(warehouse['logisticsWarehouseType'])
                        except:
                            # print(k['orderId']," 自发")
                            pass
                    if len(warehouse_type_list) > 1 :
                        raise KeyError("订单存在混仓？")
                    elif len(warehouse_type_list) < 1:
                        pass
                        # print(k['orderId']," 自发?")
                    elif len(warehouse_type_list) ==1:
                        if warehouse_type_list[0] == 'cainiaoInternationalWarehouse':
                            #拿到所有的ship_from
                            ship_from_list = []
                            for ship_from_tmp_list in k['orderFee']['target']['childOrderExtInfoList']:
                                tmp =  json.loads(ship_from_tmp_list['sku'])
                                # print(tmp['sku'])
                                for ship_from in tmp['sku']:
                                    if ship_from['pName'] == 'Ships From':
                                        # print(ship_from['pValueId'])
                                        if ship_from['pValue'] not in ship_from_list:
                                            ship_from_list.append(ship_from['pValue'])
                            print(ship_from_list)
                            if len(ship_from_list) < 1 :
                                body =json.loads(k['orderFee']['body'])
                                if k['order']['orderStatus'] == 'FINISH' and body['aliexpress_trade_new_redefining_findorderbyid_response']['target']['logistics_status'] != 'BUYER_ACCEPT_GOODS':
                                    pass
                                else:
                                    print(k['orderId']," : 异常订单，没有ships_from,呆在草稿")
                            if len(ship_from_list) >1 :
                                if 'China' in ship_from_list:
                                    pass
                                else : raise KeyError("订单号：%s 存在多个 ship_from ? "%k['orderId'])
                            if len(ship_from_list) == 1:
                                if ship_from_list[0] == 'Russian Federation':
                                    # pass
                                    print(k['orderId'],':艾姆勒俄罗斯仓')
                                elif ship_from_list[0] == 'SPAIN' or ship_from_list[0] == 'spain':
                                    print(k['orderId'],':速卖通西班牙海外仓')
                                    # pass
                                elif ship_from_list[0] == 'China' or ship_from_list[0] == 'CN' or ship_from_list[0] == 'CHINA':
                                    # pass
                                    print(k['orderId'],':速卖通香港优选仓(SmallRig)')
                                else:
                                    body =json.loads(k['orderFee']['body'])
                                    if k['order']['orderStatus'] == 'FINISH' and body['aliexpress_trade_new_redefining_findorderbyid_response']['target']['logistics_status'] != 'BUYER_ACCEPT_GOODS':
                                        pass
                                    else:
                                        print(ship_from_list)
                                        raise KeyError('订单号： %s 未找到仓库'%k['orderId'])
                except :
                    pass






    def test_find_all_day(self,orderId="8182962096940031"):

        db_list = ["aliexpress_order_struct"]
        for db in db_list:
            print( "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]
            query = { "order.gmtUpdate": { "$gte": "2023-12-26 00:00:00" ,"$lte": "2023-12-30 23:59:59" } }
            results = collection.find(query).limit(1).sort('insertTime', pymongo.DESCENDING)  # get a single document
            order_list = []
            for k in results:
                k = self.handle_objectid(k)
                pull_order(env='test',id=k['_id'],platformId=45)
                # print(k)
                print(json.dumps(k, ensure_ascii=False))





    def tearDown(self):
        self.client.close()

if __name__ == "__main__":
    unittest.main()
