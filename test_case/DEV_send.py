#!/usr/bin/python
import requests
import json,time,random
import requests
import datetime
import toucheng
'''测试打包复核-2c如果跑失败，可能是已发货列表不止1条数据'''
import datetime
import string

tomtime = datetime.datetime.now()+datetime.timedelta(days=1)
tomtimes = tomtime.strftime("%Y-%m-%d %H:%M:%S")
print(tomtimes)
# 获取当前时间
times=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# 转为时间数组
timeArray = time.strptime(times, "%Y-%m-%d %H:%M:%S")
# 转为时间戳
timeStamp = int(time.mktime(timeArray))
num = random.randint(1000000,1000000000)
orderSnSource = "SL" + str(num)+ str(num)+ str(num)

class RelyData(object):
    purchaseSn = None
    purchaseSn_id = None
    receivingGoogsSn = None

'''物流信息-测试'''

# logistics = "ZGYZ"
# expressTypeName = "中国邮政"
# logisticsServiceProviderCode = 'SZYZ'

#环境
# env = "test"
env = "uat"
# env = "dev"
# env = "ipo"

so_list=[]

'''渠道平台 抖音全球站渠道test,uat通用'''
#复核方式
status_type = 1
#渠道LEQI-MALL
# platformId = 60
# channelId = 159
#亚马逊
# platformId = 30
# channelId = 13
# #抖音-小店
platformId=53
channelId=130
#产品数量
orderQuantity = 2
# 创建一个字符串包含所有小写字母
letters = string.ascii_lowercase

#是否聚合
aggregate = 2
#循环次数
XH_t = 5
#商品个数
goods_t =3


'''ZHONGTONG,中通,ZTO_FW/SF-LUYUN,顺丰-陆运,SFEXPRESS_FW,SFCRD,顺丰次日达,SZSF/国内顺丰陆运-寄付,SF-2,SZSF/SF-DOUYIN-4,顺丰-特快-抖音,SF_FS'''

if env == "uat":
    '''物流信息-uat'''
    logistics = "ZHONGTONG"
    expressTypeName = "中通"
    logisticsServiceProviderCode = 'ZTO_FW'
    warehouseId = 57
    printId = "d3bcbc33f32f452eb5e8e48c3610556b"
    sync_url = "http://bereal.smallrig.net/smallrig-job-admin/jobinfo/trigger"
    sync_headers = {
        'Cookie': "XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d; _gcl_au=1.1.1445770930.1692086830; _fbp=fb.1.1692086830643.1704661399; _ga=GA1.1.825110043.1664445764; _ga_X64KPEGTYM=GS1.1.1695373981.11.1.1695374036.5.0.0; _SIGN_ON_token=%22eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5nemhlbiIsInVzZXJJZCI6IjQ1NyIsIm5pY2tOYW1lIjoi6buE6ZWHIiwidGltZXN0YW1wIjoxNjk2OTIwMzA4OTA1fQ.rlDARgQMUwjBdkhX_DwVtYDiqWejgcEoHjs9VnqTuk0%22; _SIGN_ON_userId=%22457%22; _SIGN_ON_userName=%22%E9%BB%84%E9%95%87%22",
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        'cache-control': "no-cache",
        'Postman-Token': "195590c1-447b-4a12-bc25-5dee36dacde0"
    }

elif env =="dev":
    warehouseId = 232
    logistics = "ZHONGTONG"
    expressTypeName = "中通"
    logisticsServiceProviderCode = 'ZTO_FW'
    printId = "47c707e1866c4dc98c31324f77110a99"
    sync_url = "http://192.168.133.209:19010/smallrig-job-admin/jobinfo/trigger"
    sync_headers = {
        'Cookie': "AMCV_8F99160E571FC0427F000101%40AdobeOrg=1585540135%7CMCIDTS%7C19503%7CMCMID%7C45405227628454493324255079471335081864%7CMCAAMLH-1685627999%7C11%7CMCAAMB-1685627999%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1685030399s%7CNONE%7CvVersion%7C4.4.0; XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d; private_content_version=fedbe008fa35da8a07f53cbc9acd69eb; apt.uid=AP-XD7ZED5OKDHG-2-1-1685015460765-99678589.0.2.3dd4a7a2-4d40-47ed-b87b-2fd6e9944077; NG_TRANSLATE_LANG_KEY=%22en%22; _SIGN_ON_token=%22eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5nemhlbiIs",
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        'cache-control': "no-cache",
        'Postman-Token': "195590c1-447b-4a12-bc25-5dee36dacde0"
    }

elif env =="test":
    warehouseId = 232
    logistics = "ZHONGTONG"
    expressTypeName = "中通"
    logisticsServiceProviderCode = 'ZTO_FW'
    printId = "8aba99e92e584f50b298cefb83af9b52"
    sync_url = "http://192.168.133.223:19010/smallrig-job-admin/jobinfo/trigger"
    sync_headers = {
        'Cookie': "AMCV_8F99160E571FC0427F000101%40AdobeOrg=1585540135%7CMCIDTS%7C19503%7CMCMID%7C45405227628454493324255079471335081864%7CMCAAMLH-1685627999%7C11%7CMCAAMB-1685627999%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1685030399s%7CNONE%7CvVersion%7C4.4.0; XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d; private_content_version=fedbe008fa35da8a07f53cbc9acd69eb; apt.uid=AP-XD7ZED5OKDHG-2-1-1685015460765-99678589.0.2.3dd4a7a2-4d40-47ed-b87b-2fd6e9944077; NG_TRANSLATE_LANG_KEY=%22en%22; _SIGN_ON_token=%22eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5nemhlbiIs",
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        'cache-control': "no-cache",
        'Postman-Token': "195590c1-447b-4a12-bc25-5dee36dacde0"
    }
elif env =="ipo":
    warehouseId = 57
    logistics = "ZHONGTONG"
    expressTypeName = "中通"
    logisticsServiceProviderCode = 'ZTO_FW'
    printId = "8aba99e92e584f50b298cefb83af9b52"
    sync_url = "http://192.168.133.234:19010/smallrig-job-admin/jobinfo/trigger"
    sync_headers = {
        'Cookie': "XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d; _SIGN_ON_token=%22eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5nemhlbiIsInVzZXJJZCI6IjQ1NyIsIm5pY2tOYW1lIjoi6buE6ZWHIiwidGltZXN0YW1wIjoxNzAzNzY3MTU3NzA0fQ.w_pF5N2DFNgMOVABGVSSYInFQ3ZoLEK_FJoZ0hiUH3A%22; _SIGN_ON_userId=%22457%22; _SIGN_ON_userName=%22%E9%BB%84%E9%95%87%22",
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        'cache-control': "no-cache",
        'Postman-Token': "195590c1-447b-4a12-bc25-5dee36dacde0"
    }


class Wms:
    def __init__(self):
        so_list = []
        self.login()
        AccessToken = getattr(RelyData, 'accessToken')
        UserId = getattr(RelyData, 'userId')
        self.urls = getattr(RelyData, 'url')
        self.headers = {
            "Content-Type": "application/json",
            "User-Id": UserId,
            "Access-Token": AccessToken,
            "system-code": "ERP"
        }


        # 选择10个随机字母
        random_letters = random.choices(letters, k=10)
        # 将随机字母列表转换为字符串
        result = ''.join(random_letters)
        self.Address1 = "龙华区民治街道樟坑2区999_" + result

        self.id = getattr(RelyData, 'purchaseSn_id')
        self.receivingGoogsSn = getattr(RelyData, 'receivingGoogsSn')

        self.item_MARKET = {'HZlechuang-PRO': 138, 'NPI-PRO': 127, 'OPM-Pro': 106, 'China-2B-Pro': 100, 'eBay-Pro(头程)': 98,
                'B2B-Pro(DBC)': 96, 'R&D-Pro': 92, 'SIOP-Pro': 91, 'Amazon-Public': 90, 'MKT-Pro': 11, 'China-Pro': 10,
                'Website-Pro': 9, 'B2B-Pro': 8, 'eBay-Pro': 7, 'Amazon-HYC-Pro': 6, 'Amazon-TY-Pro': 5,
                'Amazon-RM-Pro': 4, 'Amazon-SR-Pro': 3, 'Amazon-CF-Pro': 2, 'Amazon-AC-Pro': 1}

        self.urlF = self.urls + "/API/oms/saleOrder/v1/save"
        self.url2 = self.urls + '/API/oms/saleOrder/v1/list'
        self.url4 = self.urls + '/API/oms/order/v1/list'
        self.url7 = self.urls + '/API/wms/document-distribution/v1/queryDocumentDistributionPage'
        self.url9 = self.urls + "/API/wms/audit/v1/queryAuditDetails"
        self.url12 = self.urls + "/API/wms/documentsOut/v1/queryBagPage"
        self.url6 = self.urls + "/API/oms/order/v1/batchSubmit"
        self.url9_add = self.urls + "/API/wms/audit/v1/queryAuditSku"
        self.url_ShippingOrder = self.urls + '/API/oms/shippingNotice/v1/list'

    def test01(self):
        '''提交2c订单'''
        random_letters = random.choices(letters, k=10)
        result = ''.join(random_letters)
        Address2 = "龙华区民治街道樟坑2区999_" + result

        if aggregate==1:
            self.receiverAddress = self.Address1
        else:
            self.receiverAddress = Address2

        self.urlF = self.urls + "/API/oms/saleOrder/v1/save"
        # channelId = self.item
        ##2个sku
        payload={
            "platformId": platformId,
            "channelId": channelId,
            "orderAttribute": 1,
            "payTime": "2023-12-25 19:32:09",
            "showWeight": 0.112,
            "customerMessage": "买家留言",
            "serviceRemark": "客服备注",
            "saleOrderCost": {
                "paymentProofFile": {
                    "files": [
                        {
                            "name": "23432img-kxAdF1703504096583.pdf",
                            "url": "http://smallrig-pmd.oss-cn-shenzhen.aliyuncs.com/23432img-kxAdF1703504096583.pdf"
                        }
                    ]
                },
                "shippingFee": "",
                "totalFee": "200",
                "otherIncome": 0,
                "isPaid": "",
                "couponFee": "",
                "marketIncome": "",
                "actualShippingCost": "",
                "platformFee": "",
                "otherFee": "",
                "currency": "RMB",
                "platformCoupon": "",
                "useBalance": "",
                "warehouseFee": "",
                "total": "200"
            },
            "saleOrderAddress": {
                "customerId": "GH23432423",
                "customerName": "abe",
                "receiverName": "abe",
                "receiverTel": "18476691641",
                "receiverContinent": "大洋洲",
                "receiverCountryCode": "AU",
                "receiverCity": "深圳",
                "receiverRegion": "南山区",
                "receiverAddress": self.receiverAddress,
                "houseNumber": "1020",
                "customerEmail": "2607103304@qq.com",
                "receiverCompany": "深圳乐其",
                "receiverProvince": "广东",
                "receiverAddress2": "西丽街道波顿科技园2",
                "receiverPostcode": "2500"
            },
            "products": [
                {
                    "productCode": "1112",
                    "productId": 2589,
                    "productStatusName": "下架",
                    "productStatusId": 5,
                    "weight": 12,
                    "productName": "斯莫格EVF单反摄影监视器转接头快接管夹热靴配件相机连接件1112",
                    "selectNum": 0,
                    "newSelectNum": 1,
                    "scale": 1,
                    "externalSku": "1112",
                    "orderQuantity": 2,
                    "productCodeSys": "1112",
                    "productNameSys": "斯莫格EVF单反摄影监视器转接头快接管夹热靴配件相机连接件1112",
                    "saleOrderSysItems": [
                        {
                            "orderQuantity": 2,
                            "feeRatio": 1,
                            "productCode": "1112",
                            "productId": 2589,
                            "productName": "斯莫格EVF单反摄影监视器转接头快接管夹热靴配件相机连接件1112",
                            "productStatusId": 5,
                            "productStatusName": "下架",
                            "scale": 1,
                            "weight": 12
                        }
                    ],
                    "length": 1,
                    "price": "2.000",
                    "allPrice": "4.000",
                    "unitProductPrice": 2,
                    "productQuantity": 1,
                    "orderSnSource": "",
                    "sourceCode": ""
                },
                {
                    "productCode": "1986C",
                    "productId": 1888,
                    "productStatusName": "下架",
                    "productStatusId": 5,
                    "weight": 100,
                    "productName": "SmallRig Sony A6500 Camera Accessory Kit 1986",
                    "selectNum": 0,
                    "newSelectNum": 1,
                    "scale": 1,
                    "externalSku": "1986C",
                    "orderQuantity": 2,
                    "productCodeSys": "1986C",
                    "productNameSys": "SmallRig Sony A6500 Camera Accessory Kit 1986",
                    "saleOrderSysItems": [
                        {
                            "orderQuantity": 2,
                            "feeRatio": 1,
                            "productCode": "1986C",
                            "productId": 1888,
                            "productName": "SmallRig Sony A6500 Camera Accessory Kit 1986",
                            "productStatusId": 5,
                            "productStatusName": "下架",
                            "scale": 1,
                            "weight": 100
                        }
                    ],
                    "length": 1,
                    "price": "2.000",
                    "allPrice": "4.000",
                    "unitProductPrice": 2,
                    "productQuantity": 1,
                    "orderSnSource": "",
                    "sourceCode": ""
                }
            ],
            "saleOrderItem": [
                {
                    "productCode": "1112",
                    "productId": 2589,
                    "productStatusName": "下架",
                    "productStatusId": 5,
                    "weight": 12,
                    "productName": "斯莫格EVF单反摄影监视器转接头快接管夹热靴配件相机连接件1112",
                    "selectNum": 0,
                    "newSelectNum": 1,
                    "scale": 1,
                    "externalSku": "1112",
                    "orderQuantity": 2,
                    "productCodeSys": "1112",
                    "productNameSys": "斯莫格EVF单反摄影监视器转接头快接管夹热靴配件相机连接件1112",
                    "saleOrderSysItems": [
                        {
                            "orderQuantity": 2,
                            "feeRatio": 1,
                            "productCode": "1112",
                            "productId": 2589,
                            "productName": "斯莫格EVF单反摄影监视器转接头快接管夹热靴配件相机连接件1112",
                            "productStatusId": 5,
                            "productStatusName": "下架",
                            "scale": 1,
                            "weight": 12
                        }
                    ],
                    "length": 1,
                    "price": "2.000",
                    "allPrice": "4.000",
                    "unitProductPrice": 2,
                    "productQuantity": 1,
                    "orderSnSource": "",
                    "sourceCode": ""
                },
                {
                    "productCode": "1986C",
                    "productId": 1888,
                    "productStatusName": "下架",
                    "productStatusId": 5,
                    "weight": 100,
                    "productName": "SmallRig Sony A6500 Camera Accessory Kit 1986",
                    "selectNum": 0,
                    "newSelectNum": 1,
                    "scale": 1,
                    "externalSku": "1986C",
                    "orderQuantity": 2,
                    "productCodeSys": "1986C",
                    "productNameSys": "SmallRig Sony A6500 Camera Accessory Kit 1986",
                    "saleOrderSysItems": [
                        {
                            "orderQuantity": 2,
                            "feeRatio": 1,
                            "productCode": "1986C",
                            "productId": 1888,
                            "productName": "SmallRig Sony A6500 Camera Accessory Kit 1986",
                            "productStatusId": 5,
                            "productStatusName": "下架",
                            "scale": 1,
                            "weight": 100
                        }
                    ],
                    "length": 1,
                    "price": "2.000",
                    "allPrice": "4.000",
                    "unitProductPrice": 2,
                    "productQuantity": 1,
                    "orderSnSource": "",
                    "sourceCode": ""
                }
            ],
            "timestamp": timeStamp
        }
        return self.urlF,payload

    def test04(self,orderNo):
        '''发货订单列表-获取数据id'''
        self.url4 = self.urls + '/API/oms/order/v1/list'
        payload ={"pageSize":15,"pageNum":1,"createTimeArr":["2022-12-07 00:00:00","2053-03-06 23:59:59"],"name":orderNo,"beginDate":"2022-12-07 00:00:00","endDate":"2053-03-06 23:59:59","codeType":2,"codeMode":1,"logisticsStatus":0,"timestamp":timeStamp}
        return self.url4, payload

    def test05(self):
        '''2c发货订单列表-标记不查询平台状态'''
        FhorderId = getattr(RelyData, 'FhorderId')
        self.url5 = self.urls + '/API/oms/order/v1/batchCancelPlatformStatus'
        payload = [FhorderId]
        return self.url5, payload

    def test06_submit(self):
        '''发货订单列表-提交操作'''
        FhorderId = getattr(RelyData, 'FhorderId')
        self.url6 = self.urls + '/API/oms/order/v1/batchSubmit'
        params = {
            'orderIds': FhorderId,
        }
        json_data = {
            'timestamp': timeStamp,
        }
        response = requests.post(self.url6, params=params,
                                 headers=self.headers, json=json_data, verify=False)
        print(url + "  \n  %s" % response.text)

    def test06(self):
        '''2c发货订单列表-审单操作'''
        FhorderId = getattr(RelyData, 'FhorderId')
        self.url6 = self.urls + '/API/oms/order/v1/audit'
        payload = {"warehouseId": warehouseId, "logistics": logistics, "hasMagento": False,
                   "showReceiverRegion": False, "expressType": logistics, "expressTypeName": expressTypeName,
                   "ids": [FhorderId], "timestamp": timeStamp}
        print("payload %s" %payload)
        return self.url6, payload

    def test06_ShippingOrder(self):
        '''订单进入wms,2c订单已分配列表-获取id'''
        sourceNo = so_list[0]
        print("sourceNo :%s "%sourceNo)
        self.url_ShippingOrder = self.urls + '/API/oms/shippingNotice/v1/list'
        payload = dict({"pageSize":15,"pageNum":1,"sourceNo":sourceNo,"shippingStatus":0,"timestamp":timeStamp})
        return self.url_ShippingOrder, payload

    def test07(self,order_DistributionLowerShelf=None):
        '''订单进入wms,2c订单已分配列表-获取id'''
        if aggregate==1:
            orderCode = so_list[0]
        else:
            orderCode=order_DistributionLowerShelf
        self.url7 = self.urls + '/API/wms/document-distribution/v1/queryDocumentDistributionPage'
        payload = {"pageSize":50,"pageNum":1,"orderCode":orderCode,"skuTypeCountCriteriaValue":"","outOfStockMark":"","orderTag":2,"statusList":[2],"warehouseId":"","warehouseIds":[],"mode":"","logisticsServices":None,"shippingIds":None,"distributionType":"","customerServiceRemarksFlag":"","documentsNos":"","totalWeightBegin":"","totalWeightEnd":"","marketId":"","channelId":"","skuCode":"","skuCountCriteria":"","skuCountCriteriaValue":"","skuTypeCountCriteria":"","timeType":1,"orderTimeArr":[],"createTimeBegin":"2023-11-27 00:00:00","createTimeEnd":"2056-12-27 23:59:59","createTimeArr":["2023-11-27 00:00:00","2056-12-27 23:59:59"],"referenceNo":"","receiverCountryCode":"","trackingNumber":"","receiverName":""}
        print("test07:%s " % payload)
        return self.url7, payload

    def test08(self):
        '''订单进入wms,2c订单已分配列表-进行下架'''
        XJorderid = getattr(RelyData, 'XJorderid')
        self.url8 = self.urls + '/API/wms/document-distribution/v1/DistributionLowerShelf'
        payload = {"userPosition":"","distributionUser":"袁浩","ids":[XJorderid],"mode":1}
        return self.url8, payload

    def test_add01(self,documentsNo=None):
        '''开始拣货'''
        if documentsNo==None:
            documentsNo = getattr(RelyData, 'documentsNo')
        print("documentsNo :" + documentsNo)
        self.add01 = self.urls + '/API/wms/documentsPick/v1/startPick'
        payload = {"actualPicker":"张森锋","documentsNo":"","documentsDistributionNo":documentsNo}
        return self.add01, payload

    def test_add02(self,documentsNo=None):
        '''结束拣货'''
        if documentsNo == None:
            documentsNo = getattr(RelyData, 'documentsNo')
        self.add02 = self.urls + '/API/wms/documentsPick/v1/finishPick'
        payload = {"actualPicker":"张森锋","documentsNo":"","documentsDistributionNo":documentsNo}
        return self.add02, payload

    def test09(self,documentsNo=None):
        '''订单进入wms,2c复核-扫描物件'''
        '''扫描物件'''
        if documentsNo == None:
            documentsNo = getattr(RelyData, 'documentsNo')
        # referenceNo = getattr(RelyData, 'referenceNo')

        print('\033[33m documentsNo: %s  \033[0m' % documentsNo )
        # print('\033[33m referenceNo: %s  \033[0m' % referenceNo )

        self.url9 = self.urls + "/API/wms/audit/v1/queryAuditDetails"
        querystring = {"no":documentsNo,"type":"ONCE","printId":"47c707e1866c4dc98c31324f77110a99"}
        # querystring = {"no": "WPH202312272132220003", "type": "ONCE", "printId": printId}
        print("test09 %s" % querystring)
        # payload = "no=%s&type=ONCE&printId=%s&undefined=" % (documentsNo, printId)
        payload=""
        methon = 'GET'
        return self.url9, payload, methon, querystring

    def test09_add(self):
        '''订单进入wms,2c复核-扫描物件获取sku、数量'''
        '''扫描物件'''
        documentsPickDetailsId = getattr(RelyData, 'documentsPickDetailsId')
        documentsPickId = getattr(RelyData, 'documentsPickId')
        self.url9_add = self.urls + "/API/wms/audit/v1/queryAuditSku"
        querystring = {"documentsPickId": documentsPickId, "documentsPickDetailsId": documentsPickDetailsId}
        payload = ""
        methon = 'GET'
        return self.url9_add, payload, methon, querystring

    def test10(self):
        '''批量复核'''
        documentsPickDetailsId = getattr(RelyData, 'documentsPickDetailsId')
        documentsPickId = getattr(RelyData, 'documentsPickId')
        sku_dict = getattr(RelyData, 'sku_dict')
        self.url10 = self.urls + "/API/wms/audit/v1/auditSku"
        for key, value in sku_dict.items():
            skuNum_1 = value
            skucode = key
            payload = {"packageUser":"黄镇","auditNum":skuNum_1,"documentsPickDetailsId":documentsPickDetailsId,"documentsPickId":documentsPickId,"functionBars":[{"type":"pack","status":status_type,"disabled":False},{"type":"print_documents","status":0,"disabled":True},{"type":"print_label","status":0,"disabled":True}],"skuCode":skucode,"printId":printId,"type":"ONCE"}
            wms.requets_abe(self.url10,payload)

    def test11(self,documentsNo=None):
        '''称重'''
        if documentsNo == None:
            documentsNo = getattr(RelyData, 'documentsNo')
        self.url11 = self.urls + "/API/wms/documentsOut/v1/weighOut"
        payload = {"hight":2,"length":2,"relationDocumentsNo":documentsNo,"weight":1.01,"width":2,"totalWeightView":0,"orderTag":None}
        return self.url11, payload

    def test12(self,documentsNo=None):
        '''装袋列表获取-获取装袋id'''
        if documentsNo == None:
            documentsNo = getattr(RelyData, 'documentsNo')
        self.url12 = self.urls + "/API/wms/documentsOut/v1/queryBagPage"
        payload = {"pageSize":2000,"pageNum":1,"trackStatus":False,"trackingNumber":"","relationDocumentsNo":documentsNo,"weighStatus":2,"warehouseIds":[],"shippingId":logistics,"logisticsServiceProviderCode":logisticsServiceProviderCode}
        return self.url12, payload

    def test13(self):
        '''装袋'''
        ZDorderId = getattr(RelyData, 'ZDorderId')
        self.url13 = self.urls + "/API/wms/documentsOut/v1/createBatch"
        payload = [ZDorderId]
        return self.url13, payload

    def test16(self):
        '''自动分仓定时器'''
        if env == "test":
            payload = "id=72&executorParam=&addressList="
        elif env=="ipo":
            payload = "id=70&executorParam=&addressList="
        elif env=="uat":
            payload = "id=70&executorParam=&addressList="
        response = requests.request("POST", sync_url, data=payload, headers=sync_headers)
        return response

    def requets_abe(self,url,payload,methon='POST',querystring=None,order_no=None,):
        if methon == 'POST':
            payload = json.dumps(payload)
            if url == self.url6:
                orderStatus = getattr(RelyData, 'orderStatus')
                if orderStatus == 2:
                    response = requests.request(methon, url, data=payload, headers=self.headers)
                    print(url + "  \n  %s" % response.text)
                else:
                    pass
            else:
                response = requests.request(methon, url, data=payload, headers=self.headers)
                if url!=self.url4:
                    print(url + "  \n  %s" % response.text)
        else:
            response = requests.request("GET", url, headers=self.headers, params=querystring)
            print(url + "  \n  %s" % response.text)

        #订单为草稿时，获取订单id,用来提交订单

        if url == self.urlF:
            responsejson = response.json()
            orderNo = responsejson['data']['orderNo']
            so_list.append(orderNo)
            print("so_list: %s" % so_list)
            setattr(RelyData, "orderNo", orderNo)

        if url == self.url2:
            responsejson = response.json()
            id = responsejson['data']['items'][0]['id']
            setattr(RelyData, "orderId", id)

        if url == self.url_ShippingOrder:
            responsejson = response.json()
            i=1
            while i<5:
                i+=1
                try:
                    sourceNoList = responsejson['data']['items'][0]['sourceNoList']
                except:
                    sourceNoList = []
                # 校验长度是不是跟创建的一样
                if sourceNoList != []:
                    sourceNoList = str(sourceNoList).split(",")
                    sourceNoList_long = len(sourceNoList)
                    so_list_long = len(so_list)
                    if so_list_long != sourceNoList_long:
                        print("so_list_long:%s   sourceNoList_long :%s" % (so_list_long, sourceNoList_long))
                        time.sleep(1)
                        # 执行合单操作
                        self.excutecode_aotomerge()
                        responsejson = requests.request(methon, url, data=payload, headers=self.headers)
                    else:
                        break
                else:
                    self.excutecode_aotomerge()
                    responsejson = requests.request(methon, url, data=payload, headers=self.headers)

        if url == self.url6:
            start_time = time.time()
            while True:
                url4 = self.test04(order_no)[0]
                payload4 = self.test04(order_no)[1]
                self.requets_abe(url4,payload4)
                orderStatus = getattr(RelyData, 'orderStatus')
                wms.test16()
                if orderStatus == 2:
                    end_time = time.time()
                    execution_time = end_time - start_time
                    print('\033[35m ============================状态草稿-->待审核: %s  ========================== \033[0m'% execution_time)
                    response = requests.request(methon, url, data=payload, headers=self.headers)
                    print(url + "  \n  %s" % response.text)
                    break
                else:
                    pass

        #2c订单发货列表，订单审核前获取订单id
        if url == self.url4:
            while True:
                responsejson = response.json()
                try:
                    itmes = responsejson['data']['items']
                except:
                    itmes=[]
                if itmes == []:
                    # print('数据同步发货订单列表,请稍等。。。')
                    time.sleep(1)
                    wms.test16()
                    response = requests.request(methon, url, data=payload, headers=self.headers)
                else:
                    break
            id = responsejson['data']['items'][0]['id']
            setattr(RelyData, "FhorderId", id)
            orderCode = responsejson['data']['items'][0]['orderCode']
            orderStatus = responsejson['data']['items'][0]['orderStatus']
            setattr(RelyData, "orderCode", orderCode)
            setattr(RelyData, "orderStatus", orderStatus)

        # 2c订单发货列表，已分配后获取id,用来下架
        if url == self.url7:
            while True:
                responsejson = response.json()
                records = responsejson['data']['records']
                if records == []:
                    self.excutecode_aotomerge()
                    self.excutecode_PushtoWMS()
                    print('数据同步发货订单列表中，请稍等。。。')
                    time.sleep(1)
                    response = requests.request(methon, url, data=payload, headers=self.headers)
                else:
                    break
            XJorderid = responsejson['data']['records'][0]['id']
            documentsNo = responsejson['data']['records'][0]['documentsNo']
            referenceNo = responsejson['data']['records'][0]['referenceNo']
            setattr(RelyData, "XJorderid", XJorderid)
            setattr(RelyData, "documentsNo", documentsNo)
            setattr(RelyData, "referenceNo", referenceNo)

        #获取扫描后的参数
        if url == self.url9:
            responsejson = response.json()
            documentsPickId = responsejson['data']['documentsPickId']
            documentsPickDetailsId = responsejson['data']['documentsPickDetailsId']
            setattr(RelyData, "documentsPickId", documentsPickId)
            setattr(RelyData, "documentsPickDetailsId", documentsPickDetailsId)

        if url == self.url9_add:
            responsejson = response.json()
            sku_len = responsejson['data']['auditSku']
            sku_dict={}
            for i in range(sku_len):
                skuNum_a = responsejson['data']['auditSku'][i]["skuNum"]
                skuNum_code_a = responsejson['data']['auditSku'][i]["skuCode"]
                sku_dict["skuNum_1_code"] = skuNum_a
            skuNum_1 = responsejson['data']['auditSku'][0]["skuNum"]
            setattr(RelyData, "skuNum_1", skuNum_1)
            setattr(RelyData, "sku_dict", sku_dict)

        if url == self.url12:
            responsejson = response.json()
            ZDorderId = responsejson['data']['records'][0]['id']
            setattr(RelyData, "ZDorderId", ZDorderId)

    def excutecode_aotomerge(self):
        #test定时器
        if env == "test":
            #自动分仓
            print("执行定时器test。。。 ")
            url = sync_url
            payload = "id=556&executorParam=&addressList="
            headers = {
                'Cookie': "XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d",
                'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
                'cache-control': "no-cache",
                'Postman-Token': "195590c1-447b-4a12-bc25-5dee36dacde0"
            }
        elif env == "uat":
            #合单
            print("执行定时器test。。。 ")
            url = sync_url
            payload = "id=559&executorParam=&addressList="
            headers = {
                'Cookie': "XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d; _ga=GA1.1.825110043.1664445764; _ga_X64KPEGTYM=GS1.1.1695373981.11.1.1695374036.5.0.0; _SIGN_ON_token=%22eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5nemhlbiIsInVzZXJJZCI6IjQ1NyIsIm5pY2tOYW1lIjoi6buE6ZWHIiwidGltZXN0YW1wIjoxNzA0NTM2ODg0NDcwfQ.yQpHx5HHX_btQWIUsQDcsgBkrhH6JMX9J1EAWpYHwmk%22; _SIGN_ON_userId=%22457%22; _SIGN_ON_userName=%22%E9%BB%84%E9%95%87%22",
                'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
                'cache-control': "no-cache",
                'Postman-Token': "195590c1-447b-4a12-bc25-5dee36dacde0"
            }
        else:
            url = sync_url
            payload = "id=556&executorParam=&addressList="
            headers = {
                'Cookie': "XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d; _SIGN_ON_token=%22eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5nemhlbiIsInVzZXJJZCI6IjQ1NyIsIm5pY2tOYW1lIjoi6buE6ZWHIiwidGltZXN0YW1wIjoxNzAzNzY3MTU3NzA0fQ.w_pF5N2DFNgMOVABGVSSYInFQ3ZoLEK_FJoZ0hiUH3A%22; _SIGN_ON_userId=%22457%22; _SIGN_ON_userName=%22%E9%BB%84%E9%95%87%22",
                'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
                'cache-control': "no-cache",
                'Postman-Token': "195590c1-447b-4a12-bc25-5dee36dacde0"
            }
        response = requests.request("POST", url, data=payload, headers=headers)
        print("自动合单任务执行： %s" % response)

    def login(self):
        import requests
        if env=="test":
            cookies = {
                'AMCV_8F99160E571FC0427F000101%40AdobeOrg': '1585540135%7CMCIDTS%7C19503%7CMCMID%7C45405227628454493324255079471335081864%7CMCAAMLH-1685627999%7C11%7CMCAAMB-1685627999%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1685030399s%7CNONE%7CvVersion%7C4.4.0',
                'XXL_JOB_LOGIN_IDENTITY': '7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d',
                'private_content_version': '42daf4c53bf2104a60bd1fcbf05765fe',
                'apt.uid': 'AP-XD7ZED5OKDHG-2-1-1705659007977-52264664.0.2.9652f9cb-e54d-44ba-b0d2-aa0ae1ba6d5e',
            }

            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Access-Token': '',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json;charset=UTF-8',
                # Requests sorts cookies= alphabetically
                # 'Cookie': 'AMCV_8F99160E571FC0427F000101%40AdobeOrg=1585540135%7CMCIDTS%7C19503%7CMCMID%7C45405227628454493324255079471335081864%7CMCAAMLH-1685627999%7C11%7CMCAAMB-1685627999%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1685030399s%7CNONE%7CvVersion%7C4.4.0; XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d; private_content_version=42daf4c53bf2104a60bd1fcbf05765fe; apt.uid=AP-XD7ZED5OKDHG-2-1-1705659007977-52264664.0.2.9652f9cb-e54d-44ba-b0d2-aa0ae1ba6d5e',
                'Origin': 'http://192.168.133.223:8888',
                'Referer': 'http://192.168.133.223:8888/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'User-Id': '',
                'system-code': 'XTZX_MAIN',
            }
            json_data = {
                'systemCode': 'XTZX_MAIN',
                'username': 'abe01',
                'password': 'dc0f68a78817d8dbc94528b49afde9a5',
                '_t': 1706674076224,
            }
            response = requests.post('http://192.168.133.223:8888/API/manage/login', cookies=cookies, headers=headers,
                         json=json_data, verify=False)
            url = "http://192.168.133.223:8888"

        elif env=="uat":
            import requests
            cookies = {
                '_ga': 'GA1.1.825110043.1664445764',
                '_ga_X64KPEGTYM': 'GS1.1.1695373981.11.1.1695374036.5.0.0',
            }

            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Access-Token': '',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json;charset=UTF-8',
                # Requests sorts cookies= alphabetically
                # 'Cookie': '_ga=GA1.1.825110043.1664445764; _ga_X64KPEGTYM=GS1.1.1695373981.11.1.1695374036.5.0.0',
                'Origin': 'http://sysmall.smallrig.net',
                'Referer': 'http://sysmall.smallrig.net/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'User-Id': '',
                'system-code': 'XTZX_MAIN',
            }

            json_data = {
                'systemCode': 'XTZX_MAIN',
                'username': 'abe01',
                'password': 'dc0f68a78817d8dbc94528b49afde9a5',
                '_t': 1706674238648,
            }

            response = requests.post('http://sysmall.smallrig.net/API/manage/login', cookies=cookies, headers=headers,
                                     json=json_data, verify=False)
            url = "http://sysmall.smallrig.net"
        else:
            import requests

            cookies = {
                'XXL_JOB_LOGIN_IDENTITY': '7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d',
            }

            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Access-Token': '',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json;charset=UTF-8',
                # 'Cookie': 'XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d',
                'Origin': 'http://192.168.133.234:8888',
                'Referer': 'http://192.168.133.234:8888/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'User-Id': '',
                'system-code': 'XTZX_MAIN',
            }

            json_data = {
                'systemCode': 'XTZX_MAIN',
                'username': 'huangzhen',
                'password': 'dc0f68a78817d8dbc94528b49afde9a5',
                '_t': 1706947239231,
            }

            response = requests.post('http://192.168.133.234:8888/API/manage/login', cookies=cookies, headers=headers,
                                     json=json_data, verify=False)
            url = "http://192.168.133.234:8888"

        responsejson = response.json()
        accessToken = responsejson['data']['accessToken']
        userId = responsejson['data']['userId']
        setattr(RelyData, "accessToken", accessToken)
        setattr(RelyData, "userId", userId)
        setattr(RelyData, "url", url)

        return accessToken,userId

    def excutecode_PushtoWMS(self):
        # test定时器
        if env == "test":
            # 推送wms
            print("执行定时器test。。。 ")
            url = sync_url
            payload = "id=557&executorParam=&addressList="
            headers = {
                'Cookie': "XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d",
                'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
                'cache-control': "no-cache",
                'Postman-Token': "195590c1-447b-4a12-bc25-5dee36dacde0"
            }
        elif env == "uat":
            # 推送wms
            print("执行定时器test。。。 ")
            url = sync_url
            payload = "id=560&executorParam=&addressList="
            headers = {
                'Cookie': "XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d",
                'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
                'cache-control': "no-cache",
                'Postman-Token': "195590c1-447b-4a12-bc25-5dee36dacde0"
            }
        else:
            url = sync_url
            payload = "id=557&executorParam=&addressList="
            headers = {
                'Cookie': "XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d; _SIGN_ON_token=%22eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5nemhlbiIsInVzZXJJZCI6IjQ1NyIsIm5pY2tOYW1lIjoi6buE6ZWHIiwidGltZXN0YW1wIjoxNzAzNzY3MTU3NzA0fQ.w_pF5N2DFNgMOVABGVSSYInFQ3ZoLEK_FJoZ0hiUH3A%22; _SIGN_ON_userId=%22457%22; _SIGN_ON_userName=%22%E9%BB%84%E9%95%87%22",
                'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
                'cache-control': "no-cache",
                'Postman-Token': "195590c1-447b-4a12-bc25-5dee36dacde0"
            }
        response = requests.request("POST", url, data=payload, headers=headers)
        print(response)

if __name__=="__main__":
    for i in range(1,2):
        wms = Wms()
        wms.login()
        so_list=[]
        try:
            #提交2c订单
            for j in range(1):
                url = wms.test01()[0]
                payload = wms.test01()[1]
                wms.requets_abe(url, payload)
            #发货订单列表-审单操作
            for i in so_list:
                # 2c发货订单列表-获取数据id
                print(i)
                url = wms.test04(i)[0]
                payload = wms.test04(i)[1]
                wms.requets_abe(url, payload)
                # 2c发货订单列表-标记不查询平台状态
                url = wms.test05()[0]
                payload = wms.test05()[1]
                wms.requets_abe(url, payload)
                # 2c发货订单列表-提交操作
                start_time = time.time()
                wms.test06_submit()
                # 自动分仓操作
                wms.test16()

                # 审单操作
                url = wms.test06()[0]

                payload = wms.test06()[1]
                wms.requets_abe(url, payload, order_no=i)

            # 执行合单
            time.sleep(3)
            wms.excutecode_aotomerge()

            # 检查所有单是否都同步到了发货通知单列表
            url = wms.test06_ShippingOrder()[0]
            payload = wms.test06_ShippingOrder()[1]
            wms.requets_abe(url, payload)

            # 执行推送
            wms.excutecode_PushtoWMS()

            #订单进入wms,2c订单已分配列表-进行下架
            if aggregate == 2:
                for i in so_list:
                    # 订单进入wms,2c订单已分配列表-获取id
                    url = wms.test07(i)[0]
                    payload = wms.test07(i)[1]
                    wms.requets_abe(url, payload)
                    # 下架
                    url = wms.test08()[0]
                    payload = wms.test08()[1]
                    wms.requets_abe(url, payload)
                    # 开始拣货
                    url = wms.test_add01()[0]
                    payload = wms.test_add01()[1]
                    wms.requets_abe(url, payload)

                    # 完成拣货
                    url = wms.test_add02()[0]
                    payload = wms.test_add02()[1]
                    wms.requets_abe(url, payload)
                    #
                    # 订单进入wms,2c复核-扫描物件
                    url = wms.test09()[0]
                    payload = wms.test09()[1]
                    methon = wms.test09()[2]
                    querystring = wms.test09()[3]
                    wms.requets_abe(url, payload, methon, querystring)

                    # 订单进入wms,2c复核-扫描物件
                    url = wms.test09_add()[0]
                    payload = wms.test09_add()[1]
                    methon = wms.test09_add()[2]
                    querystring = wms.test09_add()[3]
                    wms.requets_abe(url, payload, methon, querystring)

                    # #复核
                    url = wms.test10('1112')[0]
                    payload = wms.test10('1112')[1]
                    wms.requets_abe(url, payload)
                    #
                    # 复核
                    url = wms.test10('1986C')[0]
                    payload = wms.test10('1986C')[1]
                    wms.requets_abe(url, payload)
                    #
                    ##称重
                    url = wms.test11()[0]
                    payload = wms.test11()[1]
                    wms.requets_abe(url, payload)
                    # #
                    # 获取装袋id
                    url = wms.test12()[0]
                    payload = wms.test12()[1]
                    wms.requets_abe(url, payload)

                    #装袋
                    url = wms.test13()[0]
                    payload = wms.test13()[1]
                    wms.requets_abe(url, payload)
                    print('\033[35m ============================执行结束========================== \033[0m')
                    print('\033[35m ============================执行结束========================== \033[0m')
                    print('\033[35m ============================执行结束========================== \033[0m')
                    print('\033[35m ============================执行结束========================== \033[0m')
                    print('\033[35m ============================执行结束========================== \033[0m')
                    so_list = []
            else:
                # 查询已分配列表
                url = wms.test07()[0]
                payload = wms.test07()[1]
                wms.requets_abe(url, payload)

                url = wms.test08()[0]
                payload = wms.test08()[1]
                wms.requets_abe(url, payload)
                # 开始拣货
                url = wms.test_add01()[0]
                payload = wms.test_add01()[1]
                wms.requets_abe(url, payload)

                # 完成拣货
                url = wms.test_add02()[0]
                payload = wms.test_add02()[1]
                wms.requets_abe(url, payload)

                # 订单进入wms,2c复核-扫描物件
                url = wms.test09()[0]
                payload = wms.test09()[1]
                methon = wms.test09()[2]
                querystring = wms.test09()[3]
                wms.requets_abe(url, payload, methon, querystring)
                #
                # 订单进入wms,2c复核-扫描物件
                url = wms.test09_add()[0]
                payload = wms.test09_add()[1]
                methon = wms.test09_add()[2]
                querystring = wms.test09_add()[3]
                wms.requets_abe(url, payload, methon, querystring)
                #
                # #复核
                url = wms.test10('1112')[0]
                payload = wms.test10('1112')[1]
                wms.requets_abe(url, payload)
                #
                # 复核
                url = wms.test10('1986C')[0]
                payload = wms.test10('1986C')[1]
                wms.requets_abe(url, payload)

                ##称重
                url = wms.test11()[0]
                payload = wms.test11()[1]
                wms.requets_abe(url, payload)
                #
                #获取装袋id
                url = wms.test12()[0]
                payload = wms.test12()[1]
                wms.requets_abe(url, payload)

                # 装袋
                url = wms.test13()[0]
                payload = wms.test13()[1]
                wms.requets_abe(url, payload)

                print('\033[35m ============================执行结束========================== \033[0m')
                print('\033[35m ============================执行结束========================== \033[0m')
                print('\033[35m ============================执行结束========================== \033[0m')
                print('\033[35m ============================执行结束========================== \033[0m')
                print('\033[35m ============================执行结束========================== \033[0m')
                so_list = []
        except Exception as e:
            print(e)
            print("跳过这次循环")
            # continue















