import unittest
import datetime,time,random
import requests
import json
import concurrent.futures
import importlib,sys
import pymysql
importlib.reload(sys)


import logging #导入日志模块
log = logging.getLogger() #创建日志器
log.setLevel(logging.DEBUG) #设置日志的打印级别
# fh = logging.FileHandler(filename="../logs/log.log",mode='a',encoding="utf-8") #创建日志处理器，用文件存放日志
sh = logging.StreamHandler()#创建日志处理器，在控制台打印
#创建格式器，指定日志的打印格式
fmt = logging.Formatter("[%(asctime)s]-[%(levelname)s]-[%(filename)s]-[Line:%(lineno)d]-[Msg:%(message)s]")
fmt = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
#给处理器设置格式
# fh.setFormatter(fmt=fmt)
sh.setFormatter(fmt=fmt)
#给日志器添加处理器
# logg.addHandler(fh)
log.addHandler(sh)



class Order(unittest.TestCase):




    def setUp(self,env='uat'):
        log.info('start {}'.format(self))
        log.info(f"当前执行环境： {env}")
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
            self.xxl_url = 'https://bereal.smallrig.net'
            self.connection = pymysql.connect(host='192.168.133.233',  # 数据库地址
                                              user='root',  # 数据库用户名
                                              password='Leqi!2022',  # 数据库密码
                                              db='smallrig-platform')  # 数据库名称
            self.cursor = self.connection.cursor()
        accessToken, userId = self.zt_login(env=self.env)
        self.oms_headers={"Content-Type":"application/json;charset=UTF-8","System-Code":"ERP","Access-Token":accessToken,"User-Id":userId}


    def tearDown(self):
        self.cursor.close()
        self.connection.close()

    def query(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

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

    def zt_login(self, username="huanghai",password="17f711ffa7869410fbb8edfcb5f08167",env='test'):
        """业务中台登录
        """
        log.info("登录业务中台")
        uri = "/API/manage/login"
        url = self.urls + uri
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "system-code": "XTZX",
        }
        if env == 'uat':
            headers['system-code'] = 'XTZX_MAIN'
            username = "huanghai"
            password = "dad9e82a80a5f8f6dd71d9375814f620"
            # password = "17f711ffa7869410fbb8edfcb5f08167"
        data = {"systemCode": "XTZX", "username": username, "password": password,
                    "_t": int(time.time() * 1000)}
        log.debug(url)
        log.debug(data)
        res = requests.post(url=url, data=json.dumps(data), headers=headers)
        log.debug(res.json())
        return res.json()["data"]["accessToken"], res.json()["data"]["userId"]



    def add_order(self,channelName,product_list,platformId=53):
        '''提交2c订单'''
        log.info("提交2c订单")
        uri="/API/oms/saleOrder/v1/save"
        res = self.get_market_channel_byId()
        for i in res['data']:
            if i['mcName'] == channelName:
                marketId = i['parentId']
                channelId = i['id']
        product_data_list = []
        for productCode in product_list:
            product_info = self.test_get_product_new(marketId=marketId, channelId=channelId, productCode=productCode)
            product_data = {"productCode":product_info['productCode'],"productId":product_info['productId'],"productStatusName":product_info['productStatusName'],"productStatusId":product_info['productStatusId'],"weight":12,"productName":product_info['productName'],"selectNum":0,"newSelectNum":1,"scale":1,"externalSku":product_info['productCode'],"orderQuantity":3,"productCodeSys":product_info['productCode'],"productNameSys":product_info['productName'],"saleOrderSysItems":[{"orderQuantity":2,"feeRatio":1,"productCode":product_info['productCode'],"productId":product_info['productId'],"productName":product_info['productName'],"productStatusId":product_info['productStatusId'],"productStatusName":product_info['productStatusName'],"scale":1,"weight":12}],"length":1,"price":"2.000","allPrice":"4.000","unitProductPrice":2,"productQuantity":1,"orderSnSource":"","sourceCode":""}
            product_data_list.append(product_data)
        data = {"platformId":platformId,"channelId":channelId,"orderAttribute":1,"payTime":"2023-12-25 19:32:09","showWeight":0.112,"customerMessage":"买家留言","serviceRemark":"客服备注","saleOrderCost":{"paymentProofFile":{"files":[{"name":"23432img-kxAdF1703504096583.pdf","url":"http://smallrig-pmd.oss-cn-shenzhen.aliyuncs.com/23432img-kxAdF1703504096583.pdf"}]},"shippingFee":"","totalFee":"200","otherIncome":0,"isPaid":"","couponFee":"","marketIncome":"","actualShippingCost":"","platformFee":"","otherFee":"","currency":"EUR","platformCoupon":"","useBalance":"","warehouseFee":"","total":"200"},"saleOrderAddress":{"customerId":"GH23432423","customerName":"abe","receiverName":"abe","receiverTel":"18476691641","receiverContinent":"亚洲","receiverCountryCode":"CN","receiverCity":"深圳市","receiverRegion":"南山区","receiverAddress":"龙华区民治街道樟坑2区999_%s","houseNumber":"1020","customerEmail":"2607103304@qq.com","receiverCompany":"深圳乐其","receiverProvince":"广东省","receiverAddress2":"西丽街道波顿科技园2","receiverPostcode":"2500"},"products":product_data_list,"saleOrderItem":product_data_list,"timestamp":1710833772}
        log.debug(self.urls+uri)
        log.debug(data)
        res = requests.post(url = self.urls+uri,json = data ,headers = self.oms_headers)
        log.debug(res.text)
        return res.json()['data']['orderNo']


    def get_order_id(self,orderNo,orderStatus=None):
        '''订单列表-获取数据id'''
        log.info("订单查询")
        uri = '/API/oms/order/v1/list'
        if orderStatus == None:
            data ={"pageSize":15,"pageNum":1,"realTimeType":2,"name":orderNo,"codeType":1,"codeMode":1,}
        else:
            data = {"pageSize": 15, "pageNum": 1, "realTimeType": 2, "name": orderNo, "orderStatus": orderStatus, "codeType": 1, "codeMode": 1, }
        res = requests.post(url=self.urls + uri, json=data, headers=self.oms_headers)
        log.debug(self.urls+uri)
        log.debug(data)
        log.info(res.json())
        try:
            res = res.json().get('data', {}).get('items', [{}])[0].get('id')
        except IndexError:
            log.info("没有找到该订单: %s,休息10秒重新查询"%orderNo)
            time.sleep(10)
            return self.get_order_id(orderNo, orderStatus)
        return res

    def get_order_documentsNo(self, orderNo):
        '''订单列表-获取仓库单号'''
        log.info("订单列表-获取仓库单号")
        uri = '/API/oms/order/v1/list'
        data = {"pageSize": 15, "pageNum": 1, "realTimeType": 2, "name": orderNo, "codeType": 1, "codeMode": 1, }
        res = requests.post(url=self.urls + uri, json=data, headers=self.oms_headers)
        log.debug(self.urls + uri)
        log.debug(data)
        log.info(res.json())
        orderStatus = res.json().get('data', {}).get('items', [{}])[0].get('orderStatus')
        orderCode = res.json().get('data', {}).get('items', [{}])[0].get('orderCode')
        auditRemark = res.json().get('data', {}).get('items', [{}])[0].get('auditRemark')
        auditOpinion = res.json().get('data', {}).get('items', [{}])[0].get('auditOpinion')
        if orderStatus == 3:
            res = res.json().get('data', {}).get('items', [{}])[0].get('tagWarehouseCode')
            return res
        else: raise KeyError(f"订单号：{orderCode} 已转问题件,原因： {auditOpinion}")


    def order_submit(self,orderNo):
        '''发货订单列表-提交操作'''
        log.info("订单提交")
        orderId = self.get_order_id(orderNo)
        uri =  '/API/oms/order/v1/batchSubmit'
        data = {'orderIds': orderId,}
        log.debug(self.urls+uri)
        log.debug(data)
        res = requests.post(url=self.urls + uri, params = data, headers = self.oms_headers)
        log.info(res.json())
        return res.json()


    def getShippingMethod(self,warehouseId=57):
        uri = f'/API/tms/warehouseShipping/v1/getShippingMethod?warehouseId={warehouseId}'
        url =  self.urls+uri
        res = requests.get(url=url, headers=self.oms_headers)
        return res.json()['data']


    def add_apply_order(self,orderType = 18):
        """新增样品赠品单"""
        uri = '/API/oms/giftApplyOrder/v1/save'
        url = self.urls+uri
        data = {"feeDeptId":"422bfe344d115fb3","kingdeeDeptCode":"BM20101","addressVOList":[{"giftApplyId":6408,"giftOrderIndex":1,"receiverName":"1","receiverTel":"1","receiverEmail":"","receiverCompany":"","receiverContinent":"欧洲","receiverCountryCode":"AL","receiverProvince":"","receiverCity":"2","receiverAddress":"1","receiverAddress2":"","houseNumber":"","receiverPostcode":"","delFlag":1,"createBy":"陈白琼","createTime":"2024-11-14 11:34:44","updateBy":"陈白琼","updateTime":"2024-11-14 11:36:35"}],"attachVOList":[],"channelId":88,"combineFee":"","combineType":"","cpm":"","dealerName":"","deductAmount":"","deductRatio":"","diversionObj":"","handleType":"1","infoVOList":[{"activityAddress":"","activityUrl":"","boothArea":"","brandArea":"","combineInfo":"","countryCode":"","dealer":"","demandFee":"","deviceModel":"","fansNum":"","giftOrderIndex":1,"holdPeriod":"","holdTime":"","language":"","otherNote":"","partBrand":"","partNum":"","redTelevision":"","sponsor":"","television":"","backdropIntroduct":"","mediaFlag":"","newDevelopmentFlag":"","socialMediaPlatform":"","standardCpv":"","cpvCurrency":"","expectedCooperationCpv":"","reasonForExceeding":"","tags":"","necessityOfCooperation":"","magnitude":"","clipType":"","clipContent":"","numberOfClips":"","affiliatedActivityOrProject":"","cashNeededFlag":"","cashCostCny":"","trafficPlatform":"","expectedContentReleaseTime":"","necessityOfJoin":"","feishuApprovalNum":"","eventObjective":"","sampleHandlingPlan":"","publicRelationsType":"","publicRelationsNecessity":"","influencerPlatform":"IG","influencerNickname":"1","influencerId":"2","contentGenre":"图文推荐","followerCount":"2","brandType":"","brandName":"","collaborationNecessity":"","collaborationType":"","collaborationGoal":"","applyInfo":"{\"activityAddress\":\"\",\"activityUrl\":\"\",\"boothArea\":\"\",\"brandArea\":\"\",\"combineInfo\":\"\",\"countryCode\":\"\",\"dealer\":\"\",\"demandFee\":\"\",\"deviceModel\":\"\",\"fansNum\":\"\",\"giftOrderIndex\":\"\",\"holdPeriod\":\"\",\"holdTime\":\"\",\"language\":\"\",\"otherNote\":\"\",\"partBrand\":\"\",\"partNum\":\"\",\"redTelevision\":\"\",\"sponsor\":\"\",\"television\":\"\",\"backdropIntroduct\":\"\",\"mediaFlag\":\"\",\"newDevelopmentFlag\":\"\",\"socialMediaPlatform\":\"\",\"standardCpv\":\"\",\"cpvCurrency\":\"\",\"expectedCooperationCpv\":\"\",\"reasonForExceeding\":\"\",\"tags\":\"\",\"necessityOfCooperation\":\"\",\"magnitude\":\"\",\"clipType\":\"\",\"clipContent\":\"\",\"numberOfClips\":\"\",\"affiliatedActivityOrProject\":\"\",\"cashNeededFlag\":\"\",\"cashCostCny\":\"\",\"trafficPlatform\":\"\",\"expectedContentReleaseTime\":\"\",\"necessityOfJoin\":\"\",\"feishuApprovalNum\":\"\",\"eventObjective\":\"\",\"sampleHandlingPlan\":\"\",\"publicRelationsType\":\"\",\"publicRelationsNecessity\":\"\",\"influencerPlatform\":\"IG\",\"influencerNickname\":\"1\",\"influencerId\":\"2\",\"contentGenre\":\"图文推荐\",\"followerCount\":\"2\",\"brandType\":\"\",\"brandName\":\"\",\"collaborationNecessity\":\"\",\"collaborationType\":\"\",\"collaborationGoal\":\"\"}"}],"isOutput":"","isReturn":1,"itemVOList":[{"id":35693,"giftApplyId":6408,"giftOrderIndex":1,"productId":6588,"productCode":"0000","productName":"临时半成品","projectId":"","quantity":1,"unitProductPrice":1,"totalPrice":1,"delFlag":1,"createBy":"陈白琼","createTime":"2024-11-14 11:34:44","updateBy":"陈白琼","updateTime":"2024-11-14 11:34:44"}],"marketId":10,"orderType":"17","outputContent":"","outputTime":"","platformId":44,"remark":"1","returnReceiver":"1","shippingMethod":2,"deptId":"422bfe344d115fb3","deptName":"信息技术部","id":"","orderCode":"","timestamp":1733911533000}
        res = requests.post(url=url ,json=data, headers=self.oms_headers)
        log.info("新增样品赠品单")
        log.info(res.json())
        return res.json()
    def test_add_apply_order(self):
        self.add_apply_order()
        # time.sleep(1)
        if self.env == 'uat':
            #同步钉钉状态
            self.do_job(418)
            time.sleep(2)
            self.do_job(301)
        elif self.env == 'test':
            #同步飞书状态
            self.do_job(602)
            time.sleep(3)
            #【样品/赠品单】申请单提交生成销售赠品单
            self.do_job(301)
            time.sleep(3)
            #提交下推订单


    def order_audit(self,orderNo,warehouseName,expressTypeName,orderStatus=2):
        '''2c发货订单列表-审单操作'''
        log.info("订单审核")
        orderId = self.get_order_id(orderNo,orderStatus = orderStatus)
        uri = '/API/oms/order/v1/audit'
        warehouse_info =  self.get_warehouse_info(warehouseName=warehouseName)
        warehouseId = warehouse_info['id']
        shippingMethod =self.getShippingMethod(warehouseId=warehouseId)
        for i in shippingMethod:
            if expressTypeName == i['name']:

                data = {"warehouseId": warehouseId, "logistics": i['code'], "hasMagento": False,"showReceiverRegion": False, "expressType": i['code'], "expressTypeName": i['name'],"ids": ["%s"%orderId],}
        res = requests.post(url=self.urls + uri, json=data, headers=self.oms_headers)
        log.debug(self.urls+uri)
        log.debug(data)
        log.info(res.text)
        return res.json()

    def job_login(self):
        uri = '/smallrig-job-admin/login'
        url = self.xxl_url+uri
        if self.env == 'test':
            data  = {"userName":"admin","password":"smallrig#321"}
        elif self.env == 'uat':
            data = {"userName": "admin", "password": "smallrig#321"}
            log.info(url)
            log.info(data)
        headers = {"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8","X-Requested-With":"XMLHttpRequest"}
        res = requests.post(url=url, params=data, headers=headers)
        log.info(res.headers)
        return res.headers["Set-Cookie"]



    def do_job(self,id):
        """执行定时任务"""
        log.info("执行定时任务")
        uri="/smallrig-job-admin/jobinfo/trigger"
        url = self.xxl_url + uri
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": self.job_login(),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        data = {"id": id,"executorParam": "","addressList": "" }
        res = requests.post(url, headers=headers, data=data)
        log.debug(url)
        log.debug(data)
        log.info(res.json())
        return res.json()

    def queryDocumentDistributionPage(self,documentsNos):
        """获取仓库仓号
        """
        log.info("获取仓库仓号")
        uri = '/API/wms/document-distribution/v1/queryDocumentDistributionPage'
        data = {"pageSize":50,"pageNum":1,"orderCode":"","skuTypeCountCriteriaValue":"","outOfStockMark":"","orderTag":2,"statusList":[2],"warehouseId":"","warehouseIds":[],"mode":"","logisticsServices":None,"shippingIds":None,"distributionType":"","customerServiceRemarksFlag":"","documentsNos":documentsNos,"totalWeightBegin":"","totalWeightEnd":"","marketId":"","channelId":"","skuCode":"","skuCountCriteria":"","skuCountCriteriaValue":"","skuTypeCountCriteria":"","timeType":1,"orderTimeArr":[],"createTimeBegin":"2023-11-27 00:00:00","createTimeEnd":"2056-12-27 23:59:59","createTimeArr":["2023-11-27 00:00:00","2056-12-27 23:59:59"],"referenceNo":"","receiverCountryCode":"","trackingNumber":"","receiverName":""}
        url = self.urls+uri
        res =  requests.post(url=url,json = data , headers = self.oms_headers)
        log.debug(url)
        log.debug(data)
        log.info(res.text)
        return res.json()['data']['records'][0]['id']


    def get_tagWarehouseCode(self,documentsNos):
        '''2c已分配配货列表-获取数据id'''
        time.sleep(3)
        log.info("查询2c已分配配货单数据ID")
        uri = '/API/wms/document-distribution/v1/queryDocumentDistributionPage'
        data = {"pageSize":50,"pageNum":1,"orderCode":"","skuTypeCountCriteriaValue":"","outOfStockMark":"","orderTag":2,"statusList":[2],"warehouseId":"","warehouseIds":[],"mode":"","logisticsServices":None,"shippingIds":None,"distributionType":"","customerServiceRemarksFlag":"","documentsNos":documentsNos,"totalWeightBegin":"","totalWeightEnd":"","marketId":"","channelId":"","skuCode":"","skuCountCriteria":"","skuCountCriteriaValue":"","skuTypeCountCriteria":"","timeType":1,"orderTimeArr":[],"createTimeBegin":"2023-11-27 00:00:00","createTimeEnd":"2056-12-27 23:59:59","createTimeArr":["2023-11-27 00:00:00","2056-12-27 23:59:59"],"referenceNo":"","receiverCountryCode":"","trackingNumber":"","receiverName":""}
        res = requests.post(url=self.urls + uri, json=data, headers=self.oms_headers)
        log.info(res.text)
        return res.json()['data']['records'][0]['id']

    def DistributionLowerShelf(self,documentsNos):
        """下架
        """
        log.info("下架")
        xj_id = self.queryDocumentDistributionPage(documentsNos)
        uri = '/API/wms/document-distribution/v1/DistributionLowerShelf'
        data =  {"userPosition":"","distributionUser":"袁浩","ids":[xj_id],"mode":1}
        url = self.urls+uri
        res =  requests.post(url=url,json = data , headers = self.oms_headers)
        log.info(res.text)
        return res.json()

    def startPick(self,documentsNo):
        """开始拣货
        """
        log.info("开始拣货")
        uri = '/API/wms/documentsPick/v1/startPick'
        url = self.urls+uri
        data = {"actualPicker": "张森锋", "documentsNo": "", "documentsDistributionNo": documentsNo}
        res = requests.post(url=url, json=data, headers=self.oms_headers)
        log.info(res.text)
        return res.json()

    def finishPick(self,documentsNo):
        """完成拣货确认
        """
        log.info("完成拣货确认")
        uri = '/API/wms/documentsPick/v1/finishPick'
        url = self.urls+uri
        data = {"actualPicker": "张森锋", "documentsNo": "", "documentsDistributionNo": documentsNo}
        res = requests.post(url=url, json=data, headers=self.oms_headers)
        log.info(res.text)
        return res.json()

    def get_warehouse_info(self,warehouseName=None,warehouseId=None ):
        """根据仓库名称，返回仓库ID
        """
        uri = '/API/basics/warehouse/v1/queryAuthWarehouse?status=1'
        url = self.urls + uri
        res = requests.get(url=url, headers=self.oms_headers)
        for i in res.json()['data']:
            if warehouseName != None:
                if i['warehouseName'] == warehouseName :
                    return i
            if warehouseId != None:
                if int(i['id']) == int(warehouseId):
                    return i


    def test_0001(self):
        a=self.get_warehouse_info(warehouseName='中国深圳直发仓')
        log.debug(a)
        b= self.get_warehouse_info(warehouseId=57)
        log.debug(b)
    def get_product(self,productCode,warehouseName=None,warehouseId=None):
        """查询商品信息
        """
        log.info("查询商品信息")
        uri = '/API/sku/product/v1/selectAllv2'
        url = self.urls + uri
        if warehouseName != None:
            warehouseId = self.get_warehouse_info(warehouseName)['id']
            data = {"pageSize":15,"pageNum":1,"warehouseId":warehouseId,"name":productCode,"timestamp":1710470052000}
            res = requests.post(url=url, json=data, headers=self.oms_headers)
            for i in res.json()['data']['items']:
                if str(i['productCode']) == str(productCode):
                    return i
        if warehouseId != None:
            data = {"pageSize":15,"pageNum":1,"warehouseId":warehouseId,"name":productCode,"timestamp":1710470052000}
            res = requests.post(url=url, json=data, headers=self.oms_headers)
            for i in res.json()['data']['items']:
                if str(i['productCode']) == str(productCode):
                    return i

    def test_get_product_new(self,marketId,channelId,productCode='1112'):
        """查询商品信息
        """
        log.info("查询商品信息")
        uri = '/API/sku/product/v1/selectSkuNew'
        url = self.urls + uri
        data = {"pageSize":10,"pageNum":1,"channelId":channelId,"marketId":marketId,"name":productCode}
        res = requests.post(url=url, json=data, headers=self.oms_headers)
        for i in res.json()['data']['items']:
            if str(i['productCode']) == str(productCode):
                return i



    def test_getProductEx(self,productCode=1112,channelId=45):
        uri = f'/API/sku/platform/v1/getProductEx?code={productCode}&channelId={channelId}'
        url = self.urls + uri
        res = requests.get(url=url, headers=self.oms_headers)
        print(res.json())


    def get_market_channel_byName(self,market_name,channel_name=None):
        uri = '/API/basics/marketChannel/v1/queryAuthMarketChannel?status=1&pageSize=0&pageNum=0'
        url = self.urls + uri
        res = requests.get(url=url, headers=self.oms_headers)
        for i in res.json()['data']:
            if market_name == i['mcName'] and i['parentId'] == 0:
                market_id = i['id']
        if channel_name != None:
            for j in res.json()['data']:
                if j['parentId'] == market_id and j['mcName'] == channel_name :
                    channel_id = j['id']
            return market_id,channel_id
        else:
            return market_id

    def test_shaomiao1(self,documentsNo='WPH202402201457100001'):
        """扫描
        """
        log.info("扫描")
        uri = "/API/wms/audit/v1/queryAuditDetails"
        url = self.urls+uri
        data =  {"no":documentsNo,"type":"ONCE","printId":"47c707e1866c4dc98c31324f77110a99"}
        res = requests.get(url=url,params = data, headers=self.oms_headers)
        log.info(json.dumps(res.json(),ensure_ascii=False))
        return res.json()['data']['documentsPickId'],res.json()['data']['documentsPickDetailsId']


    def test_shaomiao_sku_info(self,documentsPickId,documentsPickDetailsId):
        """扫描"""
        log.info("扫描")
        uri = "/API/wms/audit/v1/queryAuditSku"
        url = self.urls + uri
        data = {"documentsPickId": documentsPickId, "documentsPickDetailsId": documentsPickDetailsId}
        res = requests.get(url=url, params=data, headers=self.oms_headers)
        log.debug(uri,data)
        log.info(json.dumps(res.json(),ensure_ascii=False))
        return res.json()['data']['auditSku']

    def fuhe(self,documentsPickId,documentsPickDetailsId,audit_sku_list,status_type=1,printId='8aba99e92e584f50b298cefb83af9b52'):
        """批量复核
           status_type = 1  #2C复核   0  2B复核
        """
        log.info("批量复核")
        uri = "/API/wms/audit/v1/auditSku"
        url = self.urls + uri
        for sku in audit_sku_list:
            data = {"packageUser": "黄镇", "auditNum": sku['skuNum'], "documentsPickDetailsId": documentsPickDetailsId,
             "documentsPickId": documentsPickId,
             "functionBars": [{"type": "pack", "status": status_type, "disabled": False},
                              {"type": "print_documents", "status": 0, "disabled": True},
                              {"type": "print_label", "status": 0, "disabled": True}], "skuCode": sku['skuCode'],
             "printId": printId, "type": "ONCE"}
            res = requests.post(url=url, json=data, headers=self.oms_headers)
            log.info(res.json())


    def dabao_fuhe(self,documentsNo):
        """打包复核"""
        log.info("打包复核")
        documentsNo = documentsNo
        documentsPickId,documentsPickDetailsId=self.test_shaomiao1(documentsNo)
        audit_sku_list = self.test_shaomiao_sku_info(documentsPickId,documentsPickDetailsId)
        self.fuhe(documentsPickId,documentsPickDetailsId,audit_sku_list=audit_sku_list)

    def chengzhong(self,documentsNo):
        """称重"""
        log.info("称重")
        uri = "/API/wms/documentsOut/v1/weighOut"
        url = self.urls+uri
        data = {"hight":2,"length":2,"relationDocumentsNo":documentsNo,"weight":1.01,"width":2,"totalWeightView":0,"orderTag":None}
        res = requests.post(url=url, json=data, headers=self.oms_headers)
        log.info(res.json())
        return res.json()

    def queryOutBagShippingCount(self):
        uri = '/API/wms/documentsOut/v1/queryOutBagShippingCount'
        url = self.urls+uri
        data = {"warehouseIds":[],"trackStatus":False,"weighStatus":1}
        res = requests.post(url=url, json=data, headers=self.oms_headers)
        log.debug(res.json())
        return res.json()['data']



    def get_zhuangdai_id(self,documentsNo):
        """获取装袋ID
        """
        uri = "/API/wms/documentsOut/v1/queryBagPage"
        url = self.urls+uri
        shipping_count_list = self.queryOutBagShippingCount()
        for shipping in shipping_count_list:
            logisticsServiceProviderCode = shipping['logisticsServiceProviderCode']
            for shipping_id in shipping['shippingList']:
                shippingId = shipping_id['shippingId']
                data = {"pageSize":2000,"pageNum":1,"trackStatus":False,"trackingNumber":"","relationDocumentsNo":documentsNo,"weighStatus":2,"warehouseIds":[],"shippingId":shippingId,"logisticsServiceProviderCode":logisticsServiceProviderCode}
                res = requests.post(url=url, json=data, headers=self.oms_headers)
                try:
                    zhuangdai_id = res.json()['data']['records'][0]['id']
                    print(zhuangdai_id)
                    return zhuangdai_id
                except Exception:
                    pass
                data = {"pageSize": 2000, "pageNum": 1, "trackStatus": False, "trackingNumber": "","relationDocumentsNo": documentsNo, "weighStatus": 2, "warehouseIds": [],"logisticsServiceProviderCode": logisticsServiceProviderCode}
                res = requests.post(url=url, json=data, headers=self.oms_headers)
                try:
                    zhuangdai_id = res.json()['data']['records'][0]['id']
                    return zhuangdai_id
                except Exception:
                    pass


    def zhuangdai(self,documentsNo):
        """装袋
        """
        log.info("装袋")
        zhuangdai_id = self.get_zhuangdai_id(documentsNo)
        uri = "/API/wms/documentsOut/v1/createBatch"
        url =  self.urls+uri
        data = [zhuangdai_id]
        res = requests.post(url=url, json=data, headers=self.oms_headers)
        log.info(res.json())
        return res.json()


    def test_dabao_fuhe(self):
        # self.dabao_fuhe(documentsNo='WPH202402201502310001')
        # self.chengzhong(documentsNo='WPH202402201502310001')
        # self.queryOutBagShippingCount()
        # aa  = self.get_zhuangdai_id('WPH202404091459140001')
        # print(aa)
        self.zhuangdai(documentsNo='WPH202404091459140001')

    def get_market_channel_byId(self,market_id=None,channel_id=None):
        uri = '/API/basics/marketChannel/v1/queryAuthMarketChannel?status=1&pageSize=0&pageNum=0'
        url = self.urls + uri
        res = requests.get(url=url, headers=self.oms_headers)
        if market_id != None and channel_id != None:
            for i in res.json()['data']:
                if channel_id == i['id']:
                    channel_name = i['mcName']
                for j in res.json()['data']:
                    # print(j)
                    if j['id'] == market_id:
                        market_name = j['mcName']
            return market_name,channel_name
        else:return res.json()




    def  create_other_in_byName(self,warehouseName,marketName,channelName,product_code_list,num=100,warehouseId=None):
        """其它入库"""
        log.info("其它入库")
        uri = '/API/srm/otherIn/v1/createOrUpdateOtherIn'
        url = self.urls + uri
        market_id, channel_id = self.get_market_channel_byName(marketName, channelName)
        product_info_list = []
        product_code_list = list(set(product_code_list))
        for product_code in product_code_list:
            product_info = self.get_product( productCode=product_code,warehouseName=warehouseName)
            log.info(product_info)
            product ={"productCode":product_code,"productId":product_info['productId'],"productStatusName":product_info['productStatusName'],"productStatusId":product_info['productStatusId'],"weight":product_info['weight'],"productName":product_info['productName'],"selectNum":num,"newSelectNum":num,"productNum":num,"inNum":num}
            product_info_list.append(product)
        data = {"channelName":channelName,"marketId":market_id,"channelId":channel_id,"marketName":marketName,"warehouseCode":self.get_warehouse_info(warehouseName)['warehouseCode'],"warehouseName":warehouseName,"reason":"DR定制广宣品","warehouseId":self.get_warehouse_info(warehouseName)['id'],"remark":"test备注",
                "infoList":product_info_list}
        res = requests.post(url=url, json=data, headers=self.oms_headers)
        log.info(res.text)
        return res.json()

    def  create_other_in_byId(self,warehouseId,market_id,channel_id,product_code_list,num=100):
        """其它入库"""
        log.info("其它入库")
        uri = '/API/srm/otherIn/v1/createOrUpdateOtherIn'
        url = self.urls + uri
        product_code_list = list(set(product_code_list))
        product_info_list = []
        for product_code in product_code_list:
            product_info = self.get_product( productCode=product_code,warehouseId=warehouseId)
            product ={"productCode":product_code,"productId":product_info['productId'],"productStatusName":product_info['productStatusName'],"productStatusId":product_info['productStatusId'],"weight":product_info['weight'],"productName":product_info['productName'],"selectNum":num,"newSelectNum":num,"productNum":num,"inNum":num}
            product_info_list.append(product)
        market_name, channel_name = self.get_market_channel_byId(market_id=market_id, channel_id=channel_id)
        data = {"channelName":channel_name,"marketId":market_id,"channelId":channel_id,"marketName":market_name,"warehouseCode":self.get_warehouse_info(warehouseId=warehouseId)['warehouseCode'],"warehouseName":self.get_warehouse_info(warehouseId=warehouseId)['warehouseName'],"reason":"DR定制广宣品","warehouseId":warehouseId,"remark":"test备注",
                "infoList":product_info_list}
        res = requests.post(url=url, json=data, headers=self.oms_headers)
        log.info(res.text)
        return res.json()
    def getOtherIn_info(self):
        uri = '/API/srm/otherIn/v1/queryOtherInPage'
        url =  self.urls + uri
        data = {"pageSize":15,"pageNum":1,"timestamp":1710928789000}
        res = requests.post(url=url, json=data,headers=self.oms_headers)
        return res.json()

    def submitOtherIn(self):
        """提交其它入库
        """
        log.info("提交其它入库")
        time.sleep(1)
        id = self.getOtherIn_info()['data']['items'][0]['id']
        uri = f'/API/srm/otherIn/v1/submitOtherIn?id={id}'
        url =  self.urls + uri
        res = requests.get(url=url, headers=self.oms_headers)
        log.info(res.json())
        return res.json()


    def order_detail(self,orderCode):
        """获取订单详情信息"""
        log.info("获取订单详情信息")
        uri = '/API/oms/order/v1/list'
        data = {"pageSize":15,"pageNum":1,"realTimeType":2,"name":orderCode,"codeType":1,"codeMode":1,}
        res = requests.post(url=self.urls + uri, json=data, headers=self.oms_headers)
        orderId = res.json().get('data', {}).get('items', [{}])[0].get('id')
        warehouseId = res.json().get('data', {}).get('items', [{}])[0].get('warehouseId')
        marketId = res.json().get('data', {}).get('items', [{}])[0].get('marketId')
        channelId = res.json().get('data', {}).get('items', [{}])[0].get('channelId')
        uri = '/API/oms/order/v1/detailNew?orderId=%s'%orderId
        url = self.urls + uri
        res = requests.get(url=url,  headers=self.oms_headers)
        sku_list = []
        for i in res.json()['data']['orderItemList']:
            for j in i['sysItems']:
                sku_list.append(j['productCode'])
        return {"warehouseId":warehouseId,"marketId":marketId,"channelId":channelId,"sku_list":sku_list}

    def queryReceivingPage(self,documentsNo):
        """根据仓库单号，获取收货通知单信息
        :return:
        cargoOwnerId 单据ID，
        storageNo  送货单号
        """
        log.info("根据仓库单号，获取收货通知单信息")
        uri = "/API/wms/documentsReceiving/v1/queryReceivingPage"
        url = self.urls+uri
        data = {"pageSize":15,"pageNum":1,"timeArr":[],"type":1,"documentsNo":documentsNo,"storageNo":"","purchaseNo":"","kingdeeNo":"","storageType":"","supplierName":"","buyer":"","status":"","skuCode":"","tallyman":"","warehouseId":"","warehouseIds":[]}
        res = requests.post(url=url, json=data,headers=self.oms_headers)
        log.info(res.json())
        return res.json()

    def confirmArrive(self,id):
        """确认到货
        """
        log.info("确认到货")
        uri = f'/API/wms/documentsReceiving/v1/confirmArrive?id={id}'
        url =  self.urls+uri
        res = requests.get(url=url,headers=self.oms_headers)
        log.info(json.dumps(res.json(),ensure_ascii=False))
        return res.json()




    def queryReceivingDetailPage(self,documentsId,cargoOwnerId,storageNo):
        """获取收货单明细,保存
        :return:
        """
        log.info("获取收货单明细,保存")
        uri = '/API/wms/documentsReceiving/v1/queryReceivingDetailPage'
        url =  self.urls+uri
        data = {"pageSize":1500,"pageNum":1,"cargoOwnerId":cargoOwnerId,"skuCode":"","storageNo":storageNo}
        res = requests.post(url=url, json=data, headers=self.oms_headers)
        log.debug(json.dumps(res.json(),ensure_ascii=False))
        uri = '/API/wms/documentsReceiving/v1/onlySave'
        url = self.urls + uri
        sku_data_list = []
        sku_data_list2 = []
        for i in res.json()['data']['records']:
            data_info = {"detailId": i['id'], "skuCode": i['skuCode'], "skuNum": i['skuNum'], "tallyingNum": i['tallyingNum'],"tallyingNumNow": i['awaitReceivingNum'], "awaitReceivingNum": i['awaitReceivingNum']}
            data_info2 = {"detailId": i['id'], "skuCode": i['skuCode'], "skuNum": i['skuNum'], "tallyingNum": i['tallyingNum'],"tallyingNumNow": 0, "awaitReceivingNum": 0}
            sku_data_list.append(data_info)
            sku_data_list2.append(data_info2)
        data = {"id": documentsId, "infoList": sku_data_list}
        res = requests.post(url=url,json=data,headers = self.oms_headers)
        log.debug(url)
        log.debug(json.dumps(data,ensure_ascii=False))
        log.debug(res.json())
        uri = '/API/wms/documentsReceiving/v1/acceptFinish'
        url =  self.urls+uri
        data = {"id": documentsId, "infoList": sku_data_list2}
        res = requests.post(url=url, json=data, headers=self.oms_headers)
        log.debug(url)
        log.debug(json.dumps(data, ensure_ascii=False))
        log.debug(res.json())
        return res.json()

    def createPutaway(self,id):
        """生成入库上架单
        """
        log.info("生成入库上架单")
        uri = f'/API/wms/documentsReceiving/v1/createPutaway?id={id}'
        url = self.urls+uri
        res = requests.get(url=url,headers = self.oms_headers)
        log.info(res.json())
        return res.json()

    def queryPutawayDetailPage(self,documentsNo):
        """获取入库上加单详情-->上架
        """
        #获取入库上架单单据ID
        uri = '/API/wms/DocumentsPutaway/v1/queryPutawayPage'
        url =  self.urls+uri
        data = {"pageSize":15,"pageNum":1,"timeArr":[],"beginTime":"","endTime":"","documentsNo":"","warehouseId":"","receivingNo":documentsNo,"storageNo":"","kingdeeNo":"","storageType":"","canPrint":"","status":"","skuCode":"","putawayBy":""}
        res = requests.post(url=url, json=data, headers=self.oms_headers)
        log.info('获取入库上架单单据ID')
        log.info(res.json())
        putawayId = res.json()['data']['records'][0]['id']
        #获取入库上架单详情
        uri='/API/wms/documentsPutawayDetail/v1/queryPutawayDetailPage'
        url=self.urls+uri
        data = {"pageSize":1500,"pageNum":1,"putawayId":putawayId,"skuCode":""}
        res = requests.post(url=url, json=data, headers=self.oms_headers)
        log.info(json.dumps(res.json(),ensure_ascii=False))
        #批量上架
        uri = '/API/wms/documentsPutawayDetail/v1/batchPutawayDetail'
        url =  self.urls+uri
        infoList =[]
        for i in res.json()['data']['records']:
            info_data = {"detailId":i['id'],"infoList":[{"goodsAllocationId":i['recommendGoodsAllocationId'],"goodsAllocationCode":"A1-24","putawayNum":i['waitPutawayNum'],"waitPutawayNum":0}]}
            infoList.append(info_data)

        data =infoList
        res = requests.post(url=url, json=data, headers=self.oms_headers)
        log.info("批量上架")
        log.info(res.json())
        #上架确认
        uri = f'/API/wms/documentsPutawayDetail/v1/putawayConfirm?putawayId={putawayId}'
        url = self.urls+uri
        log.info('上架确认')
        res = requests.get(url=url, headers=self.oms_headers)
        log.info(res.json())
        return res.json()

    def create_put_way(self,documentsNo='WSH2404191718010001'):
        """发货通知单-->生成入库上架
        """
        log.info("发货通知单-->生成入库上架")
        #查询列表信息
        documentsInfo = self.queryReceivingPage(documentsNo = documentsNo)
        documentsId = documentsInfo['data']['records'][0]['id']
        #确认到货
        self.confirmArrive(id=documentsId)
        cargoOwnerId,storageNo = documentsInfo['data']['records'][0]['cargoOwnerId'],documentsInfo['data']['records'][0]['storageNo']
        #获取单据SKU信息
        self.queryReceivingDetailPage(documentsId=documentsId,cargoOwnerId=cargoOwnerId,storageNo=storageNo)
        #生成入库上架单
        self.createPutaway(id = documentsId)
        #入库上架
        self.queryPutawayDetailPage(documentsNo=documentsNo)

    def handover(self,documentsNo):
        """查询待交接ID
        """
        uri = "/API/wms/documentsOutBatch/v1/queryWaitHandoverBagPage"
        url =  self.urls+uri
        data = {"pageSize":15,"pageNum":1,"type":1,"orderCode":"","schedulingNo":"","type1":1,"shipmentId":"","createBy":"","documentsNo":"","relationDocumentsNo":documentsNo,"referenceNo":"","skuCode":"","status":"","warehouseIds":[],"handoverStatus":1,"logisticsServiceProviderCode":"","orderTags":[],"shippingId":""}
        log.info("查询待交接ID")
        res = requests.post(url=url,json=data, headers=self.oms_headers)
        log.info(res.json())
        handoveId = res.json()['data']['records'][0]['id']
        uri = f'/API/wms/documentsOutBatch/v1/updateHandover?id={handoveId}'
        url = self.urls + uri
        log.info("交接")
        res = requests.get(url=url, headers=self.oms_headers)
        log.info(res.json())
        return res.json()

    def test_add_tracking_number(self,order_code='SO24061400813'):
        """旺店通订单跟踪单号为空的订单设置跟踪单号"""
        SQL = "SELECT * FROM t_order_base WHERE  order_code = '%s' and  tracking_number =''"%order_code
        # print(SQL)
        results = self.query(SQL)
        if results:
            tracking_number=str(int(time.time()))
            for result in results:
                sql = "update t_order_base set  tracking_number = '%s' where id = %s"%(tracking_number,result[0])
                self.update(sql)



    def test_audit_order(self,orderCode='SO24041300086',warehouseName='中国深圳直发仓',expressTypeName='韵达',orderStatus=2):
        """审核订单，库存不足自动增加库存"""
        res = self.order_audit(orderNo=orderCode,warehouseName=warehouseName,expressTypeName=expressTypeName,orderStatus=orderStatus)
        data = res.get('data', {})
        error_list = data.get('errorList', [])
        if error_list:
            first_error = error_list[0]
            msg = first_error.get('msg', '')
            if '库存不足' in msg:
                res = self.order_detail(orderCode=orderCode)
                #新增入库
                self.create_other_in_byId(warehouseId=res['warehouseId'], market_id=res['marketId'],channel_id=res['channelId'], product_code_list=res['sku_list'], num=100)
                #提交入库
                self.submitOtherIn()
                input("钉钉审批后，在控制台按回车:")
                # 同步钉钉状态
                self.do_job(id=311)
                time.sleep(2)
                documentsNo = self.getOtherIn_info()['data']['items'][0]['wmsReceivingNo']
                #入库上架 ---需要判断是否是自营仓，不是自营仓不走wms入库上架，需要注释掉
                self.create_put_way(documentsNo)

                #重新审核
                self.order_audit(orderNo=orderCode, warehouseName=warehouseName, expressTypeName=expressTypeName,orderStatus=7)



    def test_other_in(self,warehouseName='中国深圳直发仓',marketName='Website-Pro',channelName='LeqiMall-All',product_code_list=['3708'],num=100):
        """其它入库"""
        # product_code_list =["843","877","916","971","976","1027","1069","1093","1187","1446","1597","1611","1748","1767","1815","1821","1837","1860","1878","1879","1885","1974","1981","1988","1997","2013","2024","2027","2029","2031","2057","2061","2076","2080","2101","2125","2142","2159","2179","2191","2198","2214","2230","2233","2821","2829","2831","2840","2845","2853","2854","1074B","1534B","1684B","1842B","1846B","1864B","1891B","1968C","1991B","2007C","2010B","2096B","2108B","2118B","2146B","2168B","2221B","ABL2325","APL2282","APL2311","APL2331B","APS2318","APU2381","APU2458","BSL2361","BSM2489","BSP2380","BUM2383","CCS2645","CMS2405","CMS2470","CPA2204","CPA2455","CPA2512","CPU2391B","CPU2494","DBR2267","DCD2375","DPR2304","HSS2424","HTN2439B","LCC2408","LCC2516","MD2302","MD2384","838","859","862","900","915","1055","1135","1157","1262","1403","1523","1547","1576","1590","1617","1630","1631","1658","1700","1723","1756","1765","1800","1899","1907","1933","1951","1961","1979","2001","2005","2033","2039","2051","2075","2085","2120","2131","2144","2156","2164","2192","2201","2207","2231","2232","2240","2249","2827","2857","1583B","1615B","1848B","1902B","1941B","1950B","2097B","2109B","2122B","2176B","AEH2461","APB2673","APL2341","APL2350","APT2671","BSM2298","BSM2351","BSM2352","BSS2413","BSS2436","BUC2637","BUN2501","CCC2382","CCP2345","CPA2471","CVB2255","DBC2280","HTN2439","HTR2316","HTS2367","KDBC2469","KHTR2309","KSAP2757","LCC2516B","PCC2462","TC2400","TC2453","752","842","1092","1626","1639","1681","1682","1717","1744","1764","1827","1925","2026","2034","2055","2082","2084","2113","2151","2177","2220","2238","2760","2770","2771","2855","1686B","1921B","2014C","2124B","2203B","2212B","APS2295","BSA2650","BSS2283","BSS2340","BSS2401","BSS2402","BUC2638","CCC2332","CCM2712","CMA2338","CMA2409","CPA2414","CVB2254B","CVS2344","HSN2399","HSR2511","LCS2438","TS2432","1052","1083","1584","1599","1601","1610","1642","1647","1685","1726","1751","1773","1779","1798","1802","1819","1855","2016","2069","2098","2105","2107","2202","2210","2219","2226","2244","1587B","1903B","2068B","2143B","2246B","APL2339","APL2349B","APL2354","APS2672","APU2364","BSA2355","BSE2256","BSS2273B","BSS2286","BUB2378","BUN2395","BUS2478","CCF2370","CCN2404","CPH2628","LCC2387","1051","1091","1134","1255","1522","1688","1750","1843","1856","1914","1943","1975","1993","2006","2106","2141","2170","2241","1594B","2002B","2114B","2129B","BSC2390","BSE2385","BSS2275","BSS2319","CCC2515","CCN2262","CCP2513","CMS2684","CVD2475","DPC2508","LCC2445","LCN2667","PSC2428","PSW2398","SAP2804","855","856","871","1245","1462","1493","1659","1690","1740","1787","1831","1835","1853","1872","1906","2056","2074","2128","2130","2163","2169","2215","2218","2225","2229","1732B","1982B","2003C","2062B","2186B","AAK2371","AAK2495","APU2389","BSS2308","BSS2328","BSS2412","BUC2342","BUC2498","BUN2464","CCC2407","CVG2505","CVZ2423","HPS2675","LCN2525","PSC2639","VH2500","VH2689","851","960","1716","1757","1795","1822","1845","1852","1972","1898B","2115B","AAN2366","AAW2285","BSA2696","BSC2259","BUC2497","CCC2365","CCN2499","CCP2446","CCS2268","CMA2305","DBC2261","DBM2266B","DCD1104B","KBUM2394","LCC2657","LCP2655","1054","1875","1876","1995","2060","2172","2828","1889B","2046B","2127B","BSE2294","BSE2431","BSS2420B","BSS2437","BUC2433","BUC2627","BUN2521","1050","1528","1661","1828","2174","2248","1280B","APL2278","APL2357","APU2668","BUT2664","CSD2321","HTR2297","828","951","974","1463","1870","1955","2059","2119","1897B","2245B","BSS2263","BSS2277","BSW2480","CCC2422","CVB2254","DCS2279","1049","1600","1693","1960","2171","2243","BSC2335","BSS2276","BSS2710","BUB2336","BUC2662","CCC2658","CCP2411","LCC2397","904","1566","2152","1954B","2044B","BSS2250B","BSS2711","BUC2517","CCF2356","DBC2506","HTN2362","PAC2421","1568","2008","2065","AAW2459","BSC2333","BSE2347","BSS2222B","BUC2334","CVG2320","HSS2426","1254","1970","1973","2077","2826","2093B","AAW2284","BSH2343","CCC2271","CCF2810","FAQ2323","KPAC2466","LCS2503","MD2393","2058","2157","2221","1638B","2071B","APL2253","BSE2386","LCS2467","1679","1871","2103B","BSE2348","CVD2360","1549","1713","1939B","BUC2806","1447","1775","BSC2809","CCS2629","CVZ2264","HSN2427","VH2807","2246","2251","APT2510","HSN2270","735","860","BUC2260B","BUC2496","1859","CCS2416","LCS2417","1498","2247","CCS2493","1409","2070B","BSW2482","761","1674","2228","2094B","2187B","973B","BSS2636B","1053","1124","1593","1497","2165B","CCS2434","870","2823","AAK2363","APL2258","BSS2403","CMA2209","BUC2317","CVG2678","BSL2681","1138","1598","BSS2465","2049","CCS2310","VH2299","1195B","AAK2213C","BUC2736","1241","2122C","CCP2488","942","2161","CCM2518","2245","BSS2314B","CCF2808","2087B","2066","BSL2680","BSS2714","2214B","APL2331","BSP2415","DBC2272B","HSS2425","2166B","2245B","1889B","2122C","2165B","1842B","CVD2360","BUC2334","APL2339","HSN2399","BSS2636B","CCC2515","2087B","BSL2681","APL2258","2187B","2203B","HSN2270","BSS2222B","CCC2271","BUB2336","2103B","CVG2320","CCS2434","CMA2209","CMA2305","HSS2425","CCS2416","CCM2518","CCP2488","BSE2431","LCC2397","CCS2629","BUC2517","CVG2505","BUC2317","CCS2310","BSS2314B","2044B","BSE2386","BSE2348","BSP2415","CVG2678","CCF2808","2912","VH2269","BUN2468B","2030C","2814","2919","2920","2921","2922","0000","BUN2484B","998B","2824","2836","2769","2767","2766","2799","2900","2100B","BUN2483B","2017","W1001","W1005","W1006","W1007","W1008","W1010","W1011","W1012","W1014","W1015","W1016","W1017","W1018","W1019","2082","1661","1955","2243","CPU2391B","1498","2246","2092B","2844","2144B","1887B","1980B","1788","1789","2205","BSE2346B","2841","2112","2035","2133B","2132B","1065","1089","1125","2025","2117C","2174B","DCD2374","PPP2392","BUN2485B","2847","2885","1497","1138","2214B","APL2278","2798","2901","2825","BUN2486B","2028","PAC2456","1810B","1824","LCF2811","2839","LCF2811","1660","1589","1650","1894","1938","1958","2038","2063","2132","2200","2208","2211","1807B","1963B","BSC2435","BUM2448","CPS2454","DCD2376","LVB2635","MD2519","CPU2391","2146","DBC2272","1976","2123","1701","KDBC2406","CCP2410","CCC2442","CVB2255B","2083C","CVZ2372B","2167B","2072B","2244","AAK2213C","2094B","2130","BSH2343","DBC2506","HTN2362","BUC2260B","BSS2273B","APU2364","AAK2363","2071B","2070B","BSS2250B","2228","1775","1798","BSS2413","CCS2493","BUC2342","1447","BUC2497","VH2269","TC2453","CCC2422","BSC2335","AAK2371","CCF2356","BSM2352","2191","1954B","1693","2210","2881","2879","2858","CMA2520","2102","2045C","2727","DCD1112B","2150B","APS2318","BSC2333","1822","LCS2417","2244","CVB2254","2245","CCC2332","TC2713","EB2698","LCF2812","LCF2813","BUT2429","AAA2700","2915","CCS2236B","AAK2326","2792","2093B","BSE2346B","CPS2441","2158","1970","2220","2049","1679","2832","2134B","2914","2775","2776","2777","2778","W01-01-0001","W01-01-0004","W01-01-0006","W01-01-0007","2786","1854B","2765","2913","W01-01-0003","MD2692","HTS2756","2913","2773","AAAA","2774","APL2253","2251","1674","LCC2516B","2172","AAK2495","2122B","CCF2370","CCF2810","BUC2369","1710","2938","2081C","2937","BSS2327","2154B","HTN2670","CCP2646","842B","2882","2116B","BSC2259","LCN2525","HSS2426","VH2299","2202","2221","CVZ2423","2203","1703B","2126B","2875","CMS2641","1669C","2863","2865","2876","2870","2869","1587C","1897C","2030D","2118C","2243B","KCVB2419B","2114C","BSS2314C","APS1854C","2790","2012","2867","CCF2761","HTH2759","2861","BSS2636C","2936","2771B","HTN2758","W1013","W2002","W2003","2234B","2821B","DBC2506B","2877","BSS2340","2105","DBC2506B","BSS2636C","BUC2498","HTN2439B","2146B","KCCS2694","2858","1860","2786","BSA2650","BSS2714","AAK2213C","2165B","1713","BUC2260B","HSN2427","2087B","BSE2346B","2156","BSE2294","2243","1078","1653","1998","BSL2644","BSM2368","1679","2107","CMA2209","BSS2314C","APL2331B","CVD2475","2866","1810C","PPP2396","1135","LCF2812","2191B","HSN2093C","2797","2971","2211B","AAK2651","HSS2425","1960","2937","2044B","BUB2336","EB2504","2115C","HTR2640","BSC2333","BUT2664","BSM2352","2938","2790","2947","2889","HTS2457","2972","2880","2982","2833","2916","2970","MD2303B","KCCS2752","KLCS2746","BSE2256B","2002C","2081D","LCF2811B","KCVB2749","1564","AAL2289","MB2300","KCVB2747","KCCS2750","1963C","1968D","VH2299B","2872","2052B","2137B","HSS2642","BUN2501B","BUT2665","1890B","MB2353","KCCS2751","1889C","2873","2102B","BUN2521B","2868","2097C","KCVB2748","HPG2315","1806","2904","2903","2906","2905","2791",]
        self.create_other_in_byName(warehouseName=warehouseName,marketName=marketName,channelName=channelName,product_code_list=product_code_list,num=num)
        # 提交入库
        self.submitOtherIn()
        input("飞书审批后，在控制台按回车:")
        if self.env == 'uat':
            # 同步飞书状态
            self.do_job(id=602)
        else:
            # 同步飞书状态
            self.do_job(id=602)
        time.sleep(5)
        documentsNo = self.getOtherIn_info()['data']['items'][0]['wmsReceivingNo']
        # 需要自行判断是否是自营仓，非自营仓不走WMS，需要注释
        self.create_put_way(documentsNo=documentsNo)
        #推送库存到旺店通
        # time.sleep(3)
        # self.do_job(588)



    def test_addOder_to_send(self):
        #新增2c订单
        orderNo = self.add_order(channelName='LeqiMall-All',product_list=[1112,1124],platformId=60)
        #提交订单
        self.order_submit(orderNo)
        #订单审核
        self.order_audit(orderNo=orderNo, warehouseName='中国深圳直发仓', expressTypeName='顺丰特快-寄付',orderStatus=2)
        # #合并订单
        time.sleep(5)
        self.do_job(id=556)
        time.sleep(5)
        documentsNo = self.get_order_documentsNo(orderNo=orderNo)
        while documentsNo == "" :
            # 合并订单
            self.do_job(id=556)
            time.sleep(3)
            # #推送订单
            self.do_job(id=557)
            time.sleep(3)
            documentsNo = self.get_order_documentsNo(orderNo=orderNo)

        log.info(documentsNo)
        #查询仓库单号
        self.get_tagWarehouseCode(documentsNos=documentsNo)
        #2c已分配配货单--下架
        self.DistributionLowerShelf(documentsNos=documentsNo)
        #开始拣货
        self.startPick(documentsNo=documentsNo)
        #结束拣货
        self.finishPick(documentsNo=documentsNo)
        #打包复核
        self.dabao_fuhe(documentsNo=documentsNo)
        #称重
        self.chengzhong(documentsNo=documentsNo)
        #装袋
        self.zhuangdai(documentsNo=documentsNo)
        #交接
        # self.handover(documentsNo=documentsNo)




    def test_pull_warehouse(self):
        #同步第三方仓状态
        self.do_job(id=558)
        #同步钉钉状态
        # self.do_job(id=311)

    def test_add_order_inventory(self,orderCode='SO25010900011',num=10):
        """根据订单号加库存
        """
        res = self.order_detail(orderCode=orderCode)
        #创建其它入库
        self.create_other_in_byId(warehouseId=res['warehouseId'],market_id=res['marketId'],channel_id=res['channelId'],product_code_list=res['sku_list'],num=num)
        # 提交入库
        self.submitOtherIn()
        input("飞书审批后，在控制台按回车:")
        if self.env == 'uat':
            # 同步飞书状态
            self.do_job(id=602)
        else:
            # 同步飞书状态
            self.do_job(id=602)
        time.sleep(5)
        documentsNo = self.getOtherIn_info()['data']['items'][0]['wmsReceivingNo']
        #需要自行判断是否是自营仓，非自营仓不走WMS，需要注释
        self.create_put_way(documentsNo=documentsNo)
        # self.create_put_way(documentsNo='WSH2405141422460001')


    def test_audit_to_wms(self,orderNo='SO25010600010',orderStatus=7,warehouseName='中国深圳直发仓',expressTypeName='中通线下'):
        """订单审核并推送WMS-->发货
        """
        #旺店通在审单前，如果没有跟踪单号，随机生成一个
        self.test_add_tracking_number(order_code=orderNo)
        #订单审核
        self.order_audit(orderNo=orderNo, warehouseName=warehouseName, expressTypeName=expressTypeName,orderStatus=orderStatus)
        #合并订单
        time.sleep(5)
        self.do_job(id=556)
        time.sleep(5)
        #推送订单
        documentsNo = self.get_order_documentsNo(orderNo=orderNo)
        num = 0
        while documentsNo == "" :
            if self.env == "test":
                # 合并订单
                self.do_job(id=556)
                time.sleep(3)
                #推送订单
                self.do_job(id=557)
            elif self.env == 'uat':
                # 合并订单
                self.do_job(id=559)
                time.sleep(3)
                #推送订单
                self.do_job(id=560)
            time.sleep(3)
            documentsNo = self.get_order_documentsNo(orderNo=orderNo)
            num = num +1
            if num ==3 :
                raise ValueError("订单已推送第三方仓，等待异步TMS返回")

        log.info(documentsNo)
        self.test_wms(documentsNo)


    def test_wms(self,documentsNo='WPH2501090004'):
        """WMS流程走到交接
        """
        #查询仓库单号
        self.get_tagWarehouseCode(documentsNos=documentsNo)
        #2c已分配配货单--下架
        self.DistributionLowerShelf(documentsNos=documentsNo)
        #开始拣货
        self.startPick(documentsNo=documentsNo)
        #结束拣货
        self.finishPick(documentsNo=documentsNo)
        #打包复核
        self.dabao_fuhe(documentsNo=documentsNo)
        #称重
        self.chengzhong(documentsNo=documentsNo)
        #装袋
        self.zhuangdai(documentsNo=documentsNo)
        #交接
        self.handover(documentsNo=documentsNo)

    def test_merged_push_order(self):
        if self.env == "test":
            # 合并订单
            self.do_job(id=556)
            time.sleep(3)
            #推送订单
            self.do_job(id=557)
        elif self.env == 'uat':
            # 合并订单
            self.do_job(id=556)
            time.sleep(3)
            #推送订单
            self.do_job(id=557)




    def test_addOder_to_send_1(self):
        documentsNos = []
        orderNos = []

        # #批量审单推送
        # SQL = "SELECT order_code FROM t_order_base where order_status = 2 and order_sn_source like 'CK%'  and create_time<'2024-05-17 16:59:59' and create_time>'2024-05-16 15:59:59'  AND (tag_warehouse_code IS NOT NULL OR  tag_warehouse_code != ' ') order by create_time desc "
        # results = self.query(SQL)
        # for result in results:
        #     print(result[0])
        #     orderNos.append(result[0])
        # #订单审核
        # for orderNo in orderNos:
        #     print(orderNo)
        #     self.order_audit(orderNo=orderNo, warehouseName='中国深圳直发仓', expressTypeName='中通线下',
        #                      orderStatus=2)
        #     self.do_job(id=556)
        #     self.do_job(id=557)



        print(documentsNos)
        for documentsNo in documentsNos:
            try:
                self.handover(documentsNo=documentsNo)
            except:
                pass

        SQL = "SELECT tag_warehouse_code FROM t_order_base where order_status = 3 and order_sn_source like 'CK%'  and create_time<'2024-05-17 16:59:59' and create_time>'2024-05-16 15:59:59'  AND (tag_warehouse_code IS NOT NULL OR  tag_warehouse_code != ' ') order by create_time desc "
        results = self.query(SQL)
        for result in results:
            print(result[0])
            documentsNos.append(result[0])
        for documentsNo in documentsNos:
            log.info(documentsNo)
            try:
                # 查询仓库单号
                self.get_tagWarehouseCode(documentsNos=documentsNo)
            except:pass
            try:
                # 2c已分配配货单--下架
                self.DistributionLowerShelf(documentsNos=documentsNo)
            except:pass
            try:
                # 开始拣货
                self.startPick(documentsNo=documentsNo)
            except:pass
            try :
                # 结束拣货
                self.finishPick(documentsNo=documentsNo)
            except:pass
            try:
                # 打包复核
                self.dabao_fuhe(documentsNo=documentsNo)
            except:pass
            try:
                # 称重
                self.chengzhong(documentsNo=documentsNo)
            except:pass
            try:
                # 装袋
                self.zhuangdai(documentsNo=documentsNo)
            except:pass


        #    # 交接
           #  self.handover(documentsNo=documentsNo)






    def test_dojob(self):
        """样品赠品推送到订单"""
        for i in range(10):
            # #同步飞书审批结果
            self.do_job(602)
            time.sleep(1)
            #【样品/赠品单】申请单提交生成销售赠品单
            self.do_job(301)
            #【销售订单】提交下推发货订单
            self.do_job(280)
            # #【销售订单】发货订单发货或取消反写销售发货明细
            self.do_job(282)
            time.sleep(1)



    def test_1211(self):
        for i in range(10):
            self.add_apply_order()
            time.sleep(1)


    def test_chenglian(self):
        #橙联测试环境鉴权
        #复制URL到浏览器拿到code
        url = 'https://openapi-stage-cn.orangeconnex.com/oauth/authorize?response_type=code&client_id=366f321f-a8dd-4da3-8169-ac8a05e80fe2&redirect_uri=https://sysmall.smallrig.com&state=asd484@qq.com'
        #替换code
        code = 'D%252BpIxS5PDIZtaR1owBw1wLqiRC0VYvH%252FDYnlPjKLAyp%252BIu1TA0%252FcgmZyPUsm4rPVxL2XWO6aOqmGaZagcikkB79nIt1G3i44CHn5JapwY8tUYogEBX%252F5cbOolcdct7WYJ5rlgqKlWjKkBvahzaLHBj4qfpSVyjF%252F3Zs6jJF2oQrC%252BeRvuc6aKIfuKyKT%252BtoAeYqdwfGa115Vq7y9825lrXBmo%252BQDmz5CAwZacvqzrJsYlEuJ4ZaCAN9CjcnhTbLN7rAG%252Bz0yVvd%252Fa8vDmKYFwLD2nj%252F5lbixa05ZK5CrM8bx%252FfKFLsp7c0ND2fyZuzNbNV4eca2OrrjZ6EBYmjdxfLSOfWyrWKep34iAXFLXnnKtcI9Uxqkd26KB8uNtXevnhf6%252FF%252FIY4sXKq44uG4WChcmarDDOOM5MQJRlk6E%252F8kBOLCSwBmrkw29YSxgdCq%252FyU0KXy%252BhCsXWf3GmxZgUl4dejDcZIlsL1XXDRDiGG3%252FXA7nEvn1CLAR51%252FcsFY5aIE4f81AqhSIK3m1KA1CZOERlrjr8c6LRuNEu3m%252BgcOEJePu%252BfqXaM96e9%252BQX%252BZn%252Ff5ByqeMottDt2%252FdwKhgjhaYm56cbD1aNxACZhXJ8WpdL9dUJGoiNU4gq4%252BuSm4A3moV%252BbJGThXg5UV%252FBGHCuD7DONJokhqqMwGSzqaPitK1c%253D'
        url = f'https://openapi-stage-cn.orangeconnex.com/oauth/token?grant_type=authorization_code&code={code}&redirect_uri=https://sysmall.smallrig.com&client_id=366f321f-a8dd-4da3-8169-ac8a05e80fe2'
        res =  requests.post(url = url)
        print(json.dumps(res.json()))
