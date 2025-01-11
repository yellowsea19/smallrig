import pandas as pd
import statistics
import unittest
import pymysql
import copy
import pandas as pd
from datetime import datetime, timedelta
import math
from decimal import Decimal, getcontext, ROUND_HALF_UP

class Order(unittest.TestCase):

    def setUp(self, env='test'):
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

    def custom_round(self,num):
        integer_part = int(num)
        decimal_part = num - integer_part

        if decimal_part >= 0.5:
            return math.ceil(num)
        else:
            return math.floor(num)

    def custom_round2(self,num):
        decimal_part = num - int(num)

        if decimal_part >= 0.625:
            return math.ceil(num * 100) / 100
        else:
            return math.floor(num * 100) / 100

    def read_excel_data(self, file_path):
        # 读取 Excel 文件
        df = pd.read_excel(file_path)
        # 将数据转换为字典列表
        data_list = []
        for index, row in df.iterrows():
            data_dict = row.to_dict()
            data_list.append(data_dict)
        return data_list


    def test_sell_stat_week_channel_merge(self):
        SQL = "select * from `smallrig-report`.t_sell_stat_week_channel_merge where product_code  = '3813' order by week desc"
        result = self.query_return_dict(SQL)
        for i in result:
            print(i)


    def test_xuefengtiangu(self,need_channel_id = '1818477293413093378',source_product_code=None):


        #查询真实周销量
        need_channel_sales_sql = f"""
                                SELECT week,sum(sales) as sales FROM `smallrig-platform`.t_need_channel_sales WHERE source_product_code = '{source_product_code}' and need_channel_id = {need_channel_id} group by source_product_code,week  order by week asc 
                                """
        results = self.query_return_dict(need_channel_sales_sql)
        #12周真实销量
        real_result = []
        for i in results:
            real_result.append(i['sales'])
        real_result = real_result[-12:]
        print("真实销量: ",real_result)

        # 排序取出结果
        sorted_result = sorted(real_result)
        # print(sorted_result)
        down_date = (12 + 1) / 4
        up_date = (3 * (12 + 1)) / 4
        if isinstance(down_date, int):
            pass
        else:
            # 计算 down_date 在 sorted_result 中的索引
            value_down_date = float(sorted_result[int(down_date) - 1])
            next_down_date = float(sorted_result[int(down_date)])
            # 计算 down_date 的小数部分乘以下一个整数部分在 sorted_result 中的索引
            Q1 = value_down_date + down_date % 1 * (next_down_date - value_down_date)
        print("下四分位： ",Q1)
        if isinstance(up_date, int):
            pass
        else:
            # 计算 up_date 在 sorted_result 中的索引
            value_up_date = float(sorted_result[int(up_date) - 1])
            next_up_date = float(sorted_result[int(up_date)])
            # 计算 up_date 的小数部分乘以下一个整数部分在 sorted_result 中的索引
            Q3 = value_up_date + up_date % 1 * (next_up_date - value_up_date)
        print("上四分位： ",Q3)
        shangxu = Q3 + 1.5 * (Q3 - Q1)
        shangxu =  self.custom_round(shangxu)
        xiaxu = Q1 - 1.5 * (Q3 - Q1)
        xiaxu =  self.custom_round(xiaxu)
        print("上须： ",shangxu)
        print("下须：",xiaxu)
        xuefeng_result =  copy.deepcopy(real_result)


        # 削峰填谷
        for i in xuefeng_result:
            if i < xiaxu:
                xuefeng_result[xuefeng_result.index(i)] = xiaxu
                if shangxu < 0:
                    xuefeng_result[xuefeng_result.index(i)] = 0
            elif i > shangxu:
                xuefeng_result[xuefeng_result.index(i)] = shangxu

        print("削锋填谷：xuefeng_result",xuefeng_result)
        # 小于0，取0

        # 周销标准差：最近12周削峰填谷销量的标准差
        std_deviation = statistics.stdev(xuefeng_result)
        std_deviation = self.custom_round(std_deviation)
        print('周销标准差(平均周销量近12周削峰填谷): std_deviation',std_deviation)

        # 周销标准差(真实销量)
        std_deviation_real = statistics.stdev(real_result)
        std_deviation_real = self.custom_round(std_deviation_real)
        print('周销标准差(平均周销量近12周(真实销量): std_deviation_real', std_deviation_real)

        # 平均周销量：（0.7*9-12周削峰填谷销量+0.2*5-8周削峰填谷销量+0.1*1-4周削峰填谷销量）/4
        xuefeng_avg_sale = (0.7 * (float(xuefeng_result[8]) + float(xuefeng_result[9]) + float(xuefeng_result[10]) + float(xuefeng_result[11])) +0.2 * (float(xuefeng_result[4]) + float(xuefeng_result[5]) + float(
                    xuefeng_result[6]) + float(xuefeng_result[7])) +0.1 * (float(xuefeng_result[0]) + float(xuefeng_result[1]) + float(xuefeng_result[2]) + float(xuefeng_result[3]))) / 4
        xuefeng_avg_sale = round(xuefeng_avg_sale,2)
        xuefeng_avg_sale =  round(xuefeng_avg_sale)
        print("平均周销量（削锋填谷）: xuefeng_avg_sale",xuefeng_avg_sale)




        # 平均周销量：（0.7*9-12真实销量+0.2*5-8真实销量+0.1*1-4真实销量）/4
        agv_week_sale = (Decimal('0.7') * (real_result[8] + real_result[9] + real_result[10] + real_result[11]) +
                         Decimal('0.2') * (real_result[4] + real_result[5] + real_result[6] + real_result[7]) +
                         Decimal('0.1') * (real_result[0] + real_result[1] + real_result[2] + real_result[3])) / 4
        agv_week_sale = self.custom_round(agv_week_sale)
        print("平均周销量（真实销量）: agv_week_sale",agv_week_sale)

        # 变异系数：周销标准差/平均周销量（平均周销量未0时，结果取0）
        if std_deviation == 0 or agv_week_sale == 0:
            bianyi_sex =0
        else:
            bianyi_sex = std_deviation / xuefeng_avg_sale
            getcontext().rounding = ROUND_HALF_UP
            bianyi_sex = Decimal(bianyi_sex)
            bianyi_sex = bianyi_sex.quantize(Decimal('0.00'))
        print("变异系数(近12周削峰填谷)： bianyi_sex",bianyi_sex)

        # 变异系数(真实销量)
        agv_week_sale_real = (Decimal('0.7') * (real_result[8] + real_result[9] + real_result[10] + real_result[11]) +
                              Decimal('0.2') * (real_result[4] + real_result[5] + real_result[6] + real_result[7]) +
                              Decimal('0.1') * (real_result[0] + real_result[1] + real_result[2] + real_result[3])) / 4
        agv_week_sale_real = self.custom_round(agv_week_sale_real)
        if std_deviation_real == 0 or agv_week_sale_real == 0:
            bianyi_sex_real = 0
        else:
            bianyi_sex_real = std_deviation_real / agv_week_sale_real
            bianyi_sex_real = self.custom_round2(bianyi_sex_real)

        print("变异系数(真实销量)： bianyi_sex_real", bianyi_sex_real)


        #获取需求渠道设置配置信息
        need_config_data_sql = f"""
                                select * from `smallrig-platform`.t_need_channel_settings t1 left join t_need_channel_settings_detail t2 on t1.id=t2.need_channel_id where t1.id = {need_channel_id} and t2.source_product_code ='{source_product_code}'
                                """
        need_config_results =  self.query_return_dict(need_config_data_sql)
        for need_config in need_config_results:
            bianyixishu = need_config['stocking_coefficient']
            print("备货系数： ",bianyixishu)

        forecast_week_sale = xuefeng_avg_sale * bianyixishu
        forecast_week_sale = self.custom_round(forecast_week_sale)
        print("预测周销量: forecast_week_sale",forecast_week_sale)

        # 预测30天销量：预测周销量/7*30
        mon_week_sale = forecast_week_sale / 7 * 30
        mon_week_sale = self.custom_round(mon_week_sale)
        print("预测30天销量: mon_week_sale",mon_week_sale)

        new_product_code_sql = f"""
                                        select product_code from t_product where  source_product_code = '{source_product_code}' order by create_time desc limit 1
                                        """
        new_product_code = self.query(new_product_code_sql)[0][0]

        res = { "SKU" : new_product_code,
                "源SKU": source_product_code,
                "产品等级":"",
                "产品状态":"",
                "周销标准差(近12周削峰填谷)": std_deviation,
                "削锋填谷": xuefeng_result,
               # "预测周销量": forecast_week_sale,
                "平均周销量(近12周削峰填谷)": xuefeng_avg_sale,
                "变异系数(近12周削峰填谷)": bianyi_sex,

               "周销标准差(平均周销量近12周(真实销量)": std_deviation_real,
               "平均周销量(真实销量)": agv_week_sale,
                "预测30天销量": mon_week_sale,
                "预测周销量": forecast_week_sale,
               # "变异系数平均周销量(近12周真实销量)": bianyi_sex_real,
                "第1周（削峰填谷）": xuefeng_result[0], "第2周（削峰填谷）": xuefeng_result[1],"第3周（削峰填谷）": xuefeng_result[2], "第4周（削峰填谷）": xuefeng_result[3],"第5周（削峰填谷）": xuefeng_result[4], "第6周（削峰填谷）": xuefeng_result[5],"第7周（削峰填谷）": xuefeng_result[6], "第8周（削峰填谷）": xuefeng_result[7],"第9周（削峰填谷）": xuefeng_result[8], "第10周（削峰填谷）": xuefeng_result[9],"第11周（削峰填谷）": xuefeng_result[10], "第12周（削峰填谷）": xuefeng_result[11],
                "第1周（真实销量）": real_result[0], "第2周（真实销量）": real_result[1],"第3周（真实销量）": real_result[2], "第4周（真实销量）": real_result[3],"第5周（真实销量）": real_result[4], "第6周（真实销量）": real_result[5],"第7周（真实销量）": real_result[6], "第8周（真实销量）": real_result[7],"第9周（真实销量）": real_result[8], "第10周（真实销量）": real_result[9],"第11周（真实销量）": real_result[10], "第12周（真实销量）": real_result[11]
                 }




        # print(res)
        return res

    def test_need_step3(self, is_big_week=False,need_channel_id='1821813107836694529'):
        to_execl_data = []
        step_2_data = []
        need_source_product_code_sql = f"""
                                    select source_product_code from `smallrig-platform`.t_need_channel_settings t1 left join t_need_channel_settings_detail t2 on t1.id=t2.need_channel_id where t1.id = {need_channel_id} 
                                    """
        need_source_product_code_result = self.query_return_dict(need_source_product_code_sql)
        for source_product_code in need_source_product_code_result :
            source_product_code = source_product_code['source_product_code']
            step_2_data.append(self.test_xuefengtiangu(need_channel_id=need_channel_id,source_product_code = source_product_code))
            print(f'-----------------------------------{source_product_code}------------------------------------------------------')
            # 获取需求渠道设置配置信息
            need_config_data_sql = f"""
                                    select * from `smallrig-platform`.t_need_channel_settings t1 left join t_need_channel_settings_detail t2 on t1.id=t2.need_channel_id where t1.id = {need_channel_id} and t2.source_product_code ='{source_product_code}'
                                    """
            need_config_results = self.query_return_dict(need_config_data_sql)
            for need_config in need_config_results:
                # 采购仓库存："采购仓"类型的仓库的可用库存之和 (当类型为C/D/E类时，过滤掉Market为B2B-Pro、B2B-Pro(DBC)的数据)
                #备货等级为   C/D/E类  时
                if need_config['stocking_level'] == 2:
                    print('C/D/E类')
                    cg_inv_SQL = f"""
                                    SELECT sum(CASE WHEN (t1.product_num - t1.wait_num) < 0 THEN 0 ELSE (t1.product_num - t1.wait_num) END )AS SIOP页面可用数量
                                    FROM `smallrig-platform`.t_product_inventory t1
                                    LEFT JOIN `smallrig-platform`.t_warehouse t2 ON t1.warehouse_id = t2.id
                                    WHERE t1.market_id NOT in (8,96) AND t1.product_id in (
                                    SELECT id
                                    FROM t_product t3
                                    WHERE t3.source_product_code = '{source_product_code}') AND t1.del_flag = 1 AND t2.is_purchase_warehouse = 1 AND t2.del_flag = 1;
                                    """
                else:
                    cg_inv_SQL = f"""
                                    SELECT sum(CASE WHEN (t1.product_num - t1.wait_num) < 0 THEN 0 ELSE (t1.product_num - t1.wait_num) END )AS SIOP页面可用数量
                                    FROM `smallrig-platform`.t_product_inventory t1
                                    LEFT JOIN `smallrig-platform`.t_warehouse t2 ON t1.warehouse_id = t2.id
                                    WHERE t1.product_id in (
                                    SELECT id
                                    FROM t_product t3
                                    WHERE t3.source_product_code = '{source_product_code}') AND t1.del_flag = 1 AND t2.is_purchase_warehouse = 1 AND t2.del_flag = 1;
                                    """
                cg_inv = self.query_return_dict(cg_inv_SQL)[0]['SIOP页面可用数量']
                if cg_inv is None :
                    cg_inv = 0
                print("采购库存:　", cg_inv)

                SIOP_inv_SQL = f"""
                                SELECT  CASE WHEN (SUM(t1.product_num - t1.wait_num)) < 0 THEN 0 ELSE (SUM(t1.product_num - t1.wait_num)) END AS SIOP页面可用数量
                                FROM `smallrig-platform`.t_product_inventory t1
                                LEFT JOIN `smallrig-platform`.t_warehouse t2 ON t1.warehouse_id = t2.id
                                WHERE t1.market_id = 91 AND t1.product_id in (
                                SELECT id
                                FROM t_product t3
                                WHERE t3.source_product_code = '{source_product_code}') AND t1.del_flag = 1 AND t2.is_purchase_warehouse = 1 AND t2.del_flag = 1
    
                                """
                # print(SIOP_inv_SQL)
                SIOP_inv = self.query_return_dict(SIOP_inv_SQL)[0]['SIOP页面可用数量']
                if SIOP_inv is None:
                    SIOP_inv = 0
                SIOP_inv =  int(SIOP_inv)
                print("SIOP页面可用数量:　SIOP_inv:", SIOP_inv)

                # 《需求计划》在途："已审核"状态，SKU明细状态为"未完结"，（需求数量-回货数量）之和
                xq_zaitu_sql = f"""
                                SELECT SUM(t2.need_num - t2.received_quantity) AS 需求计划在途
                                FROM `smallrig-platform`.t_need_plan t1
                                LEFT JOIN t_need_plan_detail t2 ON t1.id = t2.need_plan_id
                                WHERE t1.status = 2 AND t1.del_flag = 1  AND t2.sku_status = 0 AND t2.del_flag=1 AND t2.product_id in (SELECT id
                                FROM t_product t3
                                WHERE t3.source_product_code = '{source_product_code}')
                                """
                xq_zaitu = self.query_return_dict(xq_zaitu_sql)[0]['需求计划在途']
                if xq_zaitu is None:
                    xq_zaitu = 0
                print("需求计划在途数量：xq_zaitu: ", xq_zaitu)

                # 《备货计划》在途："已审核"状态，SKU明细状态为"未完结"，（需求数量-分货数量）之和
                bh_zaitu_sql = f"""
                                SELECT SUM(t2.need_num-t2.received_quantity) AS 备货计划在途
                                FROM `smallrig-platform`.t_stock_plan t1
                                LEFT JOIN t_stock_plan_detail t2 ON t1.id = t2.stock_plan_id
                                WHERE t1.`status` = 2 AND t1.del_flag = 1 and t2.del_flag=1 AND t2.sku_status = 0 AND t2.product_id in (SELECT id
                                FROM t_product t3
                                WHERE t3.source_product_code = '{source_product_code}')
    
                                """
                bh_zaitu = self.query_return_dict(bh_zaitu_sql)[0]['备货计划在途']
                if bh_zaitu == None:
                    bh_zaitu = 0

                print("备货计划在途数量：bh_zaitu: ", bh_zaitu)

                today = datetime.today()
                next_monday = today + timedelta(days=(7 - today.weekday()))
                next_monday_at_midnight = datetime(next_monday.year, next_monday.month, next_monday.day)
                print(next_monday_at_midnight)

                # 第13周："已审核"状态、SKU明细状态为"未完结"、SKU期望交期小于等于13周的备货计划，（需求数量-回货数量）之和
                week_13_bh_sql = f"""
                            SELECT SUM(t2.need_num-t2.received_quantity) AS 备货计划在途
                            FROM `smallrig-platform`.t_stock_plan t1
                            LEFT JOIN t_stock_plan_detail t2 ON t1.id = t2.stock_plan_id
                            WHERE t1.`status` = 2 AND t1.del_flag = 1 and t2.del_flag=1 AND t2.sku_status = 0 AND t2.product_id in (SELECT id
                            FROM t_product t3
                            WHERE t3.source_product_code = '{source_product_code}') AND t2.expected_delivery_date < '{next_monday_at_midnight}'
                            """
                week_13 = self.query(week_13_bh_sql)[0][0]
                if week_13 == None:
                    week_13 = 0
                print("13周提货量： ", week_13)
                # 需要全局更新为，product_code 取最新的SKU
                product_status_sql = f"""
                                    select product_status_name from t_product where  source_product_code = '{source_product_code}' order by create_time desc limit 1
                                    """
                product_status = self.query(product_status_sql)[0][0]

                # 第14周："是否备货大周"为是，"已审核"状态、SKU明细状态为"未完结"、SKU期望交期大于等于14周的备货计划，（需求数量-回货数量）之和

                week_14_bh_sql = f"""
                                SELECT SUM(t2.need_num-t2.received_quantity) AS 备货计划在途
                                FROM `smallrig-platform`.t_stock_plan t1
                                LEFT JOIN t_stock_plan_detail t2 ON t1.id = t2.stock_plan_id
                                WHERE t1.`status` = 2 AND t1.del_flag = 1 and t2.del_flag=1 AND t2.sku_status = 0 AND t2.product_id in (
                                SELECT id
                                FROM t_product t3
                                WHERE t3.source_product_code = '{source_product_code}') AND t2.expected_delivery_date >= '{next_monday_at_midnight}';
                                            """
                week_14 = self.query(week_14_bh_sql)[0][0]
                if week_14 == None:
                    week_14 = 0
                print("14周提货量： ", week_14)
                # 对于产品状态为:待售、预售、在售、测试、赠品的SKU，取（大于等于14周《备货计划》在途数量，预测周销量)的较大值---按最新SKU

                #最新SKU
                new_product_code_sql = f"""
                                select product_code from t_product where  source_product_code = '{source_product_code}' order by create_time desc limit 1
                                """
                new_product_code = self.query(new_product_code_sql)[0][0]
                forecast_week_sale = self.test_xuefengtiangu( need_channel_id=need_channel_id,
                                                             source_product_code=source_product_code)['预测周销量']
                if is_big_week:
                    pass
                else:
                    if product_status in ("待售", "预售", "在售", "测试", "赠品"):
                        forecast_week_sale = self.test_xuefengtiangu(need_channel_id = need_channel_id,source_product_code=source_product_code)[
                            '预测周销量']
                        if week_14 >= forecast_week_sale:
                            week_14 = week_14
                            print("第14周: ", week_14)
                        else:
                            week_14 = forecast_week_sale
                            print("第14周: ", week_14)
                    else:
                        # 对于产品类型为其它值的SKU,取（大于等于14周《备货计划》在途数量，预测周销量)的较大值,直至《需求计划》在途数量分配完毕
                        forecast_week_sale = self.test_xuefengtiangu(need_channel_id = need_channel_id,source_product_code=source_product_code)[
                            '预测周销量']
                        if week_14 >= forecast_week_sale:
                            week_14 = week_14

                        else:
                            week_14 = forecast_week_sale
                        week_14 = min(week_14, xq_zaitu - week_13)
                        if week_14 <= 0:
                            week_14 = 0
                        print("14周提货量： ", week_14)

                # 15、16周
                # 削峰填谷均销：（0.7*9-12周削峰填谷销量+0.2*5-8周削峰填谷销量+0.1*1-4周削峰填谷销量）
                xuefengtiangu = self.test_xuefengtiangu(need_channel_id = need_channel_id,source_product_code=source_product_code)
                result = xuefengtiangu['削锋填谷']
                agv_sale = ((Decimal('0.7') * (result[8] + result[9] + result[10] + result[11]) +
                             Decimal('0.2') * (result[4] + result[5] + result[6] + result[7]) +
                             Decimal('0.1') * (result[0] + result[1] + result[2] + result[3]))) / 4
                agv_sale = self.custom_round(agv_sale)
                if need_config['is_head_product'] == 1:
                    if need_config['turnaround_months'] == 1:
                        week_15_16 = agv_sale * 14
                    elif need_config['turnaround_months'] == 2:
                        week_15_16 = agv_sale * 11
                    elif need_config['turnaround_months'] == 3:
                        week_15_16 = agv_sale * 7
                    else:
                        week_15_16 = 0
                elif need_config['is_head_product'] == 0:
                    if need_config['turnaround_months'] == 1:
                        week_15_16 = agv_sale * 14
                    elif need_config['turnaround_months'] == 2:
                        week_15_16 = agv_sale * 7
                    elif need_config['turnaround_months'] == 3:
                        week_15_16 = agv_sale * 6
                    else:
                        week_15_16 = 0
                print('15-16周提货量： week_15_16 ', week_15_16)

                # 17-25周 对于产品状态为:待售、预售、在售、测试、赠品的SKU，取预测周销量
                if product_status in ("待售", "预售", "在售", "测试", "赠品"):
                    week_17_25 = self.test_xuefengtiangu(need_channel_id = need_channel_id,source_product_code=source_product_code)[
                        '预测周销量']
                    total_17_25 = []
                    for i in range(17,26):
                        total_17_25.append(week_17_25)

                    print("17-25周提货数量： forecast_week_sale", total_17_25)
                else:
                    # 对于产品类型为其它值的SKU，取取预测周销量，直至《需求计划》在途数量分配完毕
                    # 先算出13-16周《需求计划》在途数量分配剩余数量
                    total_xq_syzaitu = xq_zaitu - week_13 - week_14 - week_15_16
                    if total_xq_syzaitu <= 0:
                        total_xq_syzaitu = 0
                    forecast_week_sale = self.test_xuefengtiangu(need_channel_id = need_channel_id,source_product_code=source_product_code)[
                        '预测周销量']
                    print("total_xq_syzaitu",total_xq_syzaitu)

                    def recursive_pick(total_xq_syzaitu, forecast_week_sale, remaining_picks, start_week, items_list=[]):
                        if remaining_picks == 0:
                            return items_list
                        else:
                            items_picked = min(total_xq_syzaitu, forecast_week_sale)
                            remaining_items = total_xq_syzaitu - items_picked

                            print(f"{start_week}周提货数: {items_picked}")
                            start_week += 1

                            items_list.append(int(items_picked))

                            return recursive_pick(remaining_items, forecast_week_sale, remaining_picks - 1, start_week,
                                                  items_list)

                    total_17_25 = recursive_pick(total_xq_syzaitu=total_xq_syzaitu, forecast_week_sale=forecast_week_sale,
                                                 remaining_picks=9, start_week=17)
                    print(total_17_25)
            # 需下单数量
            if need_config['stocking_level'] == 1:

                need_num = (week_13 + week_14 + week_15_16 + sum(total_17_25)) - SIOP_inv - xq_zaitu
            else:
                need_num = (week_13 + week_14 + week_15_16 + sum(total_17_25)) - cg_inv - xq_zaitu
            if need_num < 0:
                need_num = 0
            print("需下单数量:  need_num ", need_num)

            stock_level = {1:"A/B类",2:"C/D/E类",3:"成长期"}
            to_execl_data.append({"SKU":new_product_code,
                                "源SKU":source_product_code,
                                "产品等级":stock_level[need_config['stocking_level']],
                                "产品状态":product_status,
                                "预测周销量":forecast_week_sale,
                                "SIOP库存":SIOP_inv,
                                "采购仓库存":cg_inv,
                                "《需求计划》在途":xq_zaitu,
                                "《备货计划》在途":bh_zaitu,
                                "需下单数量":need_num,
                                "第32周(提货量预测)":week_13,
                                "第33周(提货量预测)":week_14,
                                "第34周+第35周(提货量预测)":week_15_16,
                                "第36周(提货量预测)":total_17_25[0],
                                "第37周(提货量预测)":total_17_25[1],
                                "第38周(提货量预测)":total_17_25[2],
                                "第39周(提货量预测)":total_17_25[3],
                                "第40周(提货量预测)":total_17_25[4],
                                "第41周(提货量预测)":total_17_25[5],
                                "第42周(提货量预测)":total_17_25[6],
                                "第43周(提货量预测)":total_17_25[7],
                                "第44周(提货量预测)":total_17_25[8]


                                  })
        # 创建 DataFrame
        df = pd.DataFrame(step_2_data)
        # 输出到 Excel 文件
        excel_file = 'step2.xlsx'
        df.to_excel(excel_file, index=False)
        print(f"step2数据已成功输出到 {excel_file}")
        # 创建 DataFrame
        df = pd.DataFrame(to_execl_data)
        # 输出到 Excel 文件
        excel_file = 'step3.xlsx'
        df.to_excel(excel_file, index=False)
        print(f"step3数据已成功输出到 {excel_file}")



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



def test_0718(self):
    # start_week = 17
    def recursive_pick(total_xq_syzaitu, forecast_week_sale, remaining_picks=9, start_week=17):
        if remaining_picks == 0:
            return 0
        else:
            items_picked = min(total_xq_syzaitu, forecast_week_sale)
            remaining_items = total_xq_syzaitu - items_picked

            print(f"{start_week}周提货数: {items_picked}")
            start_week += 1

            return items_picked + recursive_pick(remaining_items, forecast_week_sale, remaining_picks - 1, start_week)

    total_items = 200
    items_per_pick = 60
    total_picks = 9

    total_picked = recursive_pick(total_items, items_per_pick, total_picks)
    print(f"Total items picked: {total_picked}")




























