import requests
from common.base.handle_yaml import HandleYaml
from data import admindata
import json,time
from common.base.handle_mysql import HandleMysql
import importlib,sys
from logs.log import logger
from common.tool.aes import *
import urllib.parse
import datetime
importlib.reload(sys)

base_yaml = HandleYaml("conf/base.yaml")
do_mysql = HandleMysql()


class Erp:


    def __int__(self):
        # 测试环境
        self.job_base_url = "http://192.168.133.223:19010"
        # 中台登录地址
        self.zt_admin_base_url = "http://192.168.133.223:8888"
        # 业务中台地址
        self.zt_url = "http://192.168.133.223:5555"


    def get_job_cookie(self,username="admin",password="smallrig%23321"):
        """获取job登录信息
        """
        uri = "/smallrig-job-admin/login"
        url = base_yaml.get_data("admin","job_base_url") + uri
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest"
        }
        data = f"userName={username}&password={password}"
        res = requests.post(url=url, params=data, headers=headers)
        logger.debug("\n" + url + "\n" + str(headers) + "\n" + str(data) + "\n" + res.text + "\n")

        return res.headers["Set-Cookie"]


    def do_job(self, cookie, job_id,data):
        """执行定时任务
        """
        uri = "/smallrig-job-admin/jobinfo/trigger"
        url = base_yaml.get_data("admin","job_base_url") + uri
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Cookie": cookie
        }
        if data != None:

            data = "id=%s&executorParam=%s&addressList=" % (job_id, data)
        else:
            data = "id=%s&addressList=" % job_id

        res = requests.post(url=url, params=data, headers=headers)

        logger.debug("\n" + url + "\n" + data + "\n" + res.text + "\n")

    def zt_login(self, username="auto1",password="486cb64efebcb5edeb6a23c2b6087fff"):
        """业务中台登录
        """
        uri = "/API/manage/login"
        url = base_yaml.get_data("admin","zt_login_url") + uri
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "system-code": "XTZX",
        }


        data = {"systemCode": "XTZX", "username": username, "password": password,
                    "_t": int(time.time() * 1000)}
        res = requests.post(url=url, data=json.dumps(data), headers=headers)
        logger.debug("\n" + url + "\n" + str(headers) + "\n" + str(data) + "\n" + res.text + "\n")
        return res.json()["data"]["accessToken"], res.json()["data"]["userId"]

    def get_zt_order_number(self, token, userId, order_number):
        """查询中台订单
        """
        uri = "/API/oms/order/v1/list"
        url = base_yaml.get_data("admin","zt_url") + uri
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "system-code": "ERP",
            # "system-code": "YWZT",
            "Access-Token": token,
            "User-Id": userId
        }

        data = {"pageSize": 16, "pageNum": 1,
                "createTimeArr": ["2022-03-25 00:00:00", "%s 23:59:59" % datetime.datetime.now().strftime("%Y-%m-%d")],
                "name": order_number, "beginDate": "2022-03-25 00:00:00",
                "endDate": "%s 23:59:59" % datetime.datetime.now().strftime("%Y-%m-%d"), "codeType": 2, "codeMode": 1,
                "logisticsStatus": 0, "timestamp": int(time.time() * 1000)}
        logger.debug(url)
        res = requests.post(url=url, data=json.dumps(data), headers=headers)
        logger.debug("\n" + url + "\n" + str(headers) + "\n" + str(data) + "\n" + res.text + "\n")
        logger.debug(res.text)
        if res.json()["data"]["total"] == 0:
            logger.info("未查到业务中台订单")
            time.sleep(3)
            self.get_zt_order_number(token, userId, order_number)
        elif res.json()["data"]["total"] == 1:
            time.sleep(0.5)
            logger.info("已查到业务中台订单")
            logger.debug("\n" + url + "\n" + str(headers) + "\n" + str(data) + "\n" + res.text + "\n")
            return res.json()["data"]["items"][0]["id"]
        else:
            raise Exception




if __name__ == "main":
    Erp().get_job_cookie()