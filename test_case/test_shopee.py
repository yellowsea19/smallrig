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






    def test_shoppee_return_order(self,platformId = 34, platform_rma_code_list = ['2405280HP31K5Y8']):
        out_data_list = []
        for platform_rma_code in platform_rma_code_list:
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

                    order_db = "shopee_order_struct"
                    source_code = jsonpath(k, '$.order.order_sn')[0]
                    print("平台订单号： ", source_code)
                except KeyboardInterrupt:
                    print("mongo中无该退货退款单数据 ： ", platform_rma_code)
                except StopIteration:
                    print("mongo中无该退货退款单数据 ： ", platform_rma_code)

                try:
                    order_query = {"orderId": f'{source_code}',
                                   "finishFlag": True}
                    collection_order = self.db[order_db]
                    order_result = collection_order.find(order_query).sort('insertTime', pymongo.DESCENDING)
                    order_info = next(order_result)
                    order_id = order_info['_id']

                    # 清洗订单数据 & 售后单
                    pull_order(env=self.env, id=order_id, platformId=platformId)
                    time.sleep(1)
                    # 把订单改成已发货
                    update_order_status_sql = "update t_order_base set order_status = 4 where source_code = '%s'" % \
                                              order_info['orderId']
                    # self.update(update_order_status_sql)
                    # 若退货退款单已存在，则删除重新清洗
                    del_rma_order_sql = 'delete from t_rma_order where platform_rma_code = "%s"' % platform_rma_code
                    self.delete(del_rma_order_sql)
                    pull_rma_order(env=self.env, id=k['_id'], platformId=platformId)
                    print("orderId",order_id)

                    needs_logistics = jsonpath(k,"$.orderDetail.needs_logistics")
                    print("needs_logistics : ",needs_logistics)
                    if len(needs_logistics) != 1:
                        raise ValueError(f"{needs_logistics} 有多个needs_logistics")
                    # 查询数据库rma_type的值
                    mysql_result_rma_type_sql = "select rma_type from t_rma_order where platform_rma_code = '%s'" % platform_rma_code
                    result = self.query(mysql_result_rma_type_sql)
                    for i in result:
                        result_rma_type = i['rma_type']
                    # 查询数据库return_type 的值
                    mysql_result_return_type_sql = "select return_type from t_rma_order_return where rma_id =  (select id from t_rma_order where platform_rma_code = '%s')" % platform_rma_code
                    result = self.query(mysql_result_return_type_sql)
                    for i in result:
                        result_return_type = i['return_type']

                    # refund_type查询数据库 的值
                    mysql_result_refund_type = "select refund_type from t_rma_order_refund where rma_code =  (select rma_code from t_rma_order where platform_rma_code = '%s')" % platform_rma_code
                    result = self.query(mysql_result_refund_type)
                    for i in result:
                        result_refund_type = i['refund_type']
                    try:
                        if needs_logistics[0]  :
                            print("RMA类型为：退货&退款")
                            # RMA类型：1=换货,2=退货,3=退货换货,4=退款,5=退款换货,6=退货退款,7=退货退款换货
                            self.assertEqual(result_rma_type, 6)
                            print("退款类型为：已发货退货退款")
                            # 退款类型 12 已发货仅退款  1 已发货退货退款
                            self.assertEqual(result_refund_type, 1)

                        else:
                            print("RMA类型为：退款")
                            # RMA类型：1=换货,2=退货,3=退货换货,4=退款,5=退款换货,6=退货退款,7=退货退款换货
                            self.assertEqual(result_rma_type, 4)
                            print("退款类型为：已发货仅退款")
                            # 退款类型 12 已发货仅退款  1 已发货退货退款
                            self.assertEqual(result_refund_type, 12)

                    except AssertionError as e:
                        print(e)
                        raise ValueError('断言出错了')

                except UnboundLocalError:
                    print("mongo 中没有订单数据的版本，订单号： ", source_code)
                except StopIteration:
                    print("mongo 中没有订单数据的版本，订单号： ", source_code)


    def test_0120(self):
        platform_rma_code_list = ["2501150GK962UTC","2501140EDB10BV5","2501130DY2V4BD9","2501130BPHFM0RS","2501120A3D90UKC","2501110790TYK2N","25011006GJ2UV9Q","25011004R47UEQA","25011004Q48G9RD","25010903S9KHNKA","250109020XDD84V","25010800PXR4DUE","2501070UDSF3G11","2501070U7X9Y8JR","2501050Q032F7TK","2501050PVJ5X0GE","2501050NWCY21X0","2501040MC1DD6C0","2501040KH2JJCMT","2501040JAP511VE","2501030GB6G3UQB","2501020EVJFEC51","2501010CXB4RJ39","2501010CAT77NEK","2501010BVJJEQNP","2501010BVETAW9F","2501010BGKKQDB6","2412310A71K4HKK","2412310A1XDSBUF","241231094B67FNK","241231094GVBG2A","24123108TYRMTC8","2412300767VCK85","241229042MX885T","24122903EDFNRHD","24122802T17HS5S","24122802AJR4X8B","24122801SCP8UG7","24122801BTF7HB0","24122800F7Q3SJV","2412260TX0Y8F0T","2412260TWYVYN27","2412260TUW1UVC1","2412260SFVBHFRK","2412250R0FGCJSW","2412250QJF69RSF","2412240KQB5QFDE","2412220G3T4HQFS","2412210E2R4VDMF","2412210DUNE7NYV","2412200BPS6KUUH","2412200BHRP34QW","2412200B7FU8SCW","241219094FFJCHR","24121908T9EBX4A","24121908JJ4S2WN","24121908HP49FTN","24121908EP1Q04X","241219087WRV6DN","24121907QYWD29K","2412180680JXU9W","24121804EFKNGG3","24121703USCGHU5","241217038R8C8JK","241216019KDKF39","2412150U95XC43X","2412150TBD1JTHT","2412140SQAM6U97","2412140SBF61KQD","2412140RN9H51C6","2412140RCPHK7F4","2412130Q0386CJY","2412130PPN1XWQ0","2412130P567K360","2412120M7TTM3PJ","2412120KK6NQRTX","2412110H3056DVP","2412110GW7YGJ1D","2412100FCMWRE1Y","2412100EV8EX0CU","2412090CVEE5N07","2412090CT1V6X18","2412090BPM0PT4M","2412080A7KFBTSV","24120706UHT41JY","24120706KSUHAJX","24120400KTPJXXF","2412040096BNVMX","2412030SFX1WA4G","2412020RTHQN2FY","2412020QY2VRTUU","2412020QFFXBCXK","2412020QBF2MHFU","2411300KKYVGGT2","2411300KKASB1A8","2411300JXYCVGVP","2411300JXRS60VJ","2411290GSW5HJ2W","2411290G5BU8RF6","2411290F4DB9WS0","2411280DQMGNEJM","24112709T3E0NSB","24112608YDCFFW9","24112506R9SRHCQ","24112506QNXMHV8","241125062SGPG7N","24112504W7D83RQ","24112504R91F1QF","24112403QP1Q08W","24112301XDPVH1A","24112301WR79X2N","24112301K8XEG16","24112301CXMX5KP","24112300GNQKQYE","2411220VN362FA0","2411220V8DJGXTY","2411220UKNMJSR1","2411220UDG6EJDH","2411220UC01C8M0","2411220UCFSTKS5","2411220UBTF1GDN","2411220U3JP17EN","2411220TAK5UC9R","2411210SBBGR4C0","2411210QU727S7V","2411210QU26R56Q","2411200QK9BKC9V","2411200QF5HG38J","2411200QAKQ4J9C","2411200Q99X4TY1","2411200NC1BPFDN","2411190N5K0EVUC","2411190N3FK8W6D","2411190N28WCK08","2411190N18SBP6U","2411190MWQP4PJH","2411190MFBQ5Q3W","2411180HBX8GBJN","2411170EQUD84P8","2411160DARRR9XN","2411160CQ76639H","2411160C8GV7SUB","24111509XRH5AJG","24111408FQS88D6","24111407X828J3B","24111407Q2F4C6T","241114079U82C6M","241113052GUSWJC","24111304EGJ5JVE","24111203D70EY4R","241112037FY0VP9","2411120354M45CE","24111202YNVRFDJ","24111202U320G1V","24111202TC2QWDW","24111201BX892EX","241111012J1VHVP","24111100UBFDFMB","2411110021APEQB","2411100TBVQ91R1","2411080P7JSM7WE","2411060GWJJ1WU3","2411060FANTU1H5","2411050F5B41MT9","2411040AXYHJCU8","24110309RGPU8J7","24110309CDCV86V","24110104PM8CWUU","24110104P5N20UK","24110104G6TPPGF","241031015UHYCPE","2410290TMP5QCVC","2410290RG0U7QCG","2410270MJJXM4QH","2410270MDQSUV47","2410260JXG1RHRS","2410260HSUVT07H","2410250FFM0VUPJ","2410250F7TMHGDX","2410240D00TCDM5","2410230B7HMGD6M","2410230A6UCU3S4","24102208Y1AA8RE","241021068FPF81E","24102105C25A9JU","241021059HHK68B","24102001X8TJJ4U","24102001K4Q3GXN","2410190171SH1AT","24101900M8YFHNG","24101900CHXEW2G","2410180US1066EU","2410180UCC6F4VU"]
        self.test_shoppee_return_order(platformId=34,platform_rma_code_list=platform_rma_code_list)
