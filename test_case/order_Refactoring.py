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
        # self.client = MongoClient("mongodb://smallrig:smallrig@192.168.133.223:27017/?authMechanism=SCRAM-SHA-1&authSource=smallrig&directConnection=true")
        # self.client = MongoClient("mongodb://smallrig:smallrig@192.168.133.210:27017/?authMechanism=DEFAULT")
        self.client = MongoClient("mongodb://smallrig:smallrig@192.168.133.223:27017/?authMechanism=SCRAM-SHA-1&authSource=smallrig&directConnection=true")
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

        # self.connection = pymysql.connect(host='192.168.133.213', password='root', db='smallrig-platform')
        self.connection = pymysql.connect(host='192.168.133.210',  # 数据库地址
                                          user='root',  # 数据库用户名
                                          password='Leqi!2022',  # 数据库密码
                                          db='smallrig-platform')  # 数据库名称
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


    def test_find(self):

        db_list = ["aliexpress_order_struct","allegro_order_struct","douyin_order_struct","jd_manual_order_struct","jd_pop_order_struct","kuaishou_order_struct","lazada_order_struct","leqimall_order_struct","pdd_order_struct","shopee_order_struct","taobao_order_struct","tmall_order_struct","wechat_order_struct","youzan_order_struct","ebay_order_struct","amazon_order_struct"]
        column_name = ["platformId","channelId","channelKey","orderId","insertTime","status"]
        # print(len(db_list))
        db_list = ["tmall_order_struct"]
        aliexpress_list_data = []
        douyin_list_data = []
        allegro_list_data = []
        jd_manual_list_data = []
        jd_pop_list_data = []
        kuaishou_list_data = []
        lazada_list_data = []
        leqimall_list_data = []
        pdd_list_data = []
        shopee_list_data = []
        taobao_list_data = []
        tmall_list_data = []
        wechat_list_data = []
        youzan_list_data = []
        ebay_list_data = []
        amazon_list_data = []

        for db in db_list:
            print( "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]  # use your collection name here
            results= collection.find().limit(2000).sort('insertTime',pymongo.DESCENDING) # get a single document
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
            print(order_list)
            print(order_list_repeat)

            # douyin_list_data = []
            for j in order_list:
                # print(j)
                count = collection.count_documents({"orderId":"%s"%j})

                if count > 1:
                    results_list = collection.find({"orderId":"%s"%j}).limit(100).sort('insertTime', pymongo.ASCENDING)
                    start_data = 1
                    for k in results_list:
                        if start_data == 1:
                            pass
                        else:
                            k = self.handle_objectid(k)  # 使用我们定义的函数转化 ObjectId
                            if db == "aliexpress_order_struct" :
                                write_data ={ "id":k['_id'],"platformId":k['platformId'],"channelId":k['channelId'],"channelKey":k['channelKey'],"orderId":k['orderId'],"insertTime":k['insertTime'],"status":k["order"]["orderStatus"],"data":json.dumps(k)}
                                aliexpress_list_data.append(write_data)
                                print('--------------------------------------------')
                                print(k['orderId'])
                                # print(k)
                                # print(k['orderFee']['target']['childOrderList'])
                                try:
                                    for warehouse in k['orderFee']['target']['childOrderList']:
                                        print(warehouse['logisticsWarehouseType'])
                                        print("平台仓发货")
                                        # print(json.dumps(warehouse))
                                except:
                                    print("自发")

                            if db =="allegro_order_struct" :
                                allegro_data = {"id":k['_id'],"platformId": k['platformId'], "channelId": k['channelId'],  "channelKey": k['channelKey'], "orderId": k['orderId'],"insertTime": k['insertTime'],"status": self.allegro[k["order"]["status"]],"data":json.dumps(k)}
                                allegro_list_data.append(allegro_data)
                            if db == "douyin_order_struct":
                                douyin_data = {"id":k['_id'],"platformId": k['platformId'], "channelId": k['channelId'], "channelKey": k['channelKey'], "orderId": k['orderId'], "insertTime": k['insertTime'], "status": self.douyin[k["order"]["order_status"]],"data":json.dumps(k)}
                                douyin_list_data.append(douyin_data)
                                # SQL = "SELECT order_status ,step FROM `smallrig-platform`.t_order_base  WHERE source_code = '%s'"%k['orderId']
                                # result = self.query(SQL)
                                # if len(result) != 0:
                                #     if result[0][0] == 1 and result[0][1] ==100:
                                #         if k['order']['pay_time'] > 0 and k['syncFlag'] == True:
                                #             print("已付款订单在草稿: ",j,"  pay_time:",k['order']['pay_time'])
                                if len(k['order']['sku_order_list'])>1:
                                    print("-------------------------------------------")
                                    print(k['orderId'])
                                    print(len(k['order']['sku_order_list']))

                            if db == "jd_manual_order_struct":
                                jd_manual_data = {"id":k['_id'],"platformId": k['platformId'], "channelId": k['channelId'],"channelKey": k['channelKey'], "orderId": k['orderId'],"insertTime": k['insertTime'], "status": k["order"]["orderState"],"data":json.dumps(k)}
                                jd_manual_list_data.append(jd_manual_data)

                            if db == "jd_pop_order_struct":
                                jd_pop_data = {"id":k['_id'],"platformId": k['platformId'], "channelId": k['channelId'],
                                                  "channelKey": k['channelKey'], "orderId": k['orderId'],
                                                  "insertTime": k['insertTime'], "status": self.jdpop[k["order"]["orderState"]],"data":json.dumps(k)}
                                jd_pop_list_data.append(jd_pop_data)
                            if db == "kuaishou_order_struct":
                                kuaishou_data = {"id":k['_id'],"platformId": k['platformId'], "channelId": k['channelId'],
                                               "channelKey": k['channelKey'], "orderId": k['orderId'],
                                               "insertTime": k['insertTime'],
                                               "status": self.ks[k["order"]["orderBaseInfo"]["status"]],"data":json.dumps(k)}
                                kuaishou_list_data.append(kuaishou_data)
                            if db == "lazada_order_struct":
                                lazada_data = {"id":k['_id'],"platformId": k['platformId'], "channelId": k['channelId'],
                                                 "channelKey": k['channelKey'], "orderId": k['orderId'],
                                                 "insertTime": k['insertTime'],
                                                 "status": k["order"]["statuses"],"data":json.dumps(k)}
                                lazada_list_data.append(lazada_data)
                                print("---------------------------------------------")
                                print(k['orderId'])
                                try:
                                    # print(k['orderDetail']['data'])
                                    tmp_status = []
                                    for skulist in k['orderDetail']['data']:
                                        print(skulist['status'])
                                        if skulist['warehouse_code'] =="dropshipping":

                                            print("商家自发:",skulist['sku'])

                                            if "商家自发" not in tmp_status:
                                                tmp_status.append("商家自发")
                                        else:
                                            print("平台仓自发")
                                            if "平台仓自发" not in tmp_status:
                                                tmp_status.append("平台仓自发")
                                    if len(tmp_status)==2:
                                        print("混仓发货")

                                except KeyError:
                                    pass
                            if db == "leqimall_order_struct":
                                leqimall_data = {"id":k['_id'],"platformId": k['platformId'], "channelId": k['channelId'],
                                               "channelKey": k['channelKey'], "orderId": k['orderId'],
                                               "insertTime": k['insertTime'],
                                               }
                                leqimall_list_data.append(leqimall_data)
                            if db == "pdd_order_struct":
                                pdd_data = {"id":k['_id'],"platformId": k['platformId'], "channelId": k['channelId'],
                                                 "channelKey": k['channelKey'], "orderId": k['orderId'],
                                                 "insertTime": k['insertTime'],
                                                 "status": k["order"]["order_status"],"data":json.dumps(k)}
                                pdd_list_data.append(pdd_data)
                            if db == "shopee_order_struct":
                                shopee_data = {"id":k['_id'],"platformId": k['platformId'], "channelId": k['channelId'],
                                            "channelKey": k['channelKey'], "orderId": k['orderId'],
                                            "insertTime": k['insertTime'],
                                            "status": self.shopee[str(k["order"]["order_status"])],"data":json.dumps(k)}
                                shopee_list_data.append(shopee_data)
                            if db == "taobao_order_struct":
                                taobao_data = {"id":k['_id'],"platformId": k['platformId'], "channelId": k['channelId'],
                                               "channelKey": k['channelKey'], "orderId": k['orderId'],
                                               "insertTime": k['insertTime'],
                                               "status": self.taobao[str(k["order"]["status"])],"data":json.dumps(k)}
                                taobao_list_data.append(taobao_data)
                            if db == "tmall_order_struct":
                                tmall_data = {"id":k['_id'],"platformId": k['platformId'], "channelId": k['channelId'],
                                               "channelKey": k['channelKey'], "orderId": k['orderId'],
                                               "insertTime": k['insertTime'],
                                               "status": self.tmall[str(k["order"]["status"])],"data":json.dumps(k)}
                                tmall_list_data.append(tmall_data)
                                pull_order(k['_id'],47)
                                is_pay = k["order"]["jdp_response"]
                                is_pay = json.loads(is_pay)
                                is_pay = is_pay['trade_fullinfo_get_response']['trade'].get('pay_time')
                                # print(is_pay)
                                # 取消
                                if k["order"]["status"] == "TRADE_CLOSED" or k["order"][
                                    "status"] == 'TRADE_CLOSED_BY_TAOBAO':
                                    SQL = "select step ,order_status from t_order_base where source_code = '%s'" % k[
                                        'orderId']
                                    result = self.query(SQL)
                                    if result[0][1] == 6:
                                        print(k['orderId'], ":", "状态验证通过", "数据库状态：", result[0][1])
                                #判断是否支付
                                if is_pay is not None:
                                    print(is_pay)
                                    SQL="select step ,order_status from t_order_base where source_code = '%s'"%k['orderId']
                                    print(SQL)
                                    result = self.query(SQL)
                                    # print(result)
                                    # if result[0][0] == 101:
                                    if result[0][1] == 2 :
                                        print(k['orderId'],":","状态验证通过","数据库状态：",result[0][1])
                                    else:
                                        print("状态验证不通过")
                                else:
                                    SQL = "select step ,order_status from t_order_base where source_code = '%s'" % k[
                                        'orderId']
                                    print(SQL)
                                    result = self.query(SQL)
                                    if result[0][1] == 1 :
                                        print(k['orderId'],":","状态验证通过","数据库状态：",result[0][1])
                                    else:
                                        print("状态验证不通过")

                                if k["order"]["status"] == 0:
                                    pass




                            if db == "wechat_order_struct":
                                wechat_data = {"id":k['_id'],"platformId": k['platformId'], "channelId": k['channelId'],
                                              "channelKey": k['channelKey'], "orderId": k['orderId'],
                                              "insertTime": k['insertTime'],
                                              "status": self.wechat[k['orderDetail']["status"]],"data":json.dumps(k)}
                                wechat_list_data.append(wechat_data)
                            if db == "youzan_order_struct":
                                print(k)
                                youzan_data = {"id":k['_id'],"platformId": k['platformId'], "channelId": k['channelId'],
                                               "channelKey": k['channelKey'], "orderId": k['orderId'],
                                               "insertTime": k['insertTime'],
                                               "data":k}
                                youzan_list_data.append(youzan_data)
                            if db == "ebay_order_struct":
                                ebay_data = {"id":k['_id'],"platformId": k['platformId'], "channelId": k['channelId'],
                                               "channelKey": k['channelKey'], "orderId": k['orderId'],
                                               "insertTime": k['insertTime'],
                                               }
                                ebay_list_data.append(ebay_data)
                                SQL = "SELECT order_status ,step FROM `smallrig-platform`.t_order_base  WHERE source_code = '%s'" % \
                                      k['orderId']
                                result = self.query(SQL)
                                print('-----------------------------------')
                                # print(result)
                                print(j)
                                print("状态 ：",k['order']['data']['orderStatus']) #状态
                                try :
                                    print("是否支付： ",k['order']['data']['monetaryDetails']['payments']['payment'][0]['paymentStatus'])
                                except Exception as e:
                                    print("error:",e)
                                try:
                                    if "FulfillmentBy" in k['order']['data']['transactionArray']['transaction'][0]['any'][0]:
                                        print("平台仓发货")
                                        SQL = "SELECT order_tags FROM  t_order_base WHERE source_code = '%s'"%k['orderId']
                                        res = self.query(SQL)
                                        # print(res[0])
                                        if "ISS_SEND" in res[0][0] :
                                            print("数据库ebay平台仓发货标签校验通过")
                                        else:
                                            raise  Exception ('------------------------------------数据库ebay平台仓校验error----------------')
                                except Exception as e:
                                    print(e)


                            if db == "amazon_order_struct":
                                amazon_data = {"id":k['_id'],"platformId": k['platformId'], "channelId": k['channelId'],
                                             "channelKey": k['channelKey'], "orderId": k['orderId'],
                                             "insertTime": k['insertTime'],
                                             "status": self.amazon[str(k["order"]["orderStatus"])],"data":k}
                                amazon_list_data.append(amazon_data)
                        start_data = start_data + 1


        aliexpress = pd.DataFrame(aliexpress_list_data)
        douyin = pd.DataFrame(douyin_list_data)

        allegro = pd.DataFrame(allegro_list_data)
        jd_manual = pd.DataFrame(jd_manual_list_data)
        jd_pop = pd.DataFrame(jd_pop_list_data)
        kuaishou = pd.DataFrame(kuaishou_list_data)
        lazada = pd.DataFrame(lazada_list_data)
        leqimall = pd.DataFrame(leqimall_list_data)
        pdd = pd.DataFrame(pdd_list_data)
        shopee = pd.DataFrame(shopee_list_data)
        taobao = pd.DataFrame(taobao_list_data)
        tmall = pd.DataFrame(tmall_list_data)
        wechat = pd.DataFrame(wechat_list_data)
        youzan = pd.DataFrame(youzan_list_data)
        ebay = pd.DataFrame(ebay_list_data)
        amazon = pd.DataFrame(amazon_list_data)


        with pd.ExcelWriter('../ipoData/1229001.xlsx') as writer:
            aliexpress.to_excel(writer, sheet_name="aliexpress_order_struct", index=False)
            douyin.to_excel(writer, sheet_name="douyin_order_struct", index=False)
            allegro.to_excel(writer, sheet_name="allegro_order_struct", index=False)
            jd_manual.to_excel(writer, sheet_name="jd_manual_order_struct", index=False)
            jd_pop.to_excel(writer, sheet_name="jd_pop_order_struct", index=False)
            kuaishou.to_excel(writer, sheet_name="kuaishou_order_struct", index=False)
            lazada.to_excel(writer, sheet_name="lazada_order_struct", index=False)
            leqimall.to_excel(writer, sheet_name="leqimall_order_struct", index=False)
            pdd.to_excel(writer, sheet_name="pdd_order_struct", index=False)
            shopee.to_excel(writer, sheet_name="shopee_order_struct", index=False)
            taobao.to_excel(writer, sheet_name="taobao_order_struct", index=False)
            tmall.to_excel(writer, sheet_name="tmall_order_struct", index=False)
            wechat.to_excel(writer, sheet_name="wechat_order_struct", index=False)
            youzan.to_excel(writer, sheet_name="youzan_order_struct", index=False)
            ebay.to_excel(writer, sheet_name="ebay_order_struct", index=False)
            amazon.to_excel(writer, sheet_name="amazon_order_struct", index=False)










    def tearDown(self):
        self.client.close()

if __name__ == "__main__":
    unittest.main()
