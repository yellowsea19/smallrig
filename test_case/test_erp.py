import unittest
from common.base.handle_yaml import HandleYaml
from common.base.handle_mysql import HandleMysql
import time,re
from test_suite.erp import Erp
from data.erpdata import *
import importlib, sys, os

importlib.reload(sys)
base_yaml = HandleYaml("conf/base.yaml")
do_mysql = HandleMysql()


class Testwork(unittest.TestCase):


    def setUp(self):
        print('start {}'.format(self))

    def tearDown(self) -> None:
        print('end {}'.format(self))


    def test_taobao_01(self):
        """淘宝拉单流程
        """
        #登录xxl-job获取cookie
        # cookie = Erp().get_job_cookie()
        #
        # Erp().do_job(cookie = cookie,job_id = job_taobao_data["data"]["id"],data=job_taobao_data["data"]["executorParam"])
        #获取ERP token,userId
        token,userId = Erp().zt_login()
        Erp().get_zt_order_number(token = token,userId = userId,order_number="3362809537400734748")

    def test_jd_01(self):
        """京东拉单流程  channelId:88  marketId:10
        """
    # # 登录xxl-job获取cookie
    # cookie = Erp().get_job_cookie()
    # #执行定时任务  【订单拉取】京东订单列表获取
    # Erp().do_job(cookie = cookie,data = job_jd_data["data"])
    # time.sleep(10)
    # #执行定时任务  【京东订单】京东订单插入MySQL
    # Erp().do_job(cookie=cookie, data=job_jd_to_mysql["data"])
    # time.sleep(5)
    # #查询ERP发货订单列表是否已生成发货单
    token, userId = Erp().zt_login()
    order_number =  input("请输入订单号： ")
    order_id = Erp().get_zt_order_number(token=token, userId=userId, order_number=order_number)
    audit_result = Erp().oms_audit(token=token, userId=userId,warehouseId = 232,logistics = "SFCRD",expressType = "SFCRD" ,ids = order_id)
    if "库存不足" in str(audit_result) :
        pass
    elif "未映射" in str(audit_result):
        for i in audit_result :
            pattern = r'\d+'
            # 使用 re.findall() 函数，返回匹配结果列表
            result = re.findall(pattern,i['msg'])
            print(result)
            print("----------------------------------------")

    Erp().do_job(cookie=cookie,data=job_yicang_data)

    # SellerSKU映射关系
    # Erp().SellerSKU_save(token = token,userId = userId,platformCode = "1002408268245537",channelId=88,channel="JD-CN-SmallRig影视器材")
    # # 发货单更新SellerSKU
    # Erp().update_sellerSkuMatch(token = token,userId = userId,id=4124560)

    # def test_0002(self):
    #     token, userId = Erp().zt_login()
    #     Erp().stockTaking_saveOrUpdate(token=token,userId=userId,warehouseId=103,marketId=10,channelId=88)



if __name__ == "__main__":
    unittest.main()