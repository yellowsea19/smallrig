import unittest
from ddt import ddt, data, unpack
from common.base.handle_yaml import HandleYaml
from common.base.handle_mysql import HandleMysql
from test_suite.admin_api import Admin
from test_suite.test_pc import PC
import time
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


    def test_001(self):
        """淘宝拉单流程
        """
        #登录xxl-job获取cookie
        # cookie = Erp().get_job_cookie()
        #
        # Erp().do_job(cookie = cookie,job_id = job_taobao_data["data"]["id"],data=job_taobao_data["data"]["executorParam"])
        #获取ERP token,userId
        token,userId = Erp().zt_login()
        Erp().get_zt_order_number(token = token,userId = userId,order_number="3362809537400734748")
