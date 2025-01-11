import pymysql
from logs.log import logger
import unittest
import json
import jsonpath
from jsonpath_ng import jsonpath, parse
class DatabaseComparisonTestCase(unittest.TestCase):

    def setUp(self):
        # 连接数据库1 --冷库
        self.conn1 = pymysql.connect(
            host='192.168.133.213',
            user='root',
            password='root',
            db='smallrig-report'
        )


    def tearDown(self):
        # 关闭数据库连接
        import time
        time.sleep(5)
        self.conn1.close()

    def test_data_comparison(self):
        # 执行数据库1的查询
        cursor1 = self.conn1.cursor()

        SQL= """
        SELECT business_id,form_component_values ,process_name FROM t_dingding_process WHERE originator_dept_id IN (
        62136438,
        425361785,
        630611523,
        630871411,
        631023340,
        838542894

        )
        AND finish_time >="2023-01-01 00:00:00" AND finish_time < '2023-05-31 23:59:59' 
        AND process_name != "新品定价审批"
        # and business_id ='202305291125000427122'
        """
        cursor1.execute(SQL)
        result1 = cursor1.fetchall()

        print(len(result1))
        # logger.info(result1)
        # result = result1[0][0]
        total_menony = []
        result_list={}

        for tmp in result1 :
            # print(tmp)
            print("------------------start--------------------------------")
            print(tmp[0])
            print(tmp[2])
            buniess_id = tmp[0]
            tmp_list = json.loads(tmp[1])

            # print("*************************************************")

            for i in tmp_list :
                # print(i)
                rate = 1
                try:
                    if i['name'] == "参考汇率" :
                        rate = i['value']
                        # print("参考汇率： ",rate)
                except  :
                    pass

                #获取列表2的值
                if i.get('componentType') == 'TableField' :
                    # print(i.get('value'))

                    list2 = json.loads(i['value'])
                    # print("********************")
                    # print(json.dumps(list2,ensure_ascii=False))
                    # print(len(list2[0]))
                    # for i in list2:
                        # print(i)



                    for t in list2:
                        # print("-----------------------------------------------------------------")
                        for cost in t["rowValue"]:

                            # print("cost: ",cost)
                            # print(cost)
                            if cost.get("label") == "费用类别" or cost.get("label") == "研发内部费用类别":
                                cost_name1 = cost['value']
                            if cost.get('label') == "一级费用":
                                cost_name1 = cost['value']
                                # print(cost_name1)
                        for cost2 in t["rowValue"]:
                            # print("cost2:",cost2)

                            if cost2.get("label") == cost_name1:

                                cost_name2 = cost2['value']
                                # print(cost_name2)
                                if cost_name1 == "业务费用":
                                    if cost_name2 == "低值设备费（500-2000元）":
                                        cost_name2 = "办公费"
                                    if cost_name2 == "设计费":
                                        cost_name2 = "新产品设计费"
                                    if cost_name2 == "其他研发费用":
                                        cost_name2 = "其他"
                                    if cost_name2 == "样机样品费用":
                                        cost_name2 = "样品费用"
                                    if cost_name2 == "差旅费":
                                        cost_name2 = "差旅及交通费"
                                    if cost_name2 == "交通费":
                                        cost_name2 = "差旅及交通费"
                                    if cost_name2 == "知识产权费":
                                        cost_name2 = "知识产权的申请费、注册费、代理费"
                                    if cost_name2 == "软件服务费":
                                        cost_name2 = "专业服务费"
                                    if cost_name2 == "设计费":
                                        cost_name2 = "新产品设计费"
                                    if cost_name2 == "模具治具费":
                                        cost_name2 = "样品费用"
                                    if cost_name2 == "其他研发费用":
                                        cost_name2 = "其他"
                                    if cost_name2 == "检验测试认证费":
                                        cost_name2 = "检测认证费"
                                if cost_name1 == "管理费用":
                                    if cost_name2 == "会议费":
                                        cost_name2 = "其他"
                                    if cost_name2 == "低值设备费（500-2000元）":
                                        cost_name2 = "办公费"
                                    if cost_name2 == "其他费用":
                                        cost_name2 = "其他"
                                if cost_name1 == "销售费用":
                                    if  cost_name2 == "福利费":
                                        cost_name1 = "用人费用"
                                    if   cost_name2 == "差旅费":
                                        cost_name1 = "业务费用"
                                    if cost_name2 == "专业服务费":
                                        cost_name1 = "业务费用"
                                    if cost_name2 == "培训费":
                                        cost_name1 = "用人费用"
                                    if cost_name2 == "会议费":
                                        cost_name1 = "管理费用"
                                        cost_name2 = "其他"
                                    if cost_name2 == "通讯费":
                                        cost_name1 = "管理费用"
                                        cost_name2 = "其他"
                                    if cost_name2 == "快递费":
                                        cost_name1 = "业务费用"
                                        cost_name2 = "其他"
                                    if cost_name2 == "交通费":
                                        cost_name1 = "业务费用"
                                        cost_name2 = "差旅及交通费"
                                    if cost_name2 == "业务招待费":
                                        cost_name1 = "业务费用"
                                        cost_name2 = "业务招待费"
                                    if cost_name2 == "低值办公设备(1000-2000元)":
                                        cost_name1 = "业务费用"
                                        cost_name2 = "办公费"
                                    if cost_name2 == "办公费":
                                        cost_name1 = "管理费用"
                                    if cost_name2 == "关务费用":
                                        cost_name1 = "业务费用"
                                        cost_name2 = "报关清关税费"
                                    if cost_name2 == "线下推广宣传费":
                                        cost_name1 = "业务费用"
                                        cost_name2 = "推广费"
                                    if cost_name2 == "设备租赁费":
                                        cost_name1 = "管理费用"
                                        cost_name2 = "其他"
                                    if cost_name2 == "海外关税":
                                        cost_name1 = "业务费用"

                                    if cost_name2 == "推广费":
                                        cost_name1 = "业务费用"

                                    if cost_name2 == "海外应交税费":
                                        cost_name1 = "业务费用"

                                    if cost_name2 == "低值易耗品":
                                        cost_name1 = "管理费用"
                                        cost_name2 = "办公费"
                                    if cost_name2 == "外采成品客退维修":
                                        cost_name1 = "业务费用"
                                        cost_name2 = "其他"
                                    if cost_name2 == "赔偿费":
                                        cost_name1 = "管理费用"
                                        cost_name2 = "其他"

                        result_name = cost_name1+"-"+cost_name2
                        print(result_name)

                        if result_name not in result_list:
                            result_list[f'{cost_name1}-{cost_name2}'] = []
                        # print(list2[t]['rowValue'])
                        for m in t['rowValue'] :
                            # print(m)
                            if m.get('label') == '金额（元）' or m.get('label') =='金额（原币金额）':
                                # print(m['value'])
                                menony = float(m['value'])*float(rate)
                                print(menony)
                                result_list[f'{cost_name1}-{cost_name2}'].append(menony)
                    print("---------------------------end-----------------------------------")


        print(result_list)



        # print(result_list)
        # total = 0
        # for value in total_menony :
        #     total += float(value)
        #
        # # print(total_menony)
        # # print(total)
        #
        # # print(result_list)
        for key,value in result_list.items() :
            print(key,sum([float(x) for x in value]),"-------------",len(value))
            # print(key,sum([float(x) for x in value]))









if __name__ == '__main__':
    unittest.main()