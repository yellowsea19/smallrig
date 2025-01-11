import unittest
# from ddt import ddt, data, unpack
from common.base.handle_yaml import HandleYaml
from common.base.handle_mysql import HandleMysql
from test_suite.admin_api import Admin
from test_suite.test_pc import PC
import time
import importlib, sys, os

importlib.reload(sys)


class Testwork(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     global token,userId
    #     token,userId = PC().pcLogin(username='446941810@qq.com',password='a123456')
    def setUp(self):
        print('start {}'.format(self))
        # token, userId = PC().pcLogin(username='446941810@qq.com', password='a123456')

    def test_order_01(self, sku_list = [(4002, 1)],siteCode="ja_JP"):
        """PC端0元下单（余额支付）
        """
        submitOrderSkus = []
        for i in sku_list:
            tmp_dict = {'num': i[1], 'skuId': PC().getProductId(i[0],siteCode=siteCode), 'orderSkuType': 0, 'thirdpartySkuCode': i[0]}
            submitOrderSkus.append(tmp_dict)
        token, userId = PC().pcLogin(username="314221719@qq.com", password="a123456")
        masterOrderNo, orderActualMoney = PC().submitOrder(token=token, userId=userId, noSubmit=True,
                                                           submitOrderSkus=submitOrderSkus,siteCode=siteCode)
        PC().submitOrder(token=token, userId=userId, noSubmit=False, masterOrderNo=masterOrderNo,deductBalance=orderActualMoney,
                          submitOrderSkus=submitOrderSkus,siteCode=siteCode)

    def test_order_02(self, sku_list = [("APS1854C", 99)],siteCode="ja_JP"):
        """PC端线下付款下单，后台确认收款
        """
        submitOrderSkus = []
        for i in sku_list:
            tmp_dict = {'num': i[1], 'skuId': PC().getProductId(i[0],siteCode=siteCode), 'orderSkuType': 0, 'thirdpartySkuCode': i[0]}
            submitOrderSkus.append(tmp_dict)
        token, userId = PC().pcLogin(username="314221719@qq.com", password="a123456")
        masterOrderNo, orderActualMoney = PC().submitOrder(token=token, userId=userId, noSubmit=True,
                                                           submitOrderSkus=submitOrderSkus,siteCode=siteCode)
        orderNo = PC().submitOrder(token=token, userId=userId, noSubmit=False, masterOrderNo=masterOrderNo,
                         orderActualMoney=orderActualMoney, submitOrderSkus=submitOrderSkus,payWay=3,siteCode=siteCode)
        #登录后台，确认收款
        admin = Admin()
        token, userId = admin.adminLogin(username="huanghai", password="dad9e82a80a5f8f6dd71d9375814f620")
        time.sleep(3)
        pay_id = admin.query_order_pay(token, userId, orderNo)
        admin.confirm_payment(token, userId, pay_id)
    def test_createQuestion(self, productCode="4002"):
        """创建你问我答
        """
        pc_token, pc_userId = PC().pcLogin(username='314221719@qq.com', password='qqqq1111!')
        PC().createQuestion(token=pc_token, userId=pc_userId, productCode=productCode)

    def test_order_no_01(self, order_no='230407072515513256'):
        """根据订单号，返回需要发货的订单商品信息
        """
        token, userId = Admin().adminLogin(username="huanghai", password="17f711ffa7869410fbb8edfcb5f08167")
        tmp_list = Admin().getByOrderNo(token, userId, order_no)


    def test_order_create_deliver_01(self, order_no='230627082551204600'):
        """订单发货
        """
        token, userId = Admin().adminLogin(username="huanghai", password="dad9e82a80a5f8f6dd71d9375814f620")
        orderDelverSkuList = Admin().getByOrderNo(token, userId, order_no)
        res = Admin().createDeliver(token, userId, order_no, orderDelverSkuList, logisticsNo=str(int(time.time())),
                                    logisticsCode='USPS', warehouseCode='warehouseCode')
        print(res)



    def test_order_cancelOrder_01(self, order_no='230407072515513256'):
        """后台取消订单
        """
        token, userId = Admin().adminLogin(username="huanghai", password="17f711ffa7869410fbb8edfcb5f08167")
        res = Admin().cancelOrder(token, userId, order_no)
        print(res)

    def test_register_01(self):
        """注册
        """
        for i in range(10):
            PC().register(account="ssssss%s@163.com"%i,password="a123456",siteCode="ja_JP",inviteCode="PBJ5QV")

    def test_faker(self):
        from faker import Faker
        import random ,string
        f =  Faker(locale="zh_CN")
        # tmp_list=[]
        # for i in range(100):
        #     company_name = f.random_letter()
        #     if company_name not in tmp_list :
        #         tmp_list.append(company_name)
        # for j in tmp_list:
        #     print(j)
        def aa():
            code = [random.choice(string.ascii_uppercase + string.digits) for _ in range(17)]

            # 校验位由大写字母和数字构成
            check_digit = random.choice(string.ascii_uppercase + string.digits)
            code.append(check_digit)
            name = ''.join(code)
            return name
        for i in range(100):
            print(aa())
