import unittest
# from common.base.handle_yaml import HandleYaml
# from common.base.handle_mysql import HandleMysql
from test_suite.test_pc import PC
from test_case.test_sync import Sync
import importlib,sys

importlib.reload(sys)


class Order(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        global token,userId
        token,userId = PC().pcLogin(username="yellowsea2057@gmail.com",password="a123456")

    def setUp(self):
        print('start {}'.format(self))


    def test_order_delivery(self):
        """PC端下单业务中台发货
        """
        # order_number=PC().submitOrder(token,userId)
        # print(order_number)
        # sync = Sync(env="uat", order_number=order_number)
        sync = Sync(env="uat", order_number="220804104433195238")
        sync()





