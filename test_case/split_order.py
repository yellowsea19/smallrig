import unittest
import datetime,time,random
import requests
import json
import concurrent.futures
import importlib,sys
import pymysql
importlib.reload(sys)


import logging #导入日志模块
log = logging.getLogger() #创建日志器
log.setLevel(logging.INFO) #设置日志的打印级别
# fh = logging.FileHandler(filename="../logs/log.log",mode='a',encoding="utf-8") #创建日志处理器，用文件存放日志
sh = logging.StreamHandler()#创建日志处理器，在控制台打印
#创建格式器，指定日志的打印格式
fmt = logging.Formatter("[%(asctime)s]-[%(levelname)s]-[%(filename)s]-[Line:%(lineno)d]-[Msg:%(message)s]")
fmt = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
#给处理器设置格式
# fh.setFormatter(fmt=fmt)
sh.setFormatter(fmt=fmt)
#给日志器添加处理器
# logg.addHandler(fh)
log.addHandler(sh)



class Order(unittest.TestCase):




    def setUp(self,env='uat'):
        log.info('start {}'.format(self))
        log.info(f"当前执行环境： {env}")
        self.env = env
        if self.env == 'test':
            self.urls = 'http://192.168.133.223:5555'
            self.xxl_url = 'http://192.168.133.223:19010'
            self.connection = pymysql.connect(host='192.168.133.213',  # 数据库地址
                                              user='root',  # 数据库用户名
                                              password='root',  # 数据库密码
                                              db='smallrig-platform')  # 数据库名称
            self.cursor = self.connection.cursor()
        elif self.env == 'uat':
            self.urls = 'https://bereal.smallrig.net'
            self.xxl_url = 'http://192.168.133.232:19010'
            self.connection = pymysql.connect(host='192.168.133.233',  # 数据库地址
                                              user='root',  # 数据库用户名
                                              password='Leqi!2022',  # 数据库密码
                                              db='smallrig-platform')  # 数据库名称
            self.cursor = self.connection.cursor()

    def tearDown(self):
        self.cursor.close()
        self.connection.close()

    def query(self, sql):
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        # 获取字段名
        columns = [desc[0] for desc in self.cursor.description]
        result = []
        for row in rows:
            row_dict = dict(zip(columns, row))
            result.append(row_dict)
        return result


    def test_order_base(self,order_code='SO24092600019',split_order_code=('SO24092500003','SO24092500004')):
        """
        :param order_code: 需要拆单的订单号
        :param split_order_code: 拆单后的订单号，传list
        :return:
        """
        sql =  f"select * from t_order_base where order_code='{order_code}' and del_flag=1"
        results = self.query(sql)
        split_sql = f"select * from t_order_base where order_code in {split_order_code} and del_flag=1"
        # print(split_sql)
        split_resuts = self.query(split_sql)
        for i in results:
            log.debug(i)
            product_variety_num = 0
            product_total_num = 0
            total_weight = 0
            shipping_weight = 0
            for j in split_resuts:
                product_variety_num =product_variety_num + j['product_variety_num']
                product_total_num =product_total_num + j['product_total_num']

                total_weight =total_weight + j['total_weight']
                shipping_weight =shipping_weight + j['shipping_weight']
                log.debug(j)
                if j['order_type'] != i['order_type']:
                    pass
                if j['order_attribute'] != i['order_attribute']:
                    print("order_type 不相等")
                if j['own_order_status'] != i['own_order_status']:
                    print("own_order_status 不相等")
                if j['sales_record_num'] != i['sales_record_num']:
                    print("sales_record_num 不相等")
                if j['tracking_number'] != i['tracking_number']:
                    print("sales_record_num 不相等")
                if j['paypal'] != i['paypal']:
                    print("paypal 不相等")
                if j['transport'] != i['transport']:
                    print("transport 不相等")
                if j['express_type'] != i['express_type']:
                    print("express_type 不相等")
                if j['service_remark'] != i['service_remark']:
                    print("service_remark 不相等")
                if j['logistics_status'] != i['logistics_status']:
                    print("logistics_status 不相等")
                # if j['audit_opinion'] != i['audit_opinion']:
                #     print("audit_opinion 不相等")
                if j['audit_person'] != i['audit_person']:
                    print("audit_person 不相等")
                if j['audit_remark'] != i['audit_remark']:
                    print("audit_remark 不相等")
                if j['source'] != i['source']:
                    print("source 不相等")
                if j['api_status'] != i['api_status']:
                    print("api_status 不相等")
                if j['send_type'] != i['send_type']:
                    print("send_type 不相等")
                if j['is_sub_inventory'] != i['is_sub_inventory']:
                    print("is_sub_inventory 不相等")
                if j['is_tag_ship'] != i['is_tag_ship']:
                    print("is_tag_ship 不相等")
                if j['is_wait'] != i['is_wait']:
                    print("is_wait 需要手动确认是否锁单，若拆单的时候是锁单，则状态为2，当前状态为：%s"%j['is_wait'])
                if j['is_audit_unLock'] != i['is_audit_unLock']:
                    print("is_audit_unLock 不相等")
                if j['is_eccang_audit'] != i['is_eccang_audit']:
                    print("is_eccang_audit 不相等")
                if j['wait_status'] != i['wait_status']:
                    print("wait_status 不相等")
                if j['yc_warehouse_order_code'] != i['yc_warehouse_order_code']:
                    print("yc_warehouse_order_code 不相等")
                if j['auto_audit_match'] != i['auto_audit_match']:
                    print("auto_audit_match 不相等")
                if j['sync_platform_status'] != i['sync_platform_status']:
                    print("sync_platform_status 不相等")


            # if int(product_variety_num) != int(i['product_variety_num']):
            #     print("product_variety_num 不相等",j['product_variety_num'] ,i['product_variety_num'])
            if product_total_num != i['product_total_num']:
                print("product_total_num 不相等",j['product_total_num'] ,i['product_total_num'])
            if total_weight != i['total_weight']:
                print("total_weight 不相等",j['total_weight'] ,i['total_weight'])
            if shipping_weight != i['shipping_weight']:
                print("shipping_weight 不相等",j['shipping_weight'] ,i['shipping_weight'])


    def test_order_item(self,order_code='SO24092504790',split_order_code=('SO24092505146','SO24092505147')):
        """
        :param order_code: 需要拆单的订单号
        :param split_order_code: 拆单后的订单号，传list
        :return:
        """
        sql =  f"select * from t_order_item where base_id in  (select id from t_order_base where order_code='{order_code}') and del_flag = 1"
        results = self.query(sql)
        split_sql = f"select * from t_order_item where base_id in  (select id from t_order_base where order_code in {split_order_code}) and del_flag = 1"
        split_resuts = self.query(split_sql)

        for i in results:
            log.debug(i)
            product_quantity = 0
            total_fee = 0
            real_product_quantity = 0
            shipping_price = 0
            order_quantity = 0
            for j in split_resuts:
                if j['external_sku'] == i['external_sku']:
                    log.debug(j)
                    product_quantity = product_quantity + j['product_quantity']
                    total_fee = total_fee + j['total_fee']
                    real_product_quantity = real_product_quantity + j['real_product_quantity']
                    shipping_price = shipping_price + j['shipping_price']
                    order_quantity = order_quantity + j['order_quantity']
            if product_quantity != i['product_quantity']:
                print("product_quantity 不相等",j['product_quantity'] ,i['product_quantity'])
            if total_fee != i['total_fee']:
                print("total_fee 不相等",j['total_fee'] ,i['total_fee'])
            if int(real_product_quantity) != int(i['real_product_quantity']):
                print("real_product_quantity 不相等",j['real_product_quantity'] ,i['real_product_quantity'])
            if shipping_price != i['shipping_price']:
                print("shipping_price 不相等",j['shipping_price'] ,i['shipping_price'])
            if order_quantity != i['order_quantity']:
                print("order_quantity 不相等",j['order_quantity'] ,i['order_quantity'])


    def test_order_sys_item(self,order_code='SO24092504790',split_order_code=('SO24092505146','SO24092505147')):

        """
        :param order_code: 需要拆单的订单号
        :param split_order_code: 拆单后的订单号，传list
        :return:
        """
        sql = f"select * from t_order_sys_item where base_id in  (select id from t_order_base where order_code='{order_code}') and del_flag = 1"
        results = self.query(sql)
        split_sql = f"select * from t_order_sys_item where base_id in  (select id from t_order_base where order_code in {split_order_code}) and del_flag = 1"
        split_resuts = self.query(split_sql)

        for i in results:
            log.debug(i)
            product_quantity = 0
            matched_quantity = 0
            real_product_quantity = 0
            total_fee = 0
            total_weight = 0
            original_total_fee = 0

            for j in split_resuts:
                if j['external_sku'] == i['external_sku'] and j['product_code'] == i['product_code']:
                    log.info(i['external_sku'])
                    log.debug(j)
                    product_quantity = product_quantity + j['product_quantity']
                    matched_quantity = matched_quantity + j['matched_quantity']
                    real_product_quantity = real_product_quantity + j['real_product_quantity']
                    total_fee = total_fee + j['total_fee']
                    total_weight = total_weight + j['total_weight']
                    original_total_fee = original_total_fee + j['original_total_fee']

            if product_quantity != i['product_quantity']:
                print("product_quantity 不相等", j['product_quantity'], i['product_quantity'])
            if matched_quantity != i['matched_quantity']:
                print("matched_quantity 不相等", j['matched_quantity'], i['matched_quantity'])
            if real_product_quantity != i['real_product_quantity']:
                print("real_product_quantity 不相等", j['real_product_quantity'], i['real_product_quantity'])
            # if scale != i['scale']:
            #     print("scale 不相等", j['scale'], i['scale'])

            if total_fee != i['total_fee']:
                print("total_fee 不相等", j['total_fee'], i['total_fee'])
            if total_weight != i['total_weight']:
                print("total_weight 不相等", j['total_weight'], i['total_weight'])
            if original_total_fee != i['original_total_fee']:
                print("original_total_fee 不相等", j['original_total_fee'], i['original_total_fee'])


    def test_order_item_cost(self,order_code='SO24092600032',split_order_code=('SO24092600010','SO24092600011')):
        """
        :param order_code: 需要拆单的订单号
        :param split_order_code: 拆单后的订单号
        :return:
        """
        sql = f"select * from t_order_item_cost where base_id in  (select id from t_order_base where order_code='{order_code}') and del_flag = 1"
        results = self.query(sql)
        split_sql = f"select * from t_order_item_cost where base_id in  (select id from t_order_base where order_code in {split_order_code}) and del_flag = 1"
        split_resuts = self.query(split_sql)
        for i in results:
            log.debug("原单：",i)
            product_quantity = 0
            coupon_fee = 0
            platform_coupon = 0
            other_income = 0
            shipping_fee = 0
            product_tax = 0
            shipping_tax = 0
            other_tax = 0
            if i['platform_coupon'] == None:
                i['platform_coupon'] = 0
            if i['other_income'] == None:
                i['other_income'] = 0
            if i['shipping_fee'] == None:
                i['shipping_fee'] = 0
            if i['shipping_tax'] == None:
                i['shipping_tax'] = 0
            if i['other_tax'] == None:
                i['other_tax'] = 0
            if i['product_tax'] == None:
                i['product_tax'] = 0

            for j in split_resuts:
                if j['external_sku'] == i['external_sku']:
                    log.debug("拆单",j)
                    product_quantity = product_quantity + j['product_quantity']
                    coupon_fee = coupon_fee + j['coupon_fee']
                    if j['platform_coupon'] == None:
                        j['platform_coupon'] = 0
                    platform_coupon = platform_coupon + j['platform_coupon']
                    if j['other_income'] == None:
                        j['other_income'] = 0
                    other_income = other_income + j['other_income']
                    if j['shipping_fee'] == None:
                        j['shipping_fee'] = 0
                    shipping_fee = shipping_fee + j['shipping_fee']
                    if j['product_tax'] == None:
                        j['product_tax'] = 0
                    product_tax = product_tax + j['product_tax']
                    if j['shipping_tax'] == None:
                        j['shipping_tax'] = 0
                    shipping_tax = shipping_tax + j['shipping_tax']
                    if j['other_tax'] == None:
                        j['other_tax'] = 0
                    if j['product_tax'] == None:
                        j['product_tax'] = 0
                    other_tax = other_tax + j['other_tax']
            if product_quantity != i['product_quantity']:
                print("product_quantity 不相等", j['product_quantity'], i['product_quantity'])
            if coupon_fee != i['coupon_fee']:
                print("coupon_fee 不相等", j['coupon_fee'], i['coupon_fee'])
            if platform_coupon != i['platform_coupon']:
                print("platform_coupon 不相等", j['platform_coupon'], i['platform_coupon'])
            if other_income != i['other_income']:
                print("other_income 不相等", j['other_income'], i['other_income'])
            if shipping_fee != i['shipping_fee']:
                print("shipping_fee 不相等", j['shipping_fee'], i['shipping_fee'])
            if product_tax != i['product_tax']:
                print("product_tax 1不相等", j['product_tax'], i['product_tax'])
            if shipping_tax != i['shipping_tax']:
                print("shipping_tax 不相等", j['shipping_tax'], i['shipping_tax'])
            if other_tax != i['other_tax']:
                print("other_tax 不相等", j['other_tax'], i['other_tax'])


    def test_order_cost(self,order_code='SO24102600039',split_order_code=('SO24102607401','SO24110800764')):
        """
        :param order_code: 需要拆单的订单号
        :param split_order_code: 拆单后的订单号
        :return:
        """
        sql = f"select * from t_order_cost where base_id in  (select id from t_order_base where order_code='{order_code}') and del_flag = 1"
        results = self.query(sql)
        split_sql = f"select * from t_order_cost where base_id in  (select id from t_order_base where order_code in {split_order_code}) and del_flag = 1"
        split_resuts = self.query(split_sql)
        for i in results:
            log.debug("原单：",i)
            total_fee = 0
            cny_total_fee = 0
            platform_fee = 0
            shipping_fee = 0
            actual_shipping_cost = 0
            product_total = 0
            coupon_fee = 0
            audit_fee = 0
            discount_total = 0
            other_income = 0
            platform_coupon = 0
            market_income = 0
            product_tax = 0
            shipping_tax = 0
            other_tax = 0
            warehouse_fee = 0
            other_fee = 0
            use_balance = 0
            source_market_income = i['market_income']
            order_market_income = i['product_total']+i['shipping_fee'] +i['other_income'] - i['coupon_fee']
            if source_market_income != order_market_income :
                print("base_id %s : 成交额为：%s ,用 成交额=产品总金额+运费（买家支付）+其它收入- 店铺优惠  计算为 ： %s"%(i['base_id'],source_market_income,order_market_income))

            for j in split_resuts:

                log.debug("拆单",j)
                total_fee = total_fee + j['total_fee']
                cny_total_fee = cny_total_fee + j['cny_total_fee']
                platform_fee = platform_fee + j['platform_fee']
                shipping_fee = shipping_fee + j['shipping_fee']
                actual_shipping_cost = actual_shipping_cost + j['actual_shipping_cost']
                product_total = product_total + j['product_total']
                coupon_fee = coupon_fee + j['coupon_fee']
                audit_fee = audit_fee + j['audit_fee']
                discount_total = discount_total + j['discount_total']
                other_income = other_income + j['other_income']
                platform_coupon = platform_coupon + j['platform_coupon']
                market_income = market_income + j['market_income']
                if j['product_tax'] == None:
                    j['product_tax'] = 0
                product_tax = product_tax + j['product_tax']
                shipping_tax = shipping_tax + j['shipping_tax']
                other_tax = other_tax + j['other_tax']
                warehouse_fee = warehouse_fee + j['warehouse_fee']
                other_fee = other_fee + j['other_fee']
                use_balance = use_balance + j['use_balance']

            if total_fee != i['total_fee']:
                print("total_fee 不相等,拆单后：", total_fee,'原单：', i['total_fee'])
            if cny_total_fee != i['cny_total_fee']:
                print("cny_total_fee 不相等,拆单后：", cny_total_fee,'原单：', i['cny_total_fee'])
            if platform_fee != i['platform_fee']:
                print("platform_fee 不相等,拆单后：", platform_fee,'原单：', i['platform_fee'])
            if shipping_fee != i['shipping_fee']:
                print("shipping_fee 不相等,拆单后：", shipping_fee,'原单：', i['shipping_fee'])
            if product_total != i['product_total']:
                print("product_total 不相等,拆单后：", product_total,'原单：', i['product_total'])
            if coupon_fee != i['coupon_fee']:
                print("coupon_fee 不相等,拆单后：", coupon_fee,'原单：', i['coupon_fee'])
            if audit_fee != i['audit_fee']:
                print("audit_fee 不相等,拆单后：", audit_fee,'原单：', i['audit_fee'])
            if discount_total != i['discount_total']:
                print("discount_total 不相等,拆单后：", discount_total,'原单：', i['discount_total'])
            if discount_total != i['discount_total']:
                print("other_income 不相等,拆单后：", discount_total,'原单：', i['other_income'])
            if platform_coupon != i['platform_coupon']:
                print("platform_coupon 不相等,拆单后：", platform_coupon,'原单：', i['platform_coupon'])
            if market_income != i['market_income']:
                print("market_income 不相等,拆单后：", market_income,'原单：', i['market_income'])
            if product_tax != i['product_tax']:
                print("product_tax 不相等,拆单后：", product_tax,'原单：', i['product_tax'])
            if shipping_tax != i['shipping_tax']:
                print("shipping_tax 不相等,拆单后：", shipping_tax,'原单：', i['shipping_tax'])
            if other_tax != i['other_tax']:
                print("other_tax 不相等,拆单后：", other_tax,'原单：', i['other_tax'])
            if warehouse_fee != i['warehouse_fee']:
                print("warehouse_fee 不相等,拆单后：", warehouse_fee,'原单：', i['warehouse_fee'])
            if other_fee != i['other_fee']:
                print("other_fee 不相等,拆单后：", other_fee,'原单：', i['other_fee'])
            if use_balance != i['use_balance']:
                print("use_balance 不相等,拆单后：", use_balance,'原单：', i['use_balance'])

            source_split_market_income = j['market_income']
            order_split_market_income = j['product_total'] + j['shipping_fee'] + j['other_income'] - j['coupon_fee']
            if source_split_market_income != order_split_market_income:
                print("base_id %s : 成交额为：%s ,用 成交额=产品总金额+运费（买家支付）+其它收入- 店铺优惠  计算为 ： %s" % (
                j['base_id'], source_split_market_income, order_split_market_income))



    def test_1016(self,order_code='SO24112802202',split_order_code=('SO24112802208','SO24112802209','SO24112802210')):
        log.info('t_order_base')
        self.test_order_base(order_code=order_code,split_order_code=split_order_code)
        log.info('t_order_item')
        self.test_order_item(order_code=order_code,split_order_code=split_order_code)
        log.info('t_order_sys_item')
        self.test_order_sys_item(order_code=order_code,split_order_code=split_order_code)
        log.info('t_order_item_cost')
        self.test_order_item_cost(order_code=order_code,split_order_code=split_order_code)
        log.info('t_order_cost')
        self.test_order_cost(order_code=order_code,split_order_code=split_order_code)








