import unittest
from datetime import datetime
import pymongo
from pymongo import MongoClient
import json
from bson import ObjectId


class TestMongoDB(unittest.TestCase):
    def setUp(self):
        # self.client = MongoClient("mongodb://smallrig:smallrig@192.168.133.234:27017/?authMechanism=SCRAM-SHA-1&authSource=smallrig&directConnection=true")
        self.client = MongoClient("mongodb://192.168.133.235:27017/?directConnection=true")
        self.db = self.client['smallrig']  # use your database name here
        self.allegro = {"BOUGHT":"已购买未结账","FILLED_IN":"填写了结账信息未付款","READY_FOR_PROCESSING":"付款完成","CANCELLED":"买家取消"}
        self.ebay = {"Active":"购买未付款","COMPLETED":"取消","Completed":"支付完成","Inactive":"不活跃订单","CancelPending":"正在取消","InProcess":"处理中"}
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
        self.amazon = {"PendingAvailability": "预购商品,订单已下单，付款未获授权", "PENDING": "订单已下单，但付款未获授权", "Unshipped": "付款已获授权，订单已准备好发货，但订单中的任何商品尚未发货", "PartiallyShipped": "订单中的一件或多件商品 [但不是全部] 已发货", "SHIPPED": "订单中的所有商品均已发货", "InvoiceUnconfirmed": "订单中的所有商品均已发货。卖家尚未向亚马逊确认发票已发送给买家", "CANCELED": "订单已取消", "Unfulfillable": "订单无法配送。此状态仅适用于多渠道配送订单。"}




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


    def test_find(self):

        db_list = ["aliexpress_order_struct","allegro_order_struct","douyin_order_struct","jd_manual_order_struct","jd_pop_order_struct","kuaishou_order_struct","lazada_order_struct","leqimall_order_struct","pdd_order_struct","shopee_order_struct","taobao_order_struct","tmall_order_struct","wechat_order_struct","youzan_order_struct","ebay_order_struct","amazon_order_struct"]
        # print(len(db_list))
        # db_list = ["ebay_order_struct"]
        with open("mongoData.txt", "w",encoding="utf-8") as outfile:
            for db in db_list:
                outfile.write( "-----------------------------------------" + db + "----------------------------------------------" + "\n")
                print( "-----------------------------------------" + db + "----------------------------------------------" + "\n")
                collection = self.db[db]  # use your collection name here
                # doc = collection.find({"$and": [{"channelKey":"Aliexpress-CN-SR"},{"orderId":"8176722016152403"}]}).limit(300).sort('insertTime',pymongo.DESCENDING) # get a single document
                results= collection.find().limit(1000000).sort('insertTime',pymongo.DESCENDING) # get a single document
                result_list = list(results)
                order_list = []
                order_list_repeat = []

                for i in result_list:
                    data = json.dumps(i,default=str)
                    data = json.loads(data)
                    # print(json.dumps(data,ensure_ascii=False))
                    if data['orderId'] not in order_list:
                        order_list.append(data['orderId'])
                    else:
                        if data['orderId'] not in order_list_repeat:
                            order_list_repeat.append(data['orderId'])
                        # print("订单号重复:")
                print(order_list)
                print(order_list_repeat)

                for j in order_list_repeat:
                    # print(j)
                    count = collection.count_documents({"orderId":"%s"%j})
                    # print(type(results))
                    # print(results)
                    if count > 2:
                        results_list = collection.find({"orderId":"%s"%j}).limit(1000000).sort('insertTime', pymongo.DESCENDING)
                        print(count)
                        print(j)

                        outfile.write(str(j)+"\n")
                        for k in results_list:
                            # print(k)
                            k = self.handle_objectid(k)  # 使用我们定义的函数转化 ObjectId
                            # write_data = json.dumps(k,ensure_ascii=False)  # 将字典转化为 JSON 字符串
                            # print(json.dumps(k))
                            # outfile.write(k['orderId']+"-------->"+"platformId :"+str(k['platformId']) +" channelId: "+str(k['channelId'])+" channelKey: "+k['channelKey'] +" insertTime:"+str(k['insertTime'])+ '\n')
                            # outfile.write(write_data)
                            if db == "aliexpress_order_struct" :
                                outfile.write(k['orderId'] + "-------->" + "platformId :" + str(k['platformId']) + " channelId: " + str(k['channelId']) + " channelKey: " + k['channelKey'] + " insertTime:" + str(k['insertTime']) +" 状态："+self.aliexpress[str(k["order"]["fundStatus"])]+ '\n')
                            if db =="allegro_order_struct" :
                                outfile.write(k['orderId'] + "-------->" + "platformId :" + str(k['platformId']) + " channelId: " + str(k['channelId']) + " channelKey: " + k['channelKey'] + " insertTime:" + str(k['insertTime']) + " 状态：" +self.allegro[str(k["order"]["status"])] + '\n')
                            if db == "douyin_order_struct":
                                outfile.write(k['orderId'] + "-------->" + "platformId :" + str(k['platformId']) + " channelId: " + str(k['channelId']) + " channelKey: " + k['channelKey'] + " insertTime:" + str(k['insertTime']) + " 状态：" +self.douyin[k["order"]["order_status"] ]+ '\n')
                            if db == "jd_manual_order_struct":
                                outfile.write(k['orderId'] + "-------->" + "platformId :" + str(k['platformId']) + " channelId: " + str(k['channelId']) + " channelKey: " + k['channelKey'] + " insertTime:" + str(k['insertTime']) + " 状态：" +str(k["order"]["orderState"]) + '\n')
                            if db == "jd_pop_order_struct":
                                outfile.write(k['orderId'] + "-------->" + "platformId :" + str(k['platformId']) + " channelId: " + str(k['channelId']) + " channelKey: " + k['channelKey'] + " insertTime:" + str(k['insertTime']) + " 状态：" +self.jdpop[k["order"]["orderState"]] + '\n')
                            if db == "kuaishou_order_struct":
                                outfile.write(k['orderId'] + "-------->" + "platformId :" + str(k['platformId']) + " channelId: " + str(k['channelId']) + " channelKey: " + k['channelKey'] + " insertTime:" + str(k['insertTime']) + " 状态：" +self.ks[k["order"]["orderBaseInfo"]["status"]] + '\n')
                            if db == "lazada_order_struct":
                                outfile.write(k['orderId'] + "-------->" + "platformId :" + str(k['platformId']) + " channelId: " + str(k['channelId']) + " channelKey: " + k['channelKey'] + " insertTime:" + str(k['insertTime']) + " 状态：" +str(k["order"]["statuses"]) + '\n')
                            if db == "leqimall_order_struct":
                                outfile.write(k['orderId'] + "-------->" + "platformId :" + str(k['platformId']) + " channelId: " + str(k['channelId']) + " channelKey: " + k['channelKey'] + " insertTime:" + str(k['insertTime']) + " 状态：" +self.leqimall[k["order"]["orderStatus"]] + '\n')
                            if db == "pdd_order_struct":
                                outfile.write(k['orderId'] + "-------->" + "platformId :" + str(k['platformId']) + " channelId: " + str(k['channelId']) + " channelKey: " + k['channelKey'] + " insertTime:" + str(k['insertTime']) + " 状态：" +str(k["order"]["order_status"]) + '\n')
                            if db == "shopee_order_struct":
                                outfile.write(k['orderId'] + "-------->" + "platformId :" + str(k['platformId']) + " channelId: " + str(k['channelId']) + " channelKey: " + k['channelKey'] + " insertTime:" + str(k['insertTime']) + " 状态：" +self.shopee[str(k["order"]["order_status"])] + '\n')
                            if db == "taobao_order_struct":
                                outfile.write(k['orderId'] + "-------->" + "platformId :" + str(k['platformId']) + " channelId: " + str(k['channelId']) + " channelKey: " + k['channelKey'] + " insertTime:" + str(k['insertTime']) + " 状态：" +self.taobao[str(k["order"]["status"])] + '\n')
                            if db == "tmall_order_struct":
                                outfile.write(k['orderId'] + "-------->" + "platformId :" + str(k['platformId']) + " channelId: " + str(k['channelId']) + " channelKey: " + k['channelKey'] + " insertTime:" + str(k['insertTime']) + " 状态：" +self.tmall[str(k["order"]["status"])] + '\n')
                            if db == "wechat_order_struct":
                                outfile.write(k['orderId'] + "-------->" + "platformId :" + str(k['platformId']) + " channelId: " + str(k['channelId']) + " channelKey: " + k['channelKey'] + " insertTime:" + str(k['insertTime']) + " 状态：" +self.wechat[k['orderDetail']["status"]] + '\n')
                            if db == "youzan_order_struct":
                                outfile.write(k['orderId'] + "-------->" + "platformId :" + str(k['platformId']) + " channelId: " + str(k['channelId']) + " channelKey: " + k['channelKey'] + " insertTime:" + str(k['insertTime']) + " 状态：" +self.youzan[str(k["order"]["order_info"]["status"])] + '\n')
                            if db == "ebay_order_struct":
                                outfile.write(k['orderId'] + "-------->" + "platformId :" + str(k['platformId']) + " channelId: " + str(k['channelId']) + " channelKey: " + k['channelKey'] + " insertTime:" + str(k['insertTime']) + " 状态：" +self.ebay[str(k["order"]["data"]["orderStatus"])] + '\n')
                            if db == "amazon_order_struct":
                                outfile.write(k['orderId'] + "-------->" + "platformId :" + str(k['platformId']) + " channelId: " + str(k['channelId']) + " channelKey: " + k['channelKey'] + " insertTime:" + str(k['insertTime']) + " 状态：" +self.amazon[str(k["order"]["orderStatus"])] + '\n')








                        outfile.write("\n")



    def tearDown(self):
        self.client.close()

if __name__ == "__main__":
    unittest.main()
