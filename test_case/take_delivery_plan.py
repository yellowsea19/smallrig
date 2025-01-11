import logging

from logs.log import *

import unittest
import pymysql
import copy
import pandas as pd



class take_delivery(unittest.TestCase):

    def setUp(self, env='test'):
        self.env = env
        if self.env == 'test':
            self.urls = 'http://192.168.133.223:5555'
            self.xxl_url = 'http://192.168.133.223:19010'
            self.connection = pymysql.connect(host='192.168.133.213',  # 数据库地址
                                              user='root',  # 数据库用户名
                                              password='root',  # 数据库密码
                                              db='smallrig-platform',
                                              cursorclass = pymysql.cursors.DictCursor
                                              )  # 数据库名称

            self.cursor = self.connection.cursor()
        elif self.env == 'uat':
            self.urls = 'https://bereal.smallrig.net'
            self.xxl_url = 'http://192.168.133.232:19010'
            self.connection = pymysql.connect(host='192.168.133.233',  # 数据库地址
                                              user='root',  # 数据库用户名
                                              password='Leqi!2022',  # 数据库密码
                                              db='smallrig-platform',
                                              cursorclass=pymysql.cursors.DictCursor
                                              )  # 数据库名称
            self.cursor = self.connection.cursor()

    def tearDown(self):
        self.cursor.close()
        self.connection.close()

    def query(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def query_return_dict(self, sql):
        self.cursor.execute(sql)
        columns = [col[0] for col in self.cursor.description]
        results = []
        for row in self.cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

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



    def read_excel_data(self, file_path):
        # 读取 Excel 文件
        df = pd.read_excel(file_path)
        # 将数据转换为字典列表
        data_list = []
        for index, row in df.iterrows():
            data_dict = row.to_dict()
            data_list.append(data_dict)
        return data_list





    def test_delivery_plan(self,take_delivery_no='TD24102800001'):

        #提化计划导入的提货明细
        tihuo_data = self.read_excel_data(r'E:\ERP\F1 ERP V6.0.26_20241113\提货明细导入模板.xlsx')
        #提货计划导入的核算时金蝶采购单明细导入模板
        purchase_data = self.read_excel_data(r'E:\ERP\F1 ERP V6.0.26_20241113\核算时金蝶采购单明细导入模板.xlsx')
        for data in tihuo_data:
            logging.debug(data)

            #根据物料编码统计金蝶采购单的剩余收料数量
            kingdee_remain_receive_qty_sql = f"""
                                            SELECT  SUM(remain_receive_qty) as remain_receive_qty FROM t_kingdee_purchase_order WHERE mat_no = "{data['金蝶物料编码']}"
                                            """
            #金蝶采购单列表的物料剩余收料数量
            kingdee_remain_receive_qty = self.query(kingdee_remain_receive_qty_sql)[0]['remain_receive_qty']

            logger.info("物料编码： "+str(data['金蝶物料编码']))
            logger.info("剩余收料数量："+str(kingdee_remain_receive_qty))
            # 提货计划-物料明细
            wuliao_detail_sql = f"""
                                SELECT * FROM t_take_delivery_plan_material_details WHERE mat_no = '{data['金蝶物料编码']}' AND  plan_id = (SELECT id FROM t_take_delivery_plan WHERE take_delivery_no = '{take_delivery_no}' )
                                """

            wuliao_results = self.query(wuliao_detail_sql)[0]
            need_revise_num = wuliao_results['need_revise_num']
            #货计划导入的核算时金蝶采购单明细的剩余入库数量
            for data1 in purchase_data:
                if data1['金蝶物料编码'] == data['金蝶物料编码']:
                    remain_in_qty = data1['剩余入库数量']
                    logger.info('剩余入库数量: '+str(remain_in_qty))
                    if kingdee_remain_receive_qty is None:
                        kingdee_remain_receive_qty = 0
                    need_revise = kingdee_remain_receive_qty - data1['剩余入库数量']
                    logger.info("库存修正： "+str(need_revise))
                    if need_revise_num != need_revise :
                        logger.error("库存修正:"+str(data['金蝶物料编码'])+f"-------->数据库为{need_revise_num},实际应该为：{need_revise}")
                    #需求1(采购修正)
                    caigou_revise1 = wuliao_results['need_num1'] +need_revise
                    #需求1(采购修正)如果小于0，取0
                    if caigou_revise1 < 0 :
                        caigou_revise1 = 0
                    if caigou_revise1 != wuliao_results['need_revise_num1'] :
                        logger.error("需求1(采购修正):" + str(data['金蝶物料编码']) + f"-------->数据库为{wuliao_results['need_revise_num1']},实际应该为：{caigou_revise1}")
                    #需求2(采购修正)
                    caigou_revise2 = wuliao_results['need_num1'] + wuliao_results['need_num2'] +need_revise -caigou_revise1
                    if caigou_revise2 != wuliao_results['need_revise_num2'] :
                        logger.error("需求2(采购修正):" + str(data['金蝶物料编码']) + f"-------->数据库为{wuliao_results['need_revise_num2']},实际应该为：{caigou_revise2}")
                    if wuliao_results['need_num1'] +wuliao_results['need_num2'] != wuliao_results['total_need_num'] :
                        logger.error(str(data['金蝶物料编码'])+" : 需求合计错误")
                    if wuliao_results['need_revise_num1'] +wuliao_results['need_revise_num2'] != wuliao_results['total_revise_need_num'] :
                        logger.error(str(data['金蝶物料编码'])+" : 需求合计(采购修正) 错误")
                    #采购单需求拆分数量
                    if  kingdee_remain_receive_qty >= wuliao_results['total_revise_need_num'] :
                        need_split = wuliao_results['total_revise_need_num']
                    else:
                        need_split = kingdee_remain_receive_qty
                    if need_split != wuliao_results['need_split_num']:
                        logger.error(f"采购单需求拆分数量错误，实际应该是{need_split},数据库为{wuliao_results['need_split_num']}")
                    logger.info('--------------------------end-------------------------------')












        # # 创建 DataFrame
        # df = pd.DataFrame(to_execl_data)
        # # 输出到 Excel 文件
        # excel_file = 'step3.xlsx'
        # df.to_excel(excel_file, index=False)
        # print(f"step3数据已成功输出到 {excel_file}")

    def test_bijiao(self):
        # 读取第一个 Excel 文件
        df1 = pd.read_excel('step3.xlsx')

        # 读取第二个 Excel 文件
        df2 = pd.read_excel(r'C:\Users\huanghai\Downloads\需求计划计算器_20240809171749.xlsx')

        # 将两个 DataFrame 转换为字典，以便比较
        dict1 = df1.to_dict(orient='records')
        dict2 = df2.to_dict(orient='records')

        # 比较两个字典
        for i in range(len(dict1)):
            for key in dict1[i]:
                if dict1[i][key] != dict2[i][key]:
                    print(f"Row {i + 2}, Key {key}: {dict1[i][key]} != {dict2[i][key]}")






























