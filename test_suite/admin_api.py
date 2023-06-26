import requests
from common.base.handle_yaml import HandleYaml
from data import admindata
import json,time
from common.base.handle_mysql import HandleMysql
import importlib,sys
from logs.log import logger
from common.tool.aes import *

importlib.reload(sys)

base_yaml = HandleYaml("conf/base.yaml")
do_mysql = HandleMysql()

class Admin:

    def adminLogin(self,username=None,password=None):
        """后台登录接口
        """
        self.get_data = admindata.admin_login
        self.url = base_yaml.get_data("admin","login_url") + self.get_data["path"]
        self.headers = {"Content-Type": "application/json"}
        self.data = self.get_data["data"]
        if username is None or password is None:
            self.data = self.get_data["data"]
        else:
            self.data['username'] = username
            self.data['password'] = password
        request = requests.post(url = self.url,headers = self.headers,data = json.dumps(self.data))
        response = request.json()
        logger.debug(self.url)
        logger.debug("请求参数：{0}\n响应：{1}".format(self.data, response))
        return response['data']['accessToken'], response['data']['userId']


    def webClassSave(self,token,userId,clasName = None ,level = None, parentId=None,siteCode="en_US"):
        """新增前台类目
        """
        self.get_data = admindata.webClass_saveOrUpdate
        self.url = base_yaml.get_data("admin","host") + self.get_data["path"]
        self.headers = {
                    "Access-Token": token,
                    "Content-Type": "application/json;charset=UTF-8",
                    "User-Id": userId,
                    "Accept-Language": "zh_CN"
                }
        self.data = self.get_data["data"]

        self.data['className'] = clasName
        self.data['level'] = level
        self.data['siteCode'] = siteCode
        self.data['parentId'] = parentId
        # if level == 1:
        #     self.data['parentId'] = 0
        # else:
        #     self.data['parentId'] = parentId

        print(self.url)
        print(self.headers)
        request = requests.post(url = self.url,data = json.dumps(self.data),headers = self.headers)
        response = request.json()
        print("请求参数：{0}\n响应：{1}".format(json.dumps(self.data), response))

    def webClassDisable(self,token,userId,id):
        """禁用前台类目
        """
        self.get_data = admindata.webClass_disable
        self.url = base_yaml.get_data("admin","host") + self.get_data["path"]
        self.headers = {
                    "Access-Token": token,
                    "Content-Type": "application/json;charset=UTF-8",
                    "User-Id": userId,
                    "Accept-Language": "zh_CN"
                }
        self.data = self.get_data["data"]
        self.data["id"]=id
        print(self.url)
        print(self.headers)
        request = requests.post(url = self.url,params = self.data,headers = self.headers)
        response = request.json()
        print("请求参数：{0}\n响应：{1}".format(json.dumps(self.data), response))

    def webClassEnable(self,token,userId,id):
        """启用前台类目
        """
        self.get_data = admindata.webClass_enable
        self.url = base_yaml.get_data("admin","host") + self.get_data["path"]
        self.headers = {
                    "Access-Token": token,
                    "Content-Type": "application/json;charset=UTF-8",
                    "User-Id": userId,
                    "Accept-Language": "zh_CN"
                }
        self.data = self.get_data["data"]
        self.data["id"]=id
        print(self.url)
        print(self.headers)
        request = requests.post(url = self.url,params = self.data,headers = self.headers)
        response = request.json()
        print("请求参数：{0}\n响应：{1}".format(json.dumps(self.data), response))

    def getWebClassId(self,className,siteCode):
        """通过名称查询前台类目id
        """
        sql="select id from `smallrig-mall-product`.web_class where class_name = %s and type=1 and  site_code = %s order by create_time desc"
        result = do_mysql.get_data(sql,args=(className,siteCode))
        if result:
            return result['id']
        else:
            return ""

    def getWebClass_name(self,className,siteCode):
        """通过名称判断类目是否存在
        """
        sql="select class_name from `smallrig-mall-product`.web_class where type=1 and class_name = '%s' and site_code = '%s' order by create_time desc"%((className,siteCode))
        result = do_mysql.get_data(sql,)
        print(sql)
        print(result)
        if result:
            return True
        else:
            return False

    def webNavClassSave(self,token,userId,clasName = None ,level = None, parentId=None,siteCode="en_US"):
        """新增前台导航
        """
        self.get_data = admindata.webNavClass_saveOrUpdate
        self.url = base_yaml.get_data("admin","host") + self.get_data["path"]
        self.headers = {
                    "Access-Token": token,
                    "Content-Type": "application/json;charset=UTF-8",
                    "User-Id": userId,
                    "Accept-Language": "zh_CN"
                }
        self.data = self.get_data["data"]

        self.data['className'] = clasName
        self.data['level'] = level
        self.data['siteCode'] = siteCode
        self.data['parentId'] = parentId
        print(self.url)
        print(self.headers)
        request = requests.post(url = self.url,data = json.dumps(self.data),headers = self.headers)
        response = request.json()
        print("请求参数：{0}\n响应：{1}".format(json.dumps(self.data), response))

    def webNavClassEnable(self,token,userId,id):
        """启用前台导航
        """
        self.get_data = admindata.webNavClass_enable
        self.url = base_yaml.get_data("admin","host") + self.get_data["path"]
        self.headers = {
                    "Access-Token": token,
                    "Content-Type": "application/json;charset=UTF-8",
                    "User-Id": userId,
                    "Accept-Language": "zh_CN"
                }
        self.data = self.get_data["data"]
        self.data["id"]=id
        print(self.url)
        print(self.headers)
        request = requests.post(url = self.url,params = self.data,headers = self.headers)
        response = request.json()
        print("请求参数：{0}\n响应：{1}".format(json.dumps(self.data), response))

    def getwebNavClassClassId(self,className,siteCode="en_US"):
        """通过名称查询前台导航id
        """
        sql="select id from `smallrig-mall-product`.web_nav_class where class_name = %s and type=1 and site_code = %s order by create_time desc"
        result = do_mysql.get_data(sql,args=(className,siteCode))
        print(result)
        if result:
            return result['id']
        else:
            return ""

    def getwebNavClass_name(self,className,siteCode="en_US"):
        """通过名称判断前台导航是否存在
        """
        sql="select class_name from `smallrig-mall-product`.web_nav_class where type=1 and class_name = %s and site_code = %s order by create_time desc"
        result = do_mysql.get_data(sql,args=(className,siteCode))
        if result:
            return True
        else:
            return False


    def orderCreateDeliver(self,token,userId,skuId,thirdpartySkuCode,deliverNo,deliverTime,logisticsNo,orderNo):
        """创建发货单
        """
        self.get_data = admindata.order_createDeliver
        self.url = base_yaml.get_data("admin","open_api_url") + self.get_data["path"]
        self.headers = {
                    "Access-Token": token,
                    "Content-Type": "application/json;charset=UTF-8",
                    "User-Id": userId,
                    "Accept-Language": "zh_CN"
                }
        self.data = self.get_data["data"]
        self.data["skuId"]=skuId
        self.data["thirdpartySkuCode"]=thirdpartySkuCode
        self.data["deliverNo"]=deliverNo
        self.data["deliverTime"]=deliverTime
        self.data["logisticsNo"]=logisticsNo
        self.data["orderNo"]=orderNo

        print("----------------------------")
        print(json.dumps(self.data))
        self.data=encrypt(json.dumps(self.data))
        print(self.url)
        print(self.headers)
        print(self.data.decode('utf-8'))
        print(decrypt(self.data))
        request = requests.post(url = self.url,params = self.data.decode('utf-8'),headers = self.headers)
        print(request.text)
        response = request.json()
        print("请求参数：{0}\n响应：{1}".format(json.dumps(self.data), response))



    def webClassDisable(self,token,userId,id):
        """禁用前台类目
        """
        self.get_data = admindata.webClass_disable
        self.url = base_yaml.get_data("admin","host") + self.get_data["path"]
        self.headers = {
                    "Access-Token": token,
                    "Content-Type": "application/json;charset=UTF-8",
                    "User-Id": userId,
                    "Accept-Language": "zh_CN"
                }
        self.data = self.get_data["data"]
        self.data["id"]=id
        print(self.url)
        print(self.headers)
        request = requests.post(url = self.url,params = self.data,headers = self.headers)
        response = request.json()
        print("请求参数：{0}\n响应：{1}".format(json.dumps(self.data), response))


    def saveOrUpdateBlog(self,token,userId,blog_url,blogName):
        """新增博客
        """
        self.get_data = admindata.blog_saveOrUpdateBlog
        self.url = base_yaml.get_data("admin","host") + self.get_data["path"]
        self.headers = {
                    "Access-Token": token,
                    "Content-Type": "application/json;charset=UTF-8",
                    "User-Id": userId,
                    "Accept-Language": "zh_CN"
                }
        self.data = self.get_data["data"]
        self.data["blogName"]=blogName
        self.data["url"]=blog_url
        print(self.url)
        print(self.headers)
        request = requests.post(url = self.url,data = json.dumps(self.data),headers = self.headers)
        response = request.json()
        print("请求参数：{0}\n响应：{1}".format(json.dumps(self.data), response))

    def saveCouponInfo(self,token,userId,type,couponName,couponRule,satisfyMoney=None,deductionMoney=None,discount=None):
        """保存优惠券
           couponRule ： 0 满减    1 折扣  2 兑换  3 兑换运费
           type : 优惠券类型C-1-商品券，C-2兑换券，C-3运费券
           satisfyMoney   使用门槛
           deductionMoney  抵扣金额
           discount    打折
        """
        self.get_data = admindata.couponInfo_saveCouponInfo
        self.url = base_yaml.get_data("admin","host") + self.get_data["path"]
        self.headers = {
                    "Access-Token": token,
                    "Content-Type": "application/json;charset=UTF-8",
                    "User-Id": userId,
                    "Accept-Language": "zh_CN"
                }
        self.data = self.get_data["data"]
        self.data['couponName'] = couponName
        self.data['satisfyMoney'] = satisfyMoney
        self.data['couponRule'] = couponRule
        self.data['type'] = type
        if couponRule == 0:
            self.data['deductionMoney'] = deductionMoney
        elif couponRule == 1:
            self.data['discount'] = discount
        elif couponRule ==2:
            self.data["activitySkuDTO"]["skuIds"]["allGoods"] = 0
            self.data["activitySkuDTO"]["skuIds"]["contains"] = 1
        elif couponRule == 3:
            self.data['type'] = "C-3"

        logger.info("优惠券名称 ："+couponName)
        logger.debug(self.url)
        logger.debug(self.headers)
        request = requests.post(url = self.url,data = json.dumps(self.data),headers = self.headers)
        response = request.json()
        logger.debug("请求参数：{0}\n响应：{1}".format(json.dumps(self.data,ensure_ascii=False), response))

    def editCouponInfoStatus(self,token,userId,id):
        """启用优惠券
        """
        self.get_data = admindata.couponInfo_editCouponInfoStatus
        self.url = base_yaml.get_data("admin","host") + self.get_data["path"]
        self.headers = {
                    "Access-Token": token,
                    "Content-Type": "application/json;charset=UTF-8",
                    "User-Id": userId,
                    "Accept-Language": "zh_CN"
                }
        self.data = self.get_data["data"]
        self.data["id"]=id
        logger.debug(self.url)
        logger.debug(self.headers)
        request = requests.post(url = self.url,data = json.dumps(self.data),headers = self.headers)
        response = request.json()
        logger.debug("请求参数：{0}\n响应：{1}".format(json.dumps(self.data), response))

    def queryCouponInfoList(self,token,userId,couponName,type):
        """查询优惠券
        """
        self.get_data = admindata.couponInfo_queryCouponInfoList
        self.url = base_yaml.get_data("admin","host") + self.get_data["path"]
        self.headers = {
                    "Access-Token": token,
                    "Content-Type": "application/json;charset=UTF-8",
                    "User-Id": userId,
                    "Accept-Language": "zh_CN"
                }
        self.data = self.get_data["data"]
        self.data["couponName"]=couponName
        self.data["type"]=type
        logger.debug(self.url)
        logger.debug(self.headers)
        request = requests.post(url = self.url,data = json.dumps(self.data),headers = self.headers)
        response = request.json()
        logger.debug("请求参数：{0}\n响应：{1}".format(json.dumps(self.data), response))
        logger.info("优惠ID ："+str(response["data"]["records"][0]["id"]))
        return response["data"]["records"][0]["id"]

    def memberInfoList(self,token,userId,account):
        """查询会员ID
        """
        self.get_data = admindata.couponInfo_queryCouponInfoList
        self.url = base_yaml.get_data("admin","host") + self.get_data["path"]
        self.headers = {
                    "Access-Token": token,
                    "Content-Type": "application/json;charset=UTF-8",
                    "User-Id": userId,
                    "Accept-Language": "zh_CN"
                }
        self.data = self.get_data["data"]
        self.data["account"]=account
        logger.debug(self.url)
        logger.debug(self.headers)
        request = requests.post(url = self.url,data = json.dumps(self.data),headers = self.headers)
        response = request.json()
        logger.debug("请求参数：{0}\n响应：{1}".format(json.dumps(self.data), response))
        return response["data"]["records"][0]["id"]


    def generateCouponCodes(self,token,userId,couponInfoId,memberEmail,memberId):
        """根据用户生成券码
        """
        self.get_data = admindata.couponPool_generateCouponCodes
        self.url = base_yaml.get_data("admin","host") + self.get_data["path"]
        self.headers = {
                    "Access-Token": token,
                    "Content-Type": "application/json;charset=UTF-8",
                    "User-Id": userId,
                    "Accept-Language": "zh_CN"
                }
        self.data = self.get_data["data"]
        self.data["couponInfoId"]=couponInfoId
        self.data["memberEmail"]=memberEmail
        self.data["memberId"]=memberId
        logger.debug(self.url)
        logger.debug(self.headers)
        request = requests.post(url = self.url,data = json.dumps(self.data),headers = self.headers)
        response = request.json()
        logger.debug("请求参数：{0}\n响应：{1}".format(json.dumps(self.data), response))
        return response

    def queryCouponCodes(self,token,userId,memberEmail,couponInfoId):
        """根据用户生成券码
        """
        self.get_data = admindata.couponPool_queryCouponCodes
        self.url = base_yaml.get_data("admin","host") + self.get_data["path"]
        self.headers = {
                    "Access-Token": token,
                    "Content-Type": "application/json;charset=UTF-8",
                    "User-Id": userId,
                    "Accept-Language": "zh_CN"
                }
        self.data = self.get_data["data"]
        self.data["couponInfoId"]=couponInfoId
        self.data["memberEmail"]=memberEmail
        logger.debug(self.url)
        logger.debug(self.headers)
        request = requests.post(url = self.url,data = json.dumps(self.data),headers = self.headers)
        response = request.json()
        logger.info(response["data"]["records"][0]['couponCode'])
        # for i in response["data"]["records"]:
        #     logger.info(i['couponCode'])
        logger.debug("请求参数：{0}\n响应：{1}".format(json.dumps(self.data), response))
        return response

    def productListPage(self,token,userId,thirdpartySkuCode):
        """查询商品信息
        """
        self.get_data = admindata.product_listPage
        self.url = base_yaml.get_data("admin","host") + self.get_data["path"]
        self.headers = {
                    "Access-Token": token,
                    "Content-Type": "application/json;charset=UTF-8",
                    "User-Id": userId,
                    "Accept-Language": "zh_CN"
                }
        self.data = self.get_data["data"]
        self.data["thirdpartySkuCode"]=str(thirdpartySkuCode)
        logger.debug(self.url)
        logger.debug(self.headers)
        request = requests.post(url = self.url,data = json.dumps(self.data),headers = self.headers)
        response = request.json()
        logger.debug("请求参数：{0}\n响应：{1}".format(json.dumps(self.data), json.dumps(response,ensure_ascii=False)))
        for i in response['data']['records']:
            if i['productCode'] == str(thirdpartySkuCode) :
                logger.info(i)
                return i

        return response


    def getByOrderNo(self,token,userId,orderNo):
        """获取发货所需的商品信息
        """
        self.get_data = admindata.get_by_order_no
        self.url = base_yaml.get_data("admin", "host") + self.get_data["path"]
        self.headers = {
            "Access-Token": token,
            "Content-Type": "application/json;charset=UTF-8",
            "User-Id": userId,
            "Accept-Language": "zh_CN"
        }
        self.data = self.get_data["data"]
        self.data["orderNo"] = orderNo
        logger.debug(self.url)
        logger.debug(self.headers)
        res = requests.post(url=self.url, data=json.dumps(self.data), headers=self.headers)
        logger.debug(self.data)
        logger.debug(self.headers)
        logger.debug(res.text)
        res = res.json()
        orderDelverSkuList=[]
        for i in res['data']['orderSku'] :
            orderDelverSkuList.append({"count": i['buyCount'], "skuId": i['skuId'], "orderSkuType": i['orderSkuType'], "thirdpartySkuCode": i['thirdpartySkuCode']})
        return orderDelverSkuList

    def createDeliver(self,token,userId,orderNo,orderDelverSkuList,logisticsNo,logisticsCode='USPS',warehouseCode='warehouseCode'):
        """创建发货单
        """
        self.get_data = admindata.create_deliver
        self.url = base_yaml.get_data("admin", "host") + self.get_data["path"]
        self.headers = {
            "Access-Token": token,
            "Content-Type": "application/json;charset=UTF-8",
            "User-Id": userId,
            "Accept-Language": "zh_CN"
        }
        self.data = self.get_data["data"]
        self.data["orderNo"] = orderNo
        self.data["createOrderDelverSkuList"] = orderDelverSkuList
        self.data["logisticsNo"] = logisticsNo
        self.data["logisticsCode"] = logisticsCode
        self.data["warehouseCode"] = warehouseCode
        logger.debug(self.url)
        logger.debug(self.headers)
        logger.debug(self.data)
        res = requests.post(url=self.url, data=json.dumps(self.data), headers=self.headers)
        logger.debug(res.text)
        res = res.json()
        return res

    def cancelOrder(self,token,userId,orderNo):
        """后台取消订单
        """
        self.get_data = admindata.cancel_order
        self.url = base_yaml.get_data("admin", "host") + self.get_data["path"]
        self.headers = {
            "Access-Token": token,
            "Content-Type": "application/json;charset=UTF-8",
            "User-Id": userId,
            "Accept-Language": "zh_CN"
        }
        self.data = self.get_data["data"]
        self.data["orderNo"] = orderNo
        logger.debug(self.url)
        logger.debug(self.headers)
        logger.debug(self.data)
        res = requests.post(url=self.url, data=json.dumps(self.data), headers=self.headers)
        logger.debug(res.text)
        res = res.json()
        return res

    def query_order_pay(self,token,userId,orderNo):
        """后台线下确认收款
        """
        self.get_data = admindata.queryOrderPayPage
        self.url = base_yaml.get_data("admin", "host") + self.get_data["path"]
        self.headers = {
            "Access-Token": token,
            "Content-Type": "application/json;charset=UTF-8",
            "User-Id": userId,
            "Accept-Language": "zh_CN"
        }
        self.data = self.get_data["data"]
        self.data["orderNo"] = orderNo
        logger.debug(self.url)
        logger.debug(self.headers)
        logger.debug(self.data)
        res = requests.post(url=self.url, data=json.dumps(self.data), headers=self.headers)
        logger.debug(res.text)
        res = res.json()
        logger.debug(res['data']['records'][0]['id'])
        return res['data']['records'][0]['id']

    def confirm_payment(self,token,userId,id):
        """后台线下确认收款
        """
        self.get_data = admindata.confirmThePayment
        self.url = base_yaml.get_data("admin", "host") + self.get_data["path"]
        self.headers = {
            "Access-Token": token,
            "Content-Type": "application/json;charset=UTF-8",
            "User-Id": userId,
            "Accept-Language": "zh_CN"
        }
        self.data = self.get_data["data"]
        self.data["id"] = id
        logger.debug(self.url)
        logger.debug(self.headers)
        logger.debug(self.data)
        res = requests.post(url=self.url, data=json.dumps(self.data), headers=self.headers)
        logger.debug(res.text)
        res = res.json()
        return res


if __name__ == '__main__':
    admin = Admin()
    token,userId = admin.adminLogin(username="huanghai",password="dad9e82a80a5f8f6dd71d9375814f620")
    # couponName ="满10-1 002"
    # #保存优惠券
    # # admin.saveCouponInfo(token,userId,couponName,couponRule=0,satisfyMoney=10000,deductionMoney=8000)
    # admin.saveCouponInfo(token,userId,couponName,couponRule=0,satisfyMoney=10000,discount=75)
    # #查询保存的优惠券ID
    # coupon_id = admin.queryCouponInfoList(token,userId,couponName)
    # #启用优惠券
    # admin.editCouponInfoStatus(token,userId,coupon_id)
    # #查询会员ID
    # account="314221719@qq.com"
    # memberId=admin.memberInfoList(token,userId,account=account)
    # #根据用户生成券码
    # admin.generateCouponCodes(token,userId,coupon_id,account,memberId)
    # #根据用户查询券码
    # admin.queryCouponCodes(token,userId,account,coupon_id)
    # admin.productListPage(token,userId,3667)
    admin.query_order_pay(token,userId,230626021325280903)
    admin.confirm_payment(token,userId,1673152463085678593)





