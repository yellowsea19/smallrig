import requests
from common.base.handle_yaml import HandleYaml
from data import pcdata
import json,time
from test_suite.admin_api import Admin
from common.base.handle_mysql import HandleMysql
import importlib,sys
from logs.log import logger
# from luck_draw import get_ip,get_country
# ip=get_ip()

importlib.reload(sys)

base_yaml = HandleYaml("conf/base.yaml")
do_mysql = HandleMysql()

class PC:

    def pcLogin(self,username=None,password=None):
        """PC登录接口
        """
        self.get_data = pcdata.login
        self.url = base_yaml.get_data("pc","loign_url") + self.get_data["path"]
        self.headers = {"Content-Type": "application/json"}
        self.data = self.get_data["data"]
        if username is None or password is None:
            self.data = self.get_data["data"]
        else:
            self.data['account'] = username
            self.data['passwd'] = password
        request = requests.post(url = self.url,headers = self.headers,data = json.dumps(self.data))
        response = request.json()
        print(self.url)
        print("请求参数：{0}\n响应：{1}".format(self.data, response))
        return response['data']['token'], response['data']['userId']

    def register(self,account=None,password=None,siteCode="en_US",inviteCode=""):
        """PC注册接口
        """
        self.get_data = pcdata.memberLogin_register
        self.url = base_yaml.get_data("pc","loign_url") + self.get_data["path"]
        self.headers = {"Content-Type": "application/json",
                        "Site-Code": siteCode,
                        "System-Port": "0"
                        }
        self.data = self.get_data["data"]
        self.data['account'] = account
        self.data['passwd'] = password
        self.data['inviteCode'] = inviteCode
        request = requests.post(url = self.url,headers = self.headers,data = json.dumps(self.data))
        response = request.json()
        print(self.url)
        print("请求参数：{0}\n响应：{1}".format(self.data, response))
        return response

    def joinShoppingCart(self,token,userId,quantity=1,skuId="1508759569618771970"):
        """加入购物车
        """
        self.get_data = pcdata.joinShoppingCart
        self.url = base_yaml.get_data("pc","host") + self.get_data["path"]
        self.headers = {
                    "Access-Token": token,
                    "Content-Type": "application/json;charset=UTF-8",
                    "User-Id": userId,
                    "System-Port": "0",
                    "Flow-Sourcet": "0",
                    "Accept-Language": "en_US",
                }
        self.data = self.get_data["data"]
        self.data["quantity"] = quantity
        self.data["skuId"] = skuId
        request = requests.post(url = self.url,headers = self.headers,data = json.dumps(self.data))

        logger.debug(self.url)
        logger.debug("请求参数：{0}\n响应：{1}".format(self.data, request.text))
        response = request.json()
        return response


    def submitOrder(self,token,userId,submitOrderSkus,noSubmit=True,masterOrderNo="",deductBalance=0,orderActualMoney=0,payWay=1,siteCode= "en_US"):
        """下单，
        """
        self.get_data = pcdata.submitOrder
        self.url = base_yaml.get_data("pc","host") + self.get_data["path"]
        self.headers = {
                    "Access-Token": token,
                    "Content-Type": "application/json;charset=UTF-8",
                    "User-Id": userId,
                    "System-Port": "1",
                    "Flow-Sourcet": "0",
                    "Accept-Language": "en_US",
                    "Site-Code": siteCode,
                    # "x-Forwarded-For": "69.212.22.214"
                }
        self.data = self.get_data["data"]
        self.data["noSubmit"] = noSubmit
        self.data["submitOrderSkus"] = submitOrderSkus

        if masterOrderNo != "":
            self.data["masterOrderNo"]=masterOrderNo
            self.data["payWay"] = payWay
            self.data["orderActualMoney"] = orderActualMoney
            self.data["deductBalance"] = deductBalance

        request = requests.post(url = self.url,headers = self.headers,data = json.dumps(self.data))

        logger.debug(self.url)
        logger.info("请求参数：{0}\n响应：{1}".format(json.dumps(self.data,ensure_ascii=False), request.text))
        response = request.json()
        if noSubmit == True :
            return response["data"]["masterOrderNo"],response["data"]["orderActualMoney"]
        else:
            return response["data"]["orderNos"]


    def memberLottery(self,token,userId,lotteryId,usePoints="false"):
        """抽奖
        """
        self.get_data = pcdata.lottery_memberLottery
        self.url = base_yaml.get_data("pc", "host") + self.get_data["path"]
        self.headers = {
            "Access-Token": token,
            "Content-Type": "application/json;charset=UTF-8",
            "User-Id": userId,
            "System-Port": "0",
            "Flow-Sourcet": "0",
            "Accept-Language": "en_US",
            "X-Forwarded-For":"",
        }
        self.data = self.get_data["data"]
        self.data['lotteryId'] = lotteryId
        self.data['usePoints'] = usePoints
        request = requests.post(url=self.url, headers=self.headers, data=json.dumps(self.data))

        # logger.debug(self.url)
        # logger.debug("请求参数：{0}\n响应：{1}".format(self.data, request.text))
        response = request.json()
        try:
            result=response["data"]["prizeName"]
            logger.debug(response["data"]["prizeName"])
            logger.info(response["data"]["prizeName"])
            return response["data"]["prizeName"]
        except Exception as e:
            # logger.error(e)
            logger.error(response)





    def getLotteryMembers(self,token,userId,lotteryId):
        """查询用户抽奖信息
        """
        self.get_data = pcdata.lottery_getLotteryMembers
        self.url = base_yaml.get_data("pc", "host") + self.get_data["path"]
        self.headers = {
            "Access-Token": token,
            "Content-Type": "application/json;charset=UTF-8",
            "User-Id": userId,
            "System-Port": "0",
            "Flow-Sourcet": "0",
            "Accept-Language": "en_US",
        }
        self.data = self.get_data["data"]
        self.data['lotteryId'] = lotteryId
        request = requests.post(url=self.url, headers=self.headers, data=json.dumps(self.data))
        response = request.json()
        logger.info(response)
        return response


    def buyLotteryNum(self,token,userId,lotteryId):
        """购买抽奖机会
        """
        self.get_data = pcdata.lottery_buyLotteryNum
        self.url = base_yaml.get_data("pc", "host") + self.get_data["path"]
        self.headers = {
            "Access-Token": token,
            "Content-Type": "application/json;charset=UTF-8",
            "User-Id": userId,
            "System-Port": "1",
            "Flow-Sourcet": "0",
            "Accept-Language": "en_US",
        }
        self.data = self.get_data["data"]
        self.data['lotteryId'] = lotteryId
        request = requests.post(url=self.url, headers=self.headers, data=json.dumps(self.data))
        response = request.json()
        logger.info(response)
        return response




    def createQuestion(self,token,userId,productCode):
        """创建回答问题
        """
        admin_token, admin_userId = Admin().adminLogin(username="huanghai", password="17f711ffa7869410fbb8edfcb5f08167")
        productMsg = Admin().productListPage(admin_token,admin_userId,productCode)
        print("----------------------------%s"%productMsg)
        self.get_data = pcdata.createQuestion
        self.url = base_yaml.get_data("pc", "host") + self.get_data["path"]
        self.headers = {
            "Access-Token": token,
            "Content-Type": "application/json;charset=UTF-8",
            "X-Forwarded-For":"107.155.5.35",
            "User-Id": userId,
            "System-Port": "0",
            "Flow-Sourcet": "0",
            "Accept-Language": "en_US",
        }
        self.data = self.get_data["data"]
        self.data['productId'] = productMsg['id']
        self.data['productImages'] = productMsg['productImage']
        self.data['productName'] = productMsg['productName']
        self.data['productCode'] = productCode
        request = requests.post(url=self.url, headers=self.headers, data=json.dumps(self.data))
        response = request.json()
        logger.debug(self.data)
        logger.info(response)
        return response

    def getProductId(self, productCode,siteCode):
        """根据productCode返回productId
        """
        admin_token, admin_userId = Admin().adminLogin(username="huanghai", password="dad9e82a80a5f8f6dd71d9375814f620")
        productMsg = Admin().productListPage(admin_token, admin_userId, productCode,siteCode)
        logger.debug(productMsg)
        return productMsg['skuList'][0]['id']




if __name__ == '__main__':

    pc = PC()
    token, userId = pc.pcLogin(username="314221719@qq.com", password="a123456")
    print(token)
    # lotteryId="1589902252424011777"
    # # # #注册
    # # # for i in range(2000,2100):
    # # #     account="auto%s@qq.com"%i
    # # #     pc.register(account=account,password="a123456")
    # #
    # for i in range(100,101):
    #     username="auto%s@qq.com"%i
    #     token, userId = pc.pcLogin(username=username, password="a123456")
    #     #查询用户抽奖信息
    #     pc.getLotteryMembers(token, userId, lotteryId=lotteryId)
    #     # #购买抽奖机会
    #     for i in range(10):
    #         pc.buyLotteryNum(token, userId, lotteryId=lotteryId)
    #
    #     #抽奖
    #     for i in range(1):
    #         res=pc.memberLottery(token,userId,lotteryId=lotteryId)
    #
    # pc.joinShoppingCart(userId=userId,token=token)
    # masterOrderNo,orderActualMoney=pc.submitOrder(token=token,userId=userId,noSubmit=True,skuId = "1601165937875152897")
    # pc.submitOrder(token=token,userId=userId,noSubmit=False,masterOrderNo=masterOrderNo,orderActualMoney=orderActualMoney)
    # res=pc.createQuestion(token=token,userId=userId,productCode = 4002)
    res=pc.getProductId(4002)
    print(res)

