import requests, json, time
import random
import datetime
from urllib import parse
from logs.log import logger


# logger.basicConfig(level=logger.DEBUG,
#                     format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class Sync:
    def __init__(self, env="test", order_number=None):
        self.order_number = order_number
        self.env = env
        if self.env == "test":
            # 测试环境
            self.job_base_url = "http://192.168.133.223:19010"
            # 【订单拉取】自建商城拉取订单
            self.pull_order_id = 203
            # 【文件解析】订单列表文件解析
            self.file_parsing_id = 15
            # 【订单同步】自建商城=》MySQL
            self.push_mysql_zt_id = 204
            # 中台登录地址
            self.zt_admin_base_url = "http://192.168.133.223:8888"
            # 业务中台地址
            self.zt_url = "http://192.168.133.223:5555"
            # 【订单标发】Sign订单标发
            self.order_send_out_id = 168

        elif env == "uat":
            # uat环境
            self.job_base_url = "http://192.168.133.224:19010"
            # 【订单拉取】自建商城拉取订单
            self.pull_order_id = 312
            # 【文件解析】订单列表文件解析
            self.file_parsing_id = 15
            # 【订单同步】自建商城=》MySQL
            self.push_mysql_zt_id = 314
            # 中台登录地址
            self.zt_admin_base_url = "http://192.168.133.224:8888"
            # 业务中台地址
            self.zt_url = "http://192.168.133.224:90"
            # 【订单标发】Sign订单标发
            self.order_send_out_id = 283

        else: raise ValueError("环境env入参错误，仅支持‘test’或‘uat’")
        self.cookie = self.get_job_cookie()
    def get_job_cookie(self):
        """获取job登录信息
        """
        uri = "/smallrig-job-admin/login"
        url = self.job_base_url + uri
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest"
        }
        data = "userName=admin&password=smallrig%23321"
        res = requests.post(url=url, params=data, headers=headers)
        logger.debug("\n" + url + "\n" + str(headers) + "\n" + str(data) + "\n" + res.text + "\n")

        return res.headers["Set-Cookie"]

    def do_job(self, cookie, job_id, data=None):
        """执行定时任务
        """
        uri = "/smallrig-job-admin/jobinfo/trigger"
        url = self.job_base_url + uri
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

    def zt_login(self, env):
        """业务中台登录
        """
        uri = "/API/manage/login"
        url = self.zt_admin_base_url + uri
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "system-code": "XTZX",
        }
        self.env = env
        if self.env == "test":
            data = {"systemCode": "XTZX", "username": "auto1", "password": "43e685a0b8bb3fded4506bdb515cd639",
                    "_t": int(time.time() * 1000)}
        elif self.env == "uat":
            data = {"systemCode": "XTZX", "username": "huanghai ", "password": "dad9e82a80a5f8f6dd71d9375814f620",
                    "_t": int(time.time() * 1000)}
        res = requests.post(url=url, data=json.dumps(data), headers=headers)
        logger.debug("\n" + url + "\n" + str(headers) + "\n" + str(data) + "\n" + res.text + "\n")
        return res.json()["data"]["accessToken"], res.json()["data"]["userId"]

    def get_zt_order_number(self, token, userId, order_number):
        """查询中台订单
        """
        uri = "/API/oms/order/v1/list"
        url = self.zt_url + uri
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
            self.do_job(self.cookie, self.push_mysql_zt_id)
            time.sleep(20)
            self.get_zt_order_number(token, userId, order_number)
        elif res.json()["data"]["total"] == 1:
            time.sleep(0.5)
            logger.info("已查到业务中台订单")
            logger.debug("\n" + url + "\n" + str(headers) + "\n" + str(data) + "\n" + res.text + "\n")
            return res.json()["data"]["items"][0]["id"]
        else:
            raise Exception

    def order_send_out(self, token, userId, orderId):
        """订单标发
        """
        uri = "/API/oms/order/v1/sendOut"
        url = self.zt_url + uri
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "system-code": "ERP",
            # "system-code": "YWZT",
            "Access-Token": token,
            "User-Id": userId
        }

        time1 = datetime.datetime.now() + datetime.timedelta(minutes=-1)
        data = [{"warehouseId":57,"expressType":"YUANTONG","expressTypeName":"圆通","orderId":orderId,"trackNo":"%s"%random.randint(100000, 999999),"sendTime":"%s"%time1.strftime("%Y-%m-%d %H:%M:%S")}]
        res = requests.post(url=url, data=json.dumps(data), headers=headers)
        if res.json()['code'] != 10000 :
            raise  AttributeError (res.json()['message'])

        logger.debug(res.text)

    def __call__(self):
        cookie = self.get_job_cookie()
        # 拉取订单
        pull_order_data = {"minuteStr": 10}
        logger.info("【订单拉取】自建商城拉取订单")
        self.do_job(cookie, job_id=self.pull_order_id, data=pull_order_data)
        time.sleep(20)
        # # 订单文件解析
        # logger.info("文件解析")
        # self.do_job(cookie, self.file_parsing_id)

        logger.info("【订单同步】自建商城=》MySQL")
        self.do_job(cookie, self.push_mysql_zt_id)
        time.sleep(20)
        # 后台登录业务中台
        token, userId = self.zt_login(self.env)
        # 业务中台查询订单
        order_id = self.get_zt_order_number(token, userId, order_number=self.order_number)
        logger.debug(order_id)
        if order_id == None:
            order_id = self.get_zt_order_number(token, userId, order_number=self.order_number)
        # 订单标发
        logger.info("业务中台订单标发")
        self.order_send_out(token, userId, order_id)
        # XX-job【订单标发】Sign订单标发
        logger.info("执行订单标发定时任务")
        data = parse.quote('{"orderId":%s}' % order_id)
        self.do_job(cookie, job_id=self.order_send_out_id, data=data)
        logger.info("----------- end -------------------")


if __name__ == '__main__':
    sync = Sync(env="test", order_number="221021071829458095")
    sync()
