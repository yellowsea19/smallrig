import unittest,requests,json
import pymysql
import time

class DatabaseOperations(unittest.TestCase):

    def setUp(self):
        self.connection = pymysql.connect(host='192.168.133.213',  # 数据库地址
                                          user='root',  # 数据库用户名
                                          password='root',  # 数据库密码
                                          db='smallrig-platform')  # 数据库名称
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

    def tearDown(self):
        self.cursor.close()
        self.connection.close()

    def login(self):
        url = 'http://192.168.133.223:8888/API/manage/login'
        data = {"systemCode":"XTZX_MAIN","username":"huanghai","password":"17f711ffa7869410fbb8edfcb5f08167","_t":1695865848822}
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,sq;q=0.7,ar;q=0.6,an;q=0.5',
            'Access-Token': 'eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5naGFpIiwidXNlcklkIjoiNTM2Iiwibmlja05hbWUiOiLpu4TmtbciLCJ0aW1lc3RhbXAiOjE2OTU2MDgyNzUwOTV9.eL8oSpqZ7KKJiW76Qif5UXoTZENfzpjYut39RKm3YqM',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Cookie': 'XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d; _SIGN_ON_token=%22eyJhb2ciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5naGFpIiwidXNlcklkIjoiNTM2Iiwibmlja05hbWUiOiLpu4TmtbciLCJ0aW1lc3RhbXAiOjE2OTU2MDgyNzUwOTV9.eL8oSpqZ7KKJiW76Qif5UXoTZENfzpjYut39RKm3YqM%22; _SIGN_ON_userId=%22536%22; _SIGN_ON_userName=%22%E9%BB%84%E6%B5%B7%22; NG_TRANSLATE_LANG_KEY=%22en%22',
            'Origin': 'http://192.168.133.223:5555',
            'Referer': 'http://192.168.133.223:5555/YWZT/inventory/headWay/index',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'User-Id': '536',
            'system-code': 'ERP'
        }
        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
        res = response.json()
        return res['data']['accessToken']


    def query_toucheng(self,no='HS23091900002'):
        url = 'http://192.168.133.223:5555/API/srm/head_deliver_goods/v1/list'

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,sq;q=0.7,ar;q=0.6,an;q=0.5',
            'Access-Token': self.login(),
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Cookie': 'XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d; _SIGN_ON_token=%22eyJhb2ciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5naGFpIiwidXNlcklkIjoiNTM2Iiwibmlja05hbWUiOiLpu4TmtbciLCJ0aW1lc3RhbXAiOjE2OTU2MDgyNzUwOTV9.eL8oSpqZ7KKJiW76Qif5UXoTZENfzpjYut39RKm3YqM%22; _SIGN_ON_userId=%22536%22; _SIGN_ON_userName=%22%E9%BB%84%E6%B5%B7%22; NG_TRANSLATE_LANG_KEY=%22en%22',
            'Origin': 'http://192.168.133.223:5555',
            'Referer': 'http://192.168.133.223:5555/YWZT/inventory/headWay/index',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'User-Id': '536',
            'system-code': 'ERP'
        }

        data = {
            'pageSize': 15,
            'pageNum': 1,
            'orderType': 1,
            'no': '%s'%no,
            'timeType': 1,
            'timestamp': 1695610311000
        }

        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
        res =  response.json()
        # print(res)
        print(res['data']['items'][0]['receiveWarehouseId'])
        return res['data']['items'][0]['receiveWarehouseId']

    def query_zhongzhuan(self,transferCode):
        url = 'http://192.168.133.223:5555/API/srm/transferManage/v1/getList'

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,sq;q=0.7,ar;q=0.6,an;q=0.5',
            'Access-Token': self.login(),
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Cookie': 'XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d; NG_TRANSLATE_LANG_KEY=%22en%22; _SIGN_ON_token=%22eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5naGFpIiwidXNlcklkIjoiNTM2Iiwibmlja05hbWUiOiLpu4TmtbciLCJ0aW1lc3RhbXAiOjE2OTU3MTA0NDYwOTR9.nVP8Mz9PTlyhC3QP9XP64spAFNWr3FySQXeAo1_HYPY%22; _SIGN_ON_userId=%22536%22; _SIGN_ON_userName=%22%E9%BB%84%E6%B5%B7%22',
            'Origin': 'http://192.168.133.223:5555',
            'Referer': 'http://192.168.133.223:5555/YWZT/inventory/transitWarehouse/shippingManage',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'User-Id': '536',
            'system-code': 'ERP'
        }

        data = {
            'pageSize': 15,
            'pageNum': 1,
            'type1': 1,
            'transferCode': transferCode,
            'timestamp': 1695711927000
        }

        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)

        res = response.json()
        # print(res)
        print(res['data']['items'][0]['receiveWarehouseId'])
        return res['data']['items'][0]['receiveWarehouseId']

    def query_diaobo(self,allotNo):
        url = 'http://192.168.133.223:5555/API/srm/allot/v1/list'

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,sq;q=0.7,ar;q=0.6,an;q=0.5',
            'Access-Token': self.login(),
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Cookie': 'XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d; NG_TRANSLATE_LANG_KEY=%22en%22; _SIGN_ON_token=%22eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5naGFpIiwidXNlcklkIjoiNTM2Iiwibmlja05hbWUiOiLpu4TmtbciLCJ0aW1lc3RhbXAiOjE2OTU3MTA0NDYwOTR9.nVP8Mz9PTlyhC3QP9XP64spAFNWr3FySQXeAo1_HYPY%22; _SIGN_ON_userId=%22536%22; _SIGN_ON_userName=%22%E9%BB%84%E6%B5%B7%22',
            'Origin': 'http://192.168.133.223:5555',
            'Referer': 'http://192.168.133.223:5555/YWZT/inventory/partitio/marketProductPartition',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'User-Id': '536',
            'system-code': 'ERP'
        }

        data = {
            'pageSize': 15,
            'pageNum': 1,
            'allotNo': allotNo,

            'timestamp': 1695712507000
        }

        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)

        res = response.json()
        # print(res)
        print(res['data']['items'][0]['inWarehouseId'])
        return res['data']['items'][0]['inWarehouseId']

    def test_liushui(self,sku='1124'):
        #查询汇总出入库流水
        SQL = f"""
        SELECT
        t1.bound_no as boundNo,
        t1.bound_type as boundType,
        t1.source_type as sourceType,
        t1.source_no as sourceNo,
        t1.warehouse_id AS warehouseId,
        t2.product_id AS productId,
        t2.product_code AS productCode,
        t2.product_num AS changeNum,
        t1.inbound_time AS opTime,
        t2.id as boundId
        FROM
        t_out_in_inbound t1,
        t_out_in_inbound_detail t2
        WHERE
        t1.id = t2.bound_id
        AND t1.del_flag = 1
        AND t2.del_flag = 1
        AND t1.inbound_time >= "2023-09-01 00:00:00"
        AND t1.inbound_time <="2023-09-19 23:59:59"
        AND t2.product_code = '1124'
        # AND (t1.source_no = 'HS23091900002' )
        AND (t1.bound_no = 'CR23091903047' or t1.bound_no = 'CR23091903047')
        # AND t2.warehouse_id = 154 
        order BY t1.inbound_time,t1.bound_type
        """
        results = self.query(SQL)
        fields = [i[0] for i in self.cursor.description]
        liushui_list = []
        # 格式化打印结果
        for row in results:
            # 将查询到的行数据与字段名对应，得到一个包含字段名和字段值的字典
            row_with_field = dict(zip(fields, row))
            print(row_with_field)
            tmp ={}
            tmp['boundNo'] = row_with_field['boundNo']
            tmp['boundType'] = row_with_field['boundType']
            tmp['sourceType'] = row_with_field['sourceType']
            tmp['sourceNo'] = row_with_field['sourceNo']
            tmp['warehouseId'] = row_with_field['warehouseId']
            tmp['productId'] = row_with_field['productId']
            tmp['productCode'] = row_with_field['productCode']
            tmp['changeNum'] = row_with_field['changeNum']
            tmp['opTime'] = row_with_field['opTime']
            tmp['boundId'] = row_with_field['boundId']
            liushui_list.append(tmp)

        return liushui_list



    def test_batch_sanpshoot(self,snapshoot_date="20230901"):
        #初始化批次到 t_batch_info_test表
        SQL = f"""
        select * from t_batch_info_snapshoot where   snapshoot_date='{snapshoot_date}'
        """
        # print(SQL)
        results = self.query(SQL)
        fields = [i[0] for i in self.cursor.description]
        tmp=[]
        del_sql="delete from t_batch_info_test"
        self.delete(del_sql)
        # 格式化打印结果
        for row in results:
            row_with_field = dict(zip(fields, row))
            # print(row_with_field)
            SQL="""
                INSERT INTO `t_batch_info_test` ( `batch_type`, `batch_no`, `batch_time`, `product_id`, `product_code`, `warehouse_id`, `cost_price`, `quantity`, `remark`, `del_flag`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES
                 ('{}','{}','{}' ,'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');

                """.format(row_with_field["batch_type"], row_with_field["batch_no"], row_with_field["batch_time"], row_with_field["product_id"], row_with_field["product_code"], row_with_field["warehouse_id"], row_with_field["cost_price"], row_with_field["quantity"], row_with_field["remark"], row_with_field["del_flag"], row_with_field["create_by"], row_with_field["create_time"], row_with_field["update_by"], row_with_field["update_time"])
            print(SQL)
            self.insert(SQL)
            # 将查询到的行数据与字段名对应，得到一个包含字段名和字段值的字典

            # print(row_with_field)
            # print("在库：",row_with_field['product_code'],row_with_field['batch_type'],row_with_field['product_code'],float(row_with_field['cost_price']),row_with_field['quantity'],row_with_field['batch_no'])
            tmp_list = {}
            tmp_list['batch_type'] = row_with_field['batch_type']
            tmp_list['cost_price'] = row_with_field['cost_price']
            tmp_list['quantity'] = row_with_field['quantity']
            tmp_list['batch_no'] = row_with_field['batch_no']
            tmp.append(tmp_list)
            # print(tmp)
        return tmp



    def test_liushui_tmp(self,sku='1124',warehouseId=154):
        """批次校对
        """
        liushui_list = self.test_liushui()
        for liushui in liushui_list :
            print("-----------------------------------------------------------------------------")
            print(liushui)

            #根据流水拿到初始在库和在途数据
            sql_init = """
                            select * from t_batch_info_test where warehouse_id=%s and product_id = %s
                            """%(liushui['warehouseId'],liushui['productId'])
            results = self.query(sql_init)
            fields = [i[0] for i in self.cursor.description]
            pici_list = []
            for row in results:
                row_with_field = dict(zip(fields, row))
                # print(row_with_field)
                pici_list.append(row_with_field)
            # print(pici_list)

            if liushui['boundType'] == 2 and liushui['sourceType'] in (22,23,36):
                print("请调查询头程/中转/调拨")
                if liushui['sourceType'] == 23:
                    receiveWarehouseId = self.query_toucheng(liushui['sourceNo'])
                if liushui['sourceType'] == 22:
                    receiveWarehouseId =self.query_zhongzhuan(transferCode=liushui['sourceNo'])
                if liushui['sourceType'] == 36:
                    receiveWarehouseId =self.query_diaobo(allotNo=liushui['sourceNo'])

                #扣减在库数据
                for tt in pici_list :
                    # print(tt)
                    if tt['quantity'] >0 :

                        if tt['batch_type'] == 1:
                            batch_no = tt['batch_no']

                            if tt['quantity'] - liushui['changeNum'] >=0 :
                                print("在库数量：",tt['quantity'],"流水数量: ",liushui['changeNum'])
                                tt['quantity'] = tt['quantity'] - liushui['changeNum']
                                #更新数据,扣减在库数据
                                update_sql = """
                                            update t_batch_info_test set quantity = quantity - %s  where id=%s
                                            """%(liushui['changeNum'],tt['id'])
                                print("扣减在库：",update_sql)
                                self.update(update_sql)
                                # liushui['changeNum'] = 0

                                #增加在途数据
                                if liushui['sourceType'] in (22,23,36):
                                    #查询在途批次
                                    sql = """
                                        select * from t_batch_info_test where warehouse_id = %s and product_id = %s and batch_type=2
                                        """%(receiveWarehouseId,liushui['productId'])
                                    # print(sql)
                                    result_tmp = self.query(sql)
                                    fields = [i[0] for i in self.cursor.description]
                                    tmp_list = []
                                    for row in result_tmp:
                                        row_with_field = dict(zip(fields, row))
                                        # print(row_with_field)
                                        tmp_list.append(row_with_field)
                                    batch_no_list = []
                                    for t2 in tmp_list :
                                        batch_no_list.append(t2['batch_no'])
                                    if batch_no in batch_no_list:
                                        update_sql = """
                                                    update t_batch_info_test set quantity = quantity+%s  where batch_no='%s' and batch_type = 2 and warehouse_id = %s and product_id = %s
                                                    """%(liushui['changeNum'],batch_no,receiveWarehouseId,liushui['productId'])
                                        print("更新在途数据1 ：",update_sql)

                                        self.update(update_sql)
                                        liushui['changeNum'] = 0
                                    else:

                                        sql = """
                                            INSERT INTO `t_batch_info_test` ( `batch_type`, `batch_no`, `batch_time`, `product_id`, `product_code`, `warehouse_id`, `cost_price`, `quantity`, `remark`, `del_flag`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES
                                                                ('{}','{}','{}' ,'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');
                                                                """.format(2, tt['batch_no'], liushui['opTime'],liushui['productId'],liushui['productCode'],receiveWarehouseId, 0,liushui['changeNum'], "", 1, "hh",liushui['opTime'],"hh",liushui['opTime'])
                                        print("插入在途数据：",sql)
                                        self.update(sql)
                                liushui['changeNum'] = 0


                            if tt['quantity'] - liushui['changeNum'] <0 :
                                print("在库数量：", tt['quantity'], "流水数量: ", liushui['changeNum'])
                                #在库扣减为0
                                update_sql = """
                                            update t_batch_info_test set quantity = 0  where id=%s
                                            """ % ( tt['id'])
                                print("扣减在库数量33：",update_sql)
                                self.update(update_sql)
                                # 查询在途批次
                                sql_zaitu = """
                                    select * from t_batch_info_test where warehouse_id = %s and product_id = %s and  batch_type=2
                                    """ % (receiveWarehouseId, liushui['productId'])
                                result_tmp = self.query(sql_zaitu)
                                fields = [i[0] for i in self.cursor.description]
                                tmp_list = []
                                for row in result_tmp:
                                    row_with_field = dict(zip(fields, row))
                                    # print(row_with_field)
                                    tmp_list.append(row_with_field)
                                batch_no_list = []

                                #增加在途数量
                                if liushui['sourceType'] in (22, 23, 36):
                                    for t2 in tmp_list:
                                        batch_no_list.append(t2['batch_no'])
                                    if batch_no in batch_no_list:
                                        update_sql = """
                                                    update t_batch_info_test set quantity = quantity+%s  where batch_no='%s' and batch_type = 2
                                                    """ % (
                                        tt['quantity'], batch_no)
                                        print("更新在途数据2：",update_sql)
                                        self.update(update_sql)
                                        liushui['changeNum'] =  liushui['changeNum'] - tt['quantity']
                                    else:
                                        sql = """
                                                        INSERT INTO `t_batch_info_test` ( `batch_type`, `batch_no`, `batch_time`, `product_id`, `product_code`, `warehouse_id`, `cost_price`, `quantity`, `remark`, `del_flag`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES
                                                        ('{}','{}','{}' ,'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');
                                                        """.format(2, tt['batch_no'], liushui['opTime'], liushui['productId'], liushui['productCode'], receiveWarehouseId, 0, liushui['changeNum'], "", 1, "hh", liushui['opTime'], "hh", liushui['opTime'])
                                        print("插入在途数据",sql)
                                        self.update(sql)
                                liushui['changeNum'] = liushui['changeNum'] -tt['quantity']
            elif liushui['boundType'] == 2:

                for tt in pici_list:
                    # print(tt)
                    if tt['quantity'] > 0:

                        if tt['batch_type'] == 1:
                            batch_no = tt['batch_no']

                            if tt['quantity'] - liushui['changeNum'] >= 0:
                                print("在库数量：", tt['quantity'], "流水数量: ", liushui['changeNum'])
                                tt['quantity'] = tt['quantity'] - liushui['changeNum']
                                # 更新数据,扣减在库数据
                                update_sql = """
                                            update t_batch_info_test set quantity = quantity - %s  where id=%s
                                            """ % (liushui['changeNum'], tt['id'])
                                print("扣减在库：", update_sql)
                                self.update(update_sql)
                            if tt['quantity'] - liushui['changeNum'] < 0:
                                print("在库数量：", tt['quantity'], "流水数量: ", liushui['changeNum'])
                                # 在库扣减为0
                                update_sql = """
                                            update t_batch_info_test set quantity = 0  where id=%s
                                            """ % (tt['id'])
                                print("扣减在库数量44：", update_sql)
                                self.update(update_sql)
                                liushui['changeNum'] = liushui['changeNum'] - tt['quantity']


            #在库入
            if liushui['boundType'] == 1 :
                print('在库入')
                #在途出
                # 查询在途总数
                sql_zaitu_sum = """
                                                            select sum(quantity) from t_batch_info_test where warehouse_id = %s and product_id = %s and  batch_type=2 order by batch_time
                                                            """ % (liushui['warehouseId'], liushui['productId'])
                result_sum = self.query(sql_zaitu_sum)[0][0]
                print("在途总数：", result_sum)
                #查询在途数据
                sql_zaitu = """
                            select * from t_batch_info_test where warehouse_id = %s and product_id = %s and  batch_type=2 order by batch_time
                            """ % (liushui['warehouseId'], liushui['productId'])


                print(sql_zaitu)
                result_tmp = self.query(sql_zaitu)


                fields = [i[0] for i in self.cursor.description]
                tmp_list1 = []
                for row in result_tmp:
                    row_with_field = dict(zip(fields, row))
                    # print(row_with_field)
                    tmp_list1.append(row_with_field)
                print(tmp_list1)

                if tmp_list1 != []:


                    for tt in tmp_list1:

                        print("数据库流水：",tt)
                        #如果拿到的在途数据大于流水日志，则直接扣减
                        if tt['quantity'] >= liushui['changeNum']  and liushui['changeNum'] !=0 :
                            print("拿到的在途数据大于流水日志，直接扣减")
                            #在途转出
                            batch_no = tt['batch_no']
                            # 扣减在库数量
                            update_sql = """
                                        update t_batch_info_test set quantity = quantity-%s  where batch_no='%s' and batch_type = 2 and warehouse_id = %s and product_id = %s 
                                        """ % (liushui['changeNum'], batch_no, liushui['warehouseId'], liushui['productId'])
                            print("扣减在途数量", update_sql)
                            self.update(update_sql)
                            #查询在库批次
                            sql_zaiku = """
                                        select batch_no from t_batch_info_test where warehouse_id = %s and product_id = %s and  batch_type=1
                                        """ % (liushui['warehouseId'], liushui['productId'])
                            result =  self.query(sql_zaiku)
                            print(result)
                            tmp_list = []
                            for ttt in result:
                                tmp_list.append(ttt[0])
                            if batch_no in tmp_list:
                                update_sql = """
                                            update t_batch_info_test set quantity = quantity+%s  where batch_no='%s' and batch_type = 1  and warehouse_id = %s and product_id = %s
                                            """ % (liushui['changeNum'], batch_no,liushui['warehouseId'], liushui['productId'])
                                print("在途批次中，与在库批次中存在一样，数量加入在库批次",update_sql)
                                self.update(update_sql)

                            else:
                                sql = """
                                    INSERT INTO `t_batch_info_test` ( `batch_type`, `batch_no`, `batch_time`, `product_id`, `product_code`, `warehouse_id`, `cost_price`, `quantity`, `remark`, `del_flag`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES
                                    ('{}','{}','{}' ,'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');
                                    """.format(1, tt['batch_no'], liushui['opTime'], liushui['productId'],liushui['productCode'], liushui['warehouseId'], 0, liushui['changeNum'], "",1, "hh", liushui['opTime'], "hh", liushui['opTime'])
                                print("增加在库数量 ：",sql)
                                self.insert(sql)

                            liushui['changeNum'] = 0

                        elif tt['quantity'] < liushui['changeNum']  and liushui['changeNum'] !=0 and tt['quantity'] >0:

                            # 扣减在途数量
                            batch_no = tt['batch_no']
                            update_sql = """
                                        update t_batch_info_test set quantity = 0 where batch_no='%s' and batch_type = 2 and warehouse_id = %s and product_id = %s
                                        """ % (batch_no, liushui['warehouseId'], liushui['productId'])
                            print("扣减在途数量", update_sql)
                            self.update(update_sql)

                            # 查询在库批次
                            sql_zaiku = """
                                        select batch_no from t_batch_info_test where warehouse_id = %s and product_id = %s and  batch_type=1
                                        """ % (liushui['warehouseId'], liushui['productId'])
                            result = self.query(sql_zaiku)
                            print(result)
                            tmp_list = []
                            for ttt in result:
                                tmp_list.append(ttt[0])
                            if batch_no in tmp_list:
                                update_sql = """
                                            update t_batch_info_test set quantity = quantity+%s  where batch_no='%s' and batch_type = 1 and warehouse_id = %s and product_id = %s
                                            """ % (tt['quantity'], batch_no,liushui['warehouseId'],liushui['productId'])
                                print("在途批次中，与在库批次中存在一样，数量加入在库批次", update_sql)
                                self.update(update_sql)

                            else:
                                sql = """
                                    INSERT INTO `t_batch_info_test` ( `batch_type`, `batch_no`, `batch_time`, `product_id`, `product_code`, `warehouse_id`, `cost_price`, `quantity`, `remark`, `del_flag`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES
                                    ('{}','{}','{}' ,'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');
                                    """.format(1, tt['batch_no'], liushui['opTime'],liushui['productId'], liushui['productCode'],liushui['warehouseId'], 0,tt['quantity'], "", 1, "hh",liushui['opTime'], "hh", liushui['opTime'])
                                print("增加在库数量 ：", sql)
                                self.insert(sql)

                            liushui['changeNum'] = liushui['changeNum'] - tt['quantity']

                    else:
                        if liushui['changeNum'] != 0:
                            sql = """
                                INSERT INTO `t_batch_info_test` ( `batch_type`, `batch_no`, `batch_time`, `product_id`, `product_code`, `warehouse_id`, `cost_price`, `quantity`, `remark`, `del_flag`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES
                                ('{}','{}','{}' ,'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');
                                """.format(1, time.time(), liushui['opTime'],
                                           liushui['productId'], liushui['productCode'],
                                           liushui['warehouseId'], 0, liushui['changeNum'], "", 1,
                                           "hh", liushui['opTime'], "hh", liushui['opTime'])
                            print("增加在库数量6 ：", sql)
                            self.insert(sql)




















            #
            # #在库--->出
            # elif liushui['boundType'] == 2 and liushui['sourceType'] != 23:
            #     sql = """
            #                 select * from t_batch_info_test where warehouse_id=%s and product_id = %s and batch_type=1 order by create_time
            #                 """%(liushui['warehouseId'],liushui['productId'])
            #     results = self.query(sql)
            #     fields = [i[0] for i in self.cursor.description]
            #     pici_list=[]
            #     for row in results:
            #         row_with_field = dict(zip(fields, row))
            #         pici_list.append(row_with_field)
            #     print(pici_list)
            #     #从pici_list循环找出>0的数进行扣减
            #     for tt in pici_list:
            #
            #         while liushui['changeNum'] > 0:
            #
            #                 if tt['quantity'] - liushui['changeNum'] >=0 :
            #                     tt['quantity'] = tt['quantity'] - liushui['changeNum']
            #                     #更新数据
            #                     update_sql = """
            #                                 update t_batch_info_test set quantity = 0  where id=%s
            #                                 """%tt['id']
            #                     self.update(update_sql)
            #                     liushui['changeNum'] = 0
            #
            #                 if tt['quantity'] - liushui['changeNum'] <0 :
            #                     # liushui['changeNum'] = i['changeNum'] -tt['quantity']
            #                     update_sql = """
            #                                                                 update t_batch_info_test set quantity = 0  where id = %s
            #                                                                 """%tt['id']
            #                     self.update(update_sql)
            #                     liushui['changeNum'] = liushui['changeNum'] -tt['quantity']
            #                     # tt['quantity'] = 0
            # #在库--->入
            # if  liushui['boundType'] == 1 :
            #
            #     #扣减在途
            #     sql = """
            #                select * from t_batch_info where   warehouse_id=%s and product_id = %s and batch_type=2
            #                """%(liushui['warehouseId'],liushui['productId'])
            #     results = self.query(sql)
            #     fields = [i[0] for i in self.cursor.description]
            #     pici_list = []
            #     for row in results:
            #         row_with_field = dict(zip(fields, row))
            #         pici_list.append(row_with_field)
            #     for tt in pici_list:
            #         while liushui['changeNum'] > 0:
            #             if tt['quantity'] - liushui['changeNum'] >= 0:
            #                 tt['quantity'] = tt['quantity'] - liushui['changeNum']
            #                 #更新数据
            #                 update_sql = """
            #                              update t_batch_info_test set quantity = quantity-%s  where id=%s
            #                              """ % (liushui['changeNum'],tt['id'])
            #             #扣减在途数
            #             self.update(update_sql)
            #             liushui['changeNum'] = 0
            #
            #             #增加在库数
            #             # 判断批次是否一致，一致就加入相对应批次
            #             #查询在库批次
            #             sql = """
            #                select * from t_batch_info where   warehouse_id=%s and product_id = %s and batch_type=1
            #                """ % (liushui['warehouseId'], liushui['productId'])
            #             results = self.query(sql)
            #             fields = [i[0] for i in self.cursor.description]
            #             pici_list_tmp = []
            #             for row in results:
            #                 row_with_field = dict(zip(fields, row))
            #                 pici_list.append(row_with_field)
            #             batch_no_list = []
            #             for kk in pici_list_tmp:
            #                 batch_no_list.append(kk['batch_no'])
            #             if  tt['batch_no']  in batch_no_list:
            #                 sql = """
            #                 update t_batch_info_test set quantity = quantity+%s  where batch_no=%s
            #                 """%(liushui['changeNum'],tt['batch_no'])
            #                 self.update(sql)
            #             else:
            #                 inser_sql = """
            #                             INSERT INTO `t_batch_info_test` ( `batch_type`, `batch_no`, `batch_time`, `product_id`, `product_code`, `warehouse_id`, `cost_price`, `quantity`, `remark`, `del_flag`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES
            #                             ('{}','{}','{}' ,'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');
            #                             """.format(1,time.time(),liushui['create_time'],liushui['product_id'],liushui['product_code'],liushui['warehouse_id'],"",liushui['change_num'],"",1,"hh",liushui['create_time'],liushui['create_time'])
            #                 self.insert(inser_sql)
















        #根据流水拿到对应的SKU 仓库+SKU  初始值
        # init_num =

        # for i in liushui :
        #     print("流水：",i)
        #     if int(i['boundType']) == 1:
        #         in_init.append(i['changeNum'])
        #     elif int(i['boundType']) == 2:
        #         while i['changeNum'] > 0 :
        #             for j in in_init:
        #                 if j - i['changeNum'] >=0 :
        #                     in_init[in_init.index(j)] = j - i['changeNum']
        #                     i['changeNum'] = 0
        #                 if j - i['changeNum'] <0 :
        #                     i['changeNum'] = i['changeNum'] -j
        #                     in_init[in_init.index(j)]= 0
        #     else: print("---------------error----------------")
        #
        # print("result:",in_init)
        # print("行数：",len(in_init))












if __name__ == "__main__":
    unittest.main()
