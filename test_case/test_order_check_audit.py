import unittest
import requests,json
# from common.base.handle_yaml import HandleYaml
# from common.base.handle_mysql import HandleMysql
from test_suite.test_pc import PC

import importlib,sys

importlib.reload(sys)


class Order(unittest.TestCase):


    def setUp(self):
        print('start {}'.format(self))
    def edit_order_de09(self,customerEmail="314221719@qq.com",receiverName="李先生收件人",receiverCompany="公司名",receiverCountryCode="US",receiverProvince="广东省省",receiverCity="深圳市市",receiverPostcode="邮编",receiverTel="12345678901",receiverAddress="地址1粤海街道学府路6号厚德品园A座21C",receiverAddress2="地址2",receiverRegion="收货地区",houseNumber="门牌号"):
        """""
        品晟德国法兰(DE09)仓-LeqiMall   邮编

        """
        print("品晟德国法兰(DE09)仓-LeqiMall")
        url = 'http://192.168.133.223:5555/API/oms/order/v1/update'
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,sq;q=0.7,ar;q=0.6,an;q=0.5',
            'Access-Token': 'eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5naGFpIiwidXNlcklkIjoiNTM2Iiwibmlja05hbWUiOiLpu4TmtbciLCJ0aW1lc3RhbXAiOjE2OTI1ODI1OTI1NTJ9.6L0QYBNei99xesfFMVvnspf8Spbm7F16EcBZvtNTzKo',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Cookie': '...',
            'Origin': 'http://192.168.133.223:5555',
            'Referer': 'http://192.168.133.223:5555/YWZT/order/manager/orderEdit?id=5842246&orderCode=SO23081701229',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'User-Id': '536',
            'system-code': 'ERP'
        }
        data = {
        "id":5842246,
        "orderType":1,
        "orderCode":"SO23081701229",
        "platformId":47,
        "warehouseId":154,
        "marketId":10,
        "channelId":115,
        "orderSnSource":"1952730840937941589",
        "sourceCode":"1952730840937941589",
        "salesRecordNum":0,
        "transport":"express",
        "expressType":"123",
        "expressTypeName":"123",
        "productVarietyNum":1,
        "productTotalNum":1,
        "orderTime":"2023-08-17 20:18:55",
        "payTime":"2023-08-17 20:18:59",
        "sendTime":"",
        "customerMessage":"...........HAHA.哈哈。。。。。",
        "orderStatus":7,
        "flagsStatus":0,
        "auditTime":"2023-08-18 09:58:45",
        "auditOpinion":"修改收件人买家Email、收件人、",
        "auditPerson":"黄海",
        "source":1,
        "apiStatus":1,
        "pushFlag":0,
        "sendType":1,
        "isSubInventory":1,
        "isTagShip":1,
        "isWait":1,
        "waitTime":"2023-08-17 20:22:24",
        "waitStatus":0,
        "isShow":1,
        "cancelType":0,
        "problemType":0,
        "firstFinanceAuditTime":"2023-08-17 20:18:55",
        "delFlag":1,
        "createTime":"2023-08-17 20:22:24",
        "updateBy":"黄海",
        "updateTime":"2023-08-18 11:04:25",
        "customerEmail":"",
        "isAuditUnlock":0,
        "isEccangAudit":0,
        "orderCodes":"",
        "logisticsStatus":0,
        "signingTime":"",
        "warehouseName":"品晟德国法兰（DE09）仓-LeqiMall",
        "shippingWeight":0,
        "step":100,
        "ioss":"",
        "orderAttribute":1,
        "vatTaxNumber":"",
        "encryptStatus":0,
        "showWeight":31.501,
        "orderAddress":{
            "customerEmail":customerEmail,
            "receiverName":receiverName,
            "receiverCompany":receiverCompany,
            "receiverContinent":"北美洲",
            "receiverCountryCode":receiverCountryCode,
            "receiverProvince":receiverProvince,
            "receiverCity":receiverCity,
            "receiverPostcode":receiverPostcode,
            "receiverTel":receiverTel,
            "receiverAddress":receiverAddress,
            "receiverAddress2":receiverAddress2,
            "receiverRegion":receiverRegion,
            "houseNumber":houseNumber,
            "baseId":5842246,
            "id":7735627
        },
        "orderCost":{
            "id":7745184,
            "baseId":5842246,
            "totalFee":374.06,
            "cnyTotalFee":374.06,
            "platformFee":7.4812,
            "shippingFee":0,
            "actualShippingCost":0,
            "couponFee":24.94,
            "auditFee":0,
            "isPaid":1,
            "discountTotal":0,
            "exchangeRate":1,
            "currency":"RMB",
            "paymentMethods":"",
            "paymentAccount":"",
            "otherIncome":0,
            "platformCoupon":0,
            "marketIncome":374.06,
            "warehouseFee":0,
            "otherFee":0,
            "productTax":43.033,
            "shippingTax":0,
            "otherTax":0,
            "taxRate":0.13,
            "isInvoice":0,
            "useBalance":0,
            "delFlag":1,
            "createBy":"",
            "createTime":"2023-08-17 20:22:24",
            "updateBy":"",
            "updateTime":"2023-08-18 11:04:25",
            "total":374.06
        },
        "products":[
            {
                "id":12541507,
                "baseId":5842246,
                "externalSku":"4939273880401",
                "productName":"【礼遇价】SmallRig斯莫格适用于索尼A7R5/A7M4/A7S3 可折叠L型快装板sony相机配件3984",
                "unitProductPrice":399,
                "orderQuantity":1,
                "productQuantity":1,
                "realProductQuantity":0,
                "shippingPrice":0,
                "totalFee":399,
                "productRemark":"",
                "productGrade":0,
                "productType":0,
                "sourceCode":"1952730840937941589",
                "transactionId":"",
                "location":"",
                "platformItemId":"",
                "orderId":"",
                "orderTime":"2023-08-17 20:18:55",
                "delFlag":1,
                "createBy":"",
                "createTime":"2023-08-18 11:04:25",
                "updateBy":"",
                "updateTime":"2023-08-18 11:04:25",
                "sysItems":[
                    {
                        "id":69060908,
                        "baseId":5842246,
                        "itemId":12541507,
                        "productId":2066,
                        "productCode":"1128",
                        "externalSku":"4939273880401",
                        "productName":"三脚架固定板",
                        "productQuantity":1,
                        "realProductQuantity":1,
                        "scale":1,
                        "productStatusId":5,
                        "productStatusName":"下架",
                        "weight":31501,
                        "unitProductPrice":399,
                        "totalFee":399,
                        "feeRatio":1,
                        "totalWeight":31501,
                        "originalTotalFee":399,
                        "originalUnitPrice":399,
                        "delFlag":1,
                        "createBy":"",
                        "createTime":"2023-08-18 11:04:25",
                        "updateBy":"",
                        "updateTime":"2023-08-18 11:04:25",
                        "sourceCode":"",
                        "orderTime":"",
                        "productNum":"",
                        "diffWaitNum":"",
                        "imageUrl":""
                    }
                ],
                "incomeList":"",
                "orderSendTime":"",
                "orderChannelId":"",
                "platformStatus":"",
                "latestShipTime":"",
                "newSelectNum":1,
                "price":399,
                "disabled":"true",
                "allPrice":"399.000",
                "diff":"true"
            }
        ],
        "productsOld":[
            {
                "id":12541507,
                "baseId":5842246,
                "externalSku":"4939273880401",
                "productName":"【礼遇价】SmallRig斯莫格适用于索尼A7R5/A7M4/A7S3 可折叠L型快装板sony相机配件3984",
                "unitProductPrice":399,
                "orderQuantity":1,
                "productQuantity":1,
                "realProductQuantity":0,
                "shippingPrice":0,
                "totalFee":399,
                "productRemark":"",
                "productGrade":0,
                "productType":0,
                "sourceCode":"1952730840937941589",
                "transactionId":"",
                "location":"",
                "platformItemId":"",
                "orderId":"",
                "orderTime":"2023-08-17 20:18:55",
                "delFlag":1,
                "createBy":"",
                "createTime":"2023-08-18 11:04:25",
                "updateBy":"",
                "updateTime":"2023-08-18 11:04:25",
                "sysItems":[
                    {
                        "id":69060908,
                        "baseId":5842246,
                        "itemId":12541507,
                        "productId":2066,
                        "productCode":"1128",
                        "externalSku":"4939273880401",
                        "productName":"三脚架固定板",
                        "productQuantity":1,
                        "realProductQuantity":1,
                        "scale":1,
                        "productStatusId":5,
                        "productStatusName":"下架",
                        "weight":31501,
                        "unitProductPrice":399,
                        "totalFee":399,
                        "feeRatio":1,
                        "totalWeight":31501,
                        "originalTotalFee":399,
                        "originalUnitPrice":399,
                        "delFlag":1,
                        "createBy":"",
                        "createTime":"2023-08-18 11:04:25",
                        "updateBy":"",
                        "updateTime":"2023-08-18 11:04:25",
                        "sourceCode":"",
                        "orderTime":"",
                        "productNum":"",
                        "diffWaitNum":"",
                        "imageUrl":""
                    }
                ],
                "incomeList":"",
                "orderSendTime":"",
                "orderChannelId":"",
                "platformStatus":"",
                "latestShipTime":"",
                "newSelectNum":1,
                "price":399,
                "disabled":"true",
                "diff":"true"
            }
        ],
        "showReceiverRegion":"false",
        "platformName":"天猫",
        "orderItem":[
            {
                "id":12541507,
                "baseId":5842246,
                "externalSku":"4939273880401",
                "productName":"【礼遇价】SmallRig斯莫格适用于索尼A7R5/A7M4/A7S3 可折叠L型快装板sony相机配件3984",
                "unitProductPrice":399,
                "orderQuantity":1,
                "productQuantity":1,
                "realProductQuantity":0,
                "shippingPrice":0,
                "totalFee":399,
                "productRemark":"",
                "productGrade":0,
                "productType":0,
                "sourceCode":"1952730840937941589",
                "transactionId":"",
                "location":"",
                "platformItemId":"",
                "orderId":"",
                "orderTime":"2023-08-17 20:18:55",
                "delFlag":1,
                "createBy":"",
                "createTime":"2023-08-18 11:04:25",
                "updateBy":"",
                "updateTime":"2023-08-18 11:04:25",
                "sysItems":[
                    {
                        "id":69060908,
                        "baseId":5842246,
                        "itemId":12541507,
                        "productId":2066,
                        "productCode":"1128",
                        "externalSku":"4939273880401",
                        "productName":"三脚架固定板",
                        "productQuantity":1,
                        "realProductQuantity":1,
                        "scale":1,
                        "productStatusId":5,
                        "productStatusName":"下架",
                        "weight":31501,
                        "unitProductPrice":399,
                        "totalFee":399,
                        "feeRatio":1,
                        "totalWeight":31501,
                        "originalTotalFee":399,
                        "originalUnitPrice":399,
                        "delFlag":1,
                        "createBy":"",
                        "createTime":"2023-08-18 11:04:25",
                        "updateBy":"",
                        "updateTime":"2023-08-18 11:04:25",
                        "sourceCode":"",
                        "orderTime":"",
                        "productNum":"",
                        "diffWaitNum":"",
                        "imageUrl":""
                    }
                ],
                "incomeList":"",
                "orderSendTime":"",
                "orderChannelId":"",
                "platformStatus":"",
                "latestShipTime":"",
                "newSelectNum":1,
                "price":399,
                "disabled":"true",
                "allPrice":"399.000",
                "diff":"true"
            }
        ],
        "timestamp":1692328205000
    }
        print(data["orderAddress"])
        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
        print(response.text)
        return response
    def edit_order_la01(self,customerEmail="314221719@qq.com",receiverName="receiverName",receiverCompany="receiverCompany",receiverCountryCode="US",receiverProvince="广东省省",receiverCity="深圳市市",receiverPostcode="Postcode",receiverTel="12345678901",receiverAddress="地址1粤海街道学府路6号厚德品园A座21C",receiverAddress2="地址2",receiverRegion="收货地区",houseNumber="门牌号"):
        """""
        品晟美国洛杉矶(LA01）仓-LeqiMall

        """
        print("品晟美国洛杉矶(LA01）仓-LeqiMall")
        url = 'http://192.168.133.223:5555/API/oms/order/v1/update'
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,sq;q=0.7,ar;q=0.6,an;q=0.5',
            'Access-Token': 'eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5naGFpIiwidXNlcklkIjoiNTM2Iiwibmlja05hbWUiOiLpu4TmtbciLCJ0aW1lc3RhbXAiOjE2OTI1ODI1OTI1NTJ9.6L0QYBNei99xesfFMVvnspf8Spbm7F16EcBZvtNTzKo',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Cookie': '...',
            'Origin': 'http://192.168.133.223:5555',
            'Referer': 'http://192.168.133.223:5555/YWZT/order/manager/orderEdit?id=5842246&orderCode=SO23081701229',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'User-Id': '536',
            'system-code': 'ERP'
        }
        data = {
    "id":5842246,
    "orderType":1,
    "orderCode":"SO23081701229",
    "platformId":47,
    "warehouseId":220,
    "marketId":10,
    "channelId":115,
    "orderSnSource":"1952730840937941589",
    "sourceCode":"1952730840937941589",
    "salesRecordNum":0,
    "transport":"express",
    "expressType":"123",
    "expressTypeName":"123",
    "productVarietyNum":1,
    "productTotalNum":1,
    "orderTime":"2023-08-17 20:18:55",
    "payTime":"2023-08-17 20:18:59",
    "sendTime":"",
    "customerMessage":"...........HAHA.哈哈。。。。。",
    "orderStatus":7,
    "flagsStatus":0,
    "auditTime":"2023-08-18 09:58:45",
    "auditOpinion":"修改发货仓、",
    "auditPerson":"黄海",
    "source":1,
    "apiStatus":1,
    "pushFlag":0,
    "sendType":1,
    "isSubInventory":1,
    "isTagShip":1,
    "isWait":1,
    "waitTime":"2023-08-17 20:22:24",
    "waitStatus":0,
    "isShow":1,
    "cancelType":0,
    "problemType":0,
    "firstFinanceAuditTime":"2023-08-17 20:18:55",
    "delFlag":1,
    "createTime":"2023-08-17 20:22:24",
    "updateBy":"黄海",
    "updateTime":"2023-08-18 11:44:50",
    "customerEmail":"",
    "isAuditUnlock":0,
    "isEccangAudit":0,
    "orderCodes":"",
    "logisticsStatus":0,
    "signingTime":"",
    "warehouseName":"品晟德国吉森（DE06）仓-B2B",
    "shippingWeight":0,
    "step":100,
    "ioss":"",
    "orderAttribute":1,
    "vatTaxNumber":"",
    "encryptStatus":0,
    "showWeight":31.501,
    "orderAddress":{
        "customerEmail":customerEmail,
            "receiverName":receiverName,
            "receiverCompany":receiverCompany,
            "receiverContinent":"北美洲",
            "receiverCountryCode":receiverCountryCode,
            "receiverProvince":receiverProvince,
            "receiverCity":receiverCity,
            "receiverPostcode":receiverPostcode,
            "receiverTel":receiverTel,
            "receiverAddress":receiverAddress,
            "receiverAddress2":receiverAddress2,
            "receiverRegion":receiverRegion,
            "houseNumber":houseNumber,
            "baseId":5842246,
            "id":7735627
            },
            "orderCost":{
                "id":7745184,
                "baseId":5842246,
                "totalFee":374.06,
                "cnyTotalFee":374.06,
                "platformFee":7.4812,
                "shippingFee":0,
                "actualShippingCost":0,
                "couponFee":24.94,
                "auditFee":0,
                "isPaid":1,
                "discountTotal":0,
                "exchangeRate":1,
                "currency":"RMB",
                "paymentMethods":"",
                "paymentAccount":"",
                "otherIncome":0,
                "platformCoupon":0,
                "marketIncome":374.06,
                "warehouseFee":0,
                "otherFee":0,
                "productTax":43.033,
                "shippingTax":0,
                "otherTax":0,
                "taxRate":0.13,
                "isInvoice":0,
                "useBalance":0,
                "delFlag":1,
                "createBy":"",
                "createTime":"2023-08-17 20:22:24",
                "updateBy":"",
                "updateTime":"2023-08-18 11:44:50",
                "total":374.06
            },
            "products":[
                {
                    "id":12541522,
                    "baseId":5842246,
                    "externalSku":"4939273880401",
                    "productName":"【礼遇价】SmallRig斯莫格适用于索尼A7R5/A7M4/A7S3 可折叠L型快装板sony相机配件3984",
                    "unitProductPrice":399,
                    "orderQuantity":1,
                    "productQuantity":1,
                    "realProductQuantity":0,
                    "shippingPrice":0,
                    "totalFee":399,
                    "productRemark":"",
                    "productGrade":0,
                    "productType":0,
                    "sourceCode":"1952730840937941589",
                    "transactionId":"",
                    "location":"",
                    "platformItemId":"",
                    "orderId":"",
                    "orderTime":"2023-08-17 20:18:55",
                    "delFlag":1,
                    "createBy":"",
                    "createTime":"2023-08-18 11:44:50",
                    "updateBy":"",
                    "updateTime":"2023-08-18 11:44:50",
                    "sysItems":[
                        {
                            "id":69060923,
                            "baseId":5842246,
                            "itemId":12541522,
                            "productId":2066,
                            "productCode":"1128",
                            "externalSku":"4939273880401",
                            "productName":"三脚架固定板",
                            "productQuantity":1,
                            "realProductQuantity":1,
                            "scale":1,
                            "productStatusId":5,
                            "productStatusName":"下架",
                            "weight":31501,
                            "unitProductPrice":399,
                            "totalFee":399,
                            "feeRatio":1,
                            "totalWeight":31501,
                            "originalTotalFee":399,
                            "originalUnitPrice":399,
                            "delFlag":1,
                            "createBy":"",
                            "createTime":"2023-08-18 11:44:50",
                            "updateBy":"",
                            "updateTime":"2023-08-18 11:44:50",
                            "sourceCode":"",
                            "orderTime":"",
                            "productNum":"",
                            "diffWaitNum":"",
                            "imageUrl":""
                        }
                    ],
                    "incomeList":"",
                    "orderSendTime":"",
                    "orderChannelId":"",
                    "platformStatus":"",
                    "latestShipTime":"",
                    "newSelectNum":1,
                    "price":399,
                    "disabled":"true",
                    "allPrice":"399.000",
                    "diff":"true"
                }
            ],
            "productsOld":[
                {
                    "id":12541522,
                    "baseId":5842246,
                    "externalSku":"4939273880401",
                    "productName":"【礼遇价】SmallRig斯莫格适用于索尼A7R5/A7M4/A7S3 可折叠L型快装板sony相机配件3984",
                    "unitProductPrice":399,
                    "orderQuantity":1,
                    "productQuantity":1,
                    "realProductQuantity":0,
                    "shippingPrice":0,
                    "totalFee":399,
                    "productRemark":"",
                    "productGrade":0,
                    "productType":0,
                    "sourceCode":"1952730840937941589",
                    "transactionId":"",
                    "location":"",
                    "platformItemId":"",
                    "orderId":"",
                    "orderTime":"2023-08-17 20:18:55",
                    "delFlag":1,
                    "createBy":"",
                    "createTime":"2023-08-18 11:44:50",
                    "updateBy":"",
                    "updateTime":"2023-08-18 11:44:50",
                    "sysItems":[
                        {
                            "id":69060923,
                            "baseId":5842246,
                            "itemId":12541522,
                            "productId":2066,
                            "productCode":"1128",
                            "externalSku":"4939273880401",
                            "productName":"三脚架固定板",
                            "productQuantity":1,
                            "realProductQuantity":1,
                            "scale":1,
                            "productStatusId":5,
                            "productStatusName":"下架",
                            "weight":31501,
                            "unitProductPrice":399,
                            "totalFee":399,
                            "feeRatio":1,
                            "totalWeight":31501,
                            "originalTotalFee":399,
                            "originalUnitPrice":399,
                            "delFlag":1,
                            "createBy":"",
                            "createTime":"2023-08-18 11:44:50",
                            "updateBy":"",
                            "updateTime":"2023-08-18 11:44:50",
                            "sourceCode":"",
                            "orderTime":"",
                            "productNum":"",
                            "diffWaitNum":"",
                            "imageUrl":""
                        }
                    ],
                    "incomeList":"",
                    "orderSendTime":"",
                    "orderChannelId":"",
                    "platformStatus":"",
                    "latestShipTime":"",
                    "newSelectNum":1,
                    "price":399,
                    "disabled":"true",
                    "diff":"true"
                }
            ],
            "showReceiverRegion":"false",
            "platformName":"天猫",
            "orderItem":[
                {
                    "id":12541522,
                    "baseId":5842246,
                    "externalSku":"4939273880401",
                    "productName":"【礼遇价】SmallRig斯莫格适用于索尼A7R5/A7M4/A7S3 可折叠L型快装板sony相机配件3984",
                    "unitProductPrice":399,
                    "orderQuantity":1,
                    "productQuantity":1,
                    "realProductQuantity":0,
                    "shippingPrice":0,
                    "totalFee":399,
                    "productRemark":"",
                    "productGrade":0,
                    "productType":0,
                    "sourceCode":"1952730840937941589",
                    "transactionId":"",
                    "location":"",
                    "platformItemId":"",
                    "orderId":"",
                    "orderTime":"2023-08-17 20:18:55",
                    "delFlag":1,
                    "createBy":"",
                    "createTime":"2023-08-18 11:44:50",
                    "updateBy":"",
                    "updateTime":"2023-08-18 11:44:50",
                    "sysItems":[
                        {
                            "id":69060923,
                            "baseId":5842246,
                            "itemId":12541522,
                            "productId":2066,
                            "productCode":"1128",
                            "externalSku":"4939273880401",
                            "productName":"三脚架固定板",
                            "productQuantity":1,
                            "realProductQuantity":1,
                            "scale":1,
                            "productStatusId":5,
                            "productStatusName":"下架",
                            "weight":31501,
                            "unitProductPrice":399,
                            "totalFee":399,
                            "feeRatio":1,
                            "totalWeight":31501,
                            "originalTotalFee":399,
                            "originalUnitPrice":399,
                            "delFlag":1,
                            "createBy":"",
                            "createTime":"2023-08-18 11:44:50",
                            "updateBy":"",
                            "updateTime":"2023-08-18 11:44:50",
                            "sourceCode":"",
                            "orderTime":"",
                            "productNum":"",
                            "diffWaitNum":"",
                            "imageUrl":""
                        }
                    ],
                    "incomeList":"",
                    "orderSendTime":"",
                    "orderChannelId":"",
                    "platformStatus":"",
                    "latestShipTime":"",
                    "newSelectNum":1,
                    "price":399,
                    "disabled":"true",
                    "allPrice":"399.000",
                    "diff":"true"
                }
            ],
            "timestamp":1692330334000
        }

        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
        # print(response.text)
        return response


    def audit_order(self):
        #
        url = 'http://192.168.133.223:5555/API/oms/order/v1/audit'
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,sq;q=0.7,ar;q=0.6,an;q=0.5',
            'Access-Token': 'eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5naGFpIiwidXNlcklkIjoiNTM2Iiwibmlja05hbWUiOiLpu4TmtbciLCJ0aW1lc3RhbXAiOjE2OTI1ODI1OTI1NTJ9.6L0QYBNei99xesfFMVvnspf8Spbm7F16EcBZvtNTzKo',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Cookie': '_SIGN_ON_token=...; NG_TRANSLATE_LANG_KEY=%22en%22',
            'Origin': 'http://192.168.133.223:5555',
            'Referer': 'http://192.168.133.223:5555/YWZT/inventory/purchase/orderNew',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'User-Id': '536',
            'system-code': 'ERP',
        }
        data = {"warehouseId":154,"logistics":"123","hasMagento":"false","showReceiverRegion":"false","expressType":"123","expressTypeName":"123","ids":[5842246],"timestamp":1692329572000}

        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
        res = response.json()
        try :
            if res.get("data").get("errorList") :
                print(res.get("data").get("errorList"))
        except:
            print("pass")
            print("-----------------------------------------------------")

    def audit_order2(self):
        #
        url = 'http://192.168.133.223:5555/API/oms/order/v1/audit'
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,sq;q=0.7,ar;q=0.6,an;q=0.5',
            'Access-Token': 'eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5naGFpIiwidXNlcklkIjoiNTM2Iiwibmlja05hbWUiOiLpu4TmtbciLCJ0aW1lc3RhbXAiOjE2OTI1ODI1OTI1NTJ9.6L0QYBNei99xesfFMVvnspf8Spbm7F16EcBZvtNTzKo',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Cookie': '_SIGN_ON_token=...; NG_TRANSLATE_LANG_KEY=%22en%22',
            'Origin': 'http://192.168.133.223:5555',
            'Referer': 'http://192.168.133.223:5555/YWZT/inventory/purchase/orderNew',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'User-Id': '536',
            'system-code': 'ERP',
        }
        data = {"warehouseId":154,"logistics":"GLSS","hasMagento":"false","showReceiverRegion":"false","expressType":"GLSS","expressTypeName":"GLSS","ids":[5842246],"timestamp":1692600613000}

        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
        res = response.json()
        # print(res)
        try :
            if res.get("data").get("errorList")  != []:
                print(res.get("data").get("errorList"))
        except:
            print(res)
            print("-----------------------------------------------------")



    def test_001(self):
        self.edit_order_la01()
        self.audit_order()

    def test_002(self):
        print("校验收件人必填")
        receiverName = ""
        print("receiverName入参： ",receiverName)
        self.edit_order_la01(receiverName=receiverName)
        self.audit_order2()

    def test_003(self):
        print("校验收件人限50个字符")
        receiverName = "1234567 89012345 67890123456789012"
        print("receiverName入参： ",receiverName)
        self.edit_order_la01(receiverName=receiverName)
        self.audit_order2()

    def test_004(self):
        print("校验收件人特殊符号")
        receiverName = "123456789018901..."
        print("receiverName入参： ",receiverName)
        self.edit_order_la01(receiverName=receiverName)
        self.audit_order2()

    def test_005(self):
        print("手机号码/电话 ： ")
        receiverTel = "12345678901"
        print("receiverTel： ",receiverTel)
        self.edit_order_la01(receiverTel=receiverTel)
        self.audit_order2()

    def test_006(self):
        print("手机号码/电话 ： ")
        receiverTel = "fdsa"
        print("receiverTel： ",receiverTel)
        self.edit_order_la01(receiverTel=receiverTel)
        self.audit_order2()

    def test_007(self):
        print("手机号码/电话 ： ")
        receiverTel = "1234asf"
        print("receiverTel： ",receiverTel)
        self.edit_order_la01(receiverTel=receiverTel)
        self.audit_order2()

    def test_008(self):
        print("手机号码/电话 ： ")
        receiverTel = "12345678901234"
        print("receiverTel： ",receiverTel)
        self.edit_order_la01(receiverTel=receiverTel)
        self.audit_order2()

    def test_009(self):
        print("收件人国家/地区 ： ")
        receiverCountryCode = "ZRA"
        print("receiverCountryCode： ",receiverCountryCode)
        self.edit_order_la01(receiverCountryCode=receiverCountryCode)
        self.audit_order2()

    def test_010(self):
        print("收件人省/州： ")
        receiverProvince = "aaaaaaaaaaaaaaaaaaaaa"
        print("receiverProvince： ",receiverProvince)
        self.edit_order_la01(receiverProvince=receiverProvince)
        self.audit_order2()

    def test_011(self):
        print("城市： ")
        receiverCity = "1234567890123456789013456781"
        print("receiverCity： ",receiverCity)
        self.edit_order_la01(receiverCity=receiverCity)
        self.audit_order2()

    def test_0121(self):
        print("地址1： ")
        receiverAddress = "1234567890"
        print("receiverAddress： ",receiverAddress)
        self.edit_order_la01(receiverAddress=receiverAddress,receiverAddress2="1112")
        self.audit_order2()
    def test_01311(self):
        print("门牌号： ")
        houseNumber = ""
        print("houseNumber： ",houseNumber)
        self.edit_order_la01(houseNumber=houseNumber)
        self.audit_order2()

    def test_012(self):
        print("地址1： ")
        receiverAddress = "1234567890123456789012345678901234567890123456780"
        print("receiverAddress： ",receiverAddress)
        self.edit_order_la01(receiverAddress=receiverAddress,receiverAddress2="12")
        self.audit_order2()
    def test_013(self):
        print("邮编： ")
        receiverPostcode = "11aaaaaaaa"
        print("receiverPostcode： ",receiverPostcode)
        self.edit_order_la01(receiverPostcode=receiverPostcode)
        self.audit_order2()


    def test_014(self):
        print("公司名： ")
        receiverCompany = "012345678901234567890123456789012345678901234567893"
        print("receiverCompany： ", receiverCompany)
        self.edit_order_la01(receiverCompany=receiverCompany)
        self.audit_order2()

    def test_015(self):
        print("邮箱： ")
        customerEmail = "012345678901234567890123456789012345678901234567893"
        print("customerEmail： ", customerEmail)
        self.edit_order_la01(customerEmail=customerEmail)
        self.audit_order2()

if __name__=="__main__":
    unittest.TestCase()