#!/usr/bin/python
import requests
import json,time,random
import requests
import datetime

'''测试打包复核-2c如果跑失败，可能是已发货列表不止1条数据'''

import datetime
tomtime = datetime.datetime.now()+datetime.timedelta(days=1)
tomtimes = tomtime.strftime("%Y-%m-%d %H:%M:%S")
print(tomtimes)
# 获取当前时间
times=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# 转为时间数组
timeArray = time.strptime(times, "%Y-%m-%d %H:%M:%S")
# 转为时间戳
timeStamp = int(time.mktime(timeArray))
num = random.randint(100000,10000000)

class RelyData(object):
    purchaseSn = None
    purchaseSn_id = None
    receivingGoogsSn = None

#基础数据变量
status_type = 1
selectNum = 20000
newSelectNum= selectNum
productNum= selectNum
inNum= selectNum


user_chanal="2B"

if user_chanal=="2B":
    # 渠道2B
    channelName = "Magento-ALL-欧洲"
    marketId = 8
    channelId = 107
    marketName = 'B2B-Pro'

    # channelName = "Aliexpress-CN-CF速卖通（new）"
    # marketId = 250
    # channelId = 261
    # marketName = 'Aliexpress-Pro'

else:
    # 渠道2C
    channelName = "抖音-CN-SmallRig斯莫格的小店"
    marketId = 10
    channelId = 130
    marketName = 'China-Pro'

env = "uat"
warehouse = "ZYSZ"

if env == "test":
    goodsAllocationId = 1740918142430793730
    goodsAllocationCode = "SH004"
    warehouseId = 232
    urls = 'http://192.168.133.223:5555'
    warehouseName = "自研深圳仓-测试"

elif env == "uat":
    if warehouse != "ZYSZ":
        warehouseId = 57
        goodsAllocationId = 1691000318816583681
        goodsAllocationCode = "K02-20"
        urls = 'http://bereal.smallrig.net'
        warehouseName = "中国深圳直发仓"
    else:
        goodsAllocationId = 1764931009610493954
        goodsAllocationCode = "SH0001"
        warehouseId = 232
        urls = 'http://bereal.smallrig.net'
        warehouseName = "自研深圳仓-测试"

else:
    goodsAllocationId = 1740918142430793730
    goodsAllocationCode = "SH004"
    warehouseId = 232
    urls = 'http://192.168.133.234:5555'
    warehouseName = "自研深圳仓-测试"

class Wms:
    def __init__(self):
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

        self.id = getattr(RelyData, 'purchaseSn_id')

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


    def requets_abe(self, url, payload, methon='POST', querystring=None):
        if methon == 'POST':
            payload = json.dumps(payload)
            response = requests.request(methon, url, data=payload, headers=self.headers)
            print(url + "  \n  %s" % response.text)
        else:
            response = requests.request("GET", url, data=payload, headers=self.headers, params=querystring)
            print(url + "  \n  %s" % response.text)

        if "/API/srm/otherIn/v1/queryOtherInPage" in url:
            responsejson = response.json()
            JYorderid = responsejson['data']['items'][0]['id']
            otherInNo = responsejson['data']['items'][0]['otherInNo']
            setattr(RelyData, "otherInNo", otherInNo)
            setattr(RelyData, "JYorderid", JYorderid)

        if "/API/wms/documentsReceiving/v1/queryReceivingPage" in url:
            while True:
                responsejson = response.json()
                print("responsejson  %s" % responsejson)
                records = responsejson['data']['records']
                if records == []:
                    print('数据同步借用订单列表,请稍等。。。')
                    time.sleep(1)
                    response = requests.request(methon, url, data=payload, headers=self.headers)
                else:
                    break
            QRSHorderid = responsejson['data']['records'][0]['id']
            storageNo = responsejson['data']['records'][0]['storageNo']
            QRSHdocumentsNo = responsejson['data']['records'][0]['documentsNo']
            setattr(RelyData, "QRSHorderid", QRSHorderid)
            setattr(RelyData, "storageNo", storageNo)
            setattr(RelyData, "QRSHdocumentsNo", QRSHdocumentsNo)

        if "/API/wms/documentsReceiving/v1/queryReceivingDetailPage" in url:
            time.sleep(2)
            responsejson = response.json()
            WCSHorderid1112 = responsejson['data']['records'][0]['id']
            WCSHorderid = responsejson['data']['records'][1]['id']
            receivingId = responsejson['data']['records'][0]['receivingId']

            setattr(RelyData, "WCSHorderid1112", WCSHorderid1112)
            setattr(RelyData, "WCSHorderid", WCSHorderid)
            setattr(RelyData, "receivingId", receivingId)

        if url == urls+"/API/wms/DocumentsPutaway/v1/queryPutawayPage":
            responsejson = response.json()
            putawayId = responsejson['data']['records'][0]['id']
            setattr(RelyData, "putawayId", putawayId)

        if url == urls+"/API/wms/documentsPutawayDetail/v1/queryPutawayDetailPage":
            responsejson = response.json()
            putawayId01 = responsejson['data']['records'][0]['id']
            putawayId02 = responsejson['data']['records'][1]['id']

            setattr(RelyData, "putawayId01", putawayId01)
            setattr(RelyData, "putawayId02", putawayId02)

    def excutecode(self):
        if env=="test":
            url = 'http://192.168.133.223:19010/smallrig-job-admin/jobinfo/trigger'
            payload = "id=311&executorParam=&addressList="
            headers = {
                'Cookie': "_SIGN_ON_token=%22eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5nemhlbiIsInVzZXJJZCI6IjQ1NyIsIm5pY2tOYW1lIjoi6buE6ZWHIiwidGltZXN0YW1wIjoxNjY1NzExNzc2Mzk4fQ.bLi9FbhLpnIKGVLnTg-5uAJ9SpIWoAzbh7AlLLLAbwI%22; _SIGN_ON_userId=%22457%22; _SIGN_ON_userName=%22%E9%BB%84%E9%95%87%22; XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d",
                'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
                'cache-control': "no-cache",
                'Postman-Token': "195590c1-447b-4a12-bc25-5dee36dacde0"
            }
        elif env == "uat":
            url = 'http://bereal.smallrig.net/smallrig-job-admin/jobinfo/trigger'
            payload = "id=418&executorParam=&addressList="
            headers = {
                'Cookie': "XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d; _ga=GA1.1.825110043.1664445764; _ga_X64KPEGTYM=GS1.1.1695373981.11.1.1695374036.5.0.0; _SIGN_ON_token=%22eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5nemhlbiIsInVzZXJJZCI6IjQ1NyIsIm5pY2tOYW1lIjoi6buE6ZWHIiwidGltZXN0YW1wIjoxNzA0MjgzNTA2ODcwfQ.MJs89asWM7A_ATvifVdNtGaUxDNAczUtKiUYq0nm-Bg%22; _SIGN_ON_userId=%22457%22; _SIGN_ON_userName=%22%E9%BB%84%E9%95%87%22",
                'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
                'cache-control': "no-cache",
                'Postman-Token': "195590c1-447b-4a12-bc25-5dee36dacde0"
            }
        else:
            url = 'http://192.168.133.234:19010/smallrig-job-admin/jobinfo/trigger'
            payload = "id=430&executorParam=&addressList="
            headers = {
                'Cookie': "XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d; _SIGN_ON_token=%22eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5nemhlbiIsInVzZXJJZCI6IjQ1NyIsIm5pY2tOYW1lIjoi6buE6ZWHIiwidGltZXN0YW1wIjoxNzAzOTA0OTMwOTI3fQ.673vWHcat7k8V52uRu8ChOv1P-QaovLyWws_8Z8itr4%22; _SIGN_ON_userId=%22457%22; _SIGN_ON_userName=%22%E9%BB%84%E9%95%87%22",
                'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
                'cache-control': "no-cache",
                'Postman-Token': "195590c1-447b-4a12-bc25-5dee36dacde0"
            }

        response = requests.request("POST", url, data=payload, headers=headers)
        print(response)

if __name__=="__main__":
    wms = Wms()
    methon = 'GET'

    #其他入库*
    urlF = urls + "/API/srm/otherIn/v1/createOrUpdateOtherIn"
    payload = {"channelName":channelName,"marketId":marketId,"channelId":channelId,"marketName":marketName,"warehouseCode":"ZY_SZCPC","warehouseName":warehouseName,"id":None,"warehouseId":warehouseId,"remark":"备注！！！","infoList":[{"productCode":"1112","productId":2589,"productStatusName":"下架","productStatusId":5,"weight":12,"productName":"斯莫格EVF单反摄影监视器转接头快接管夹热靴配件相机连接件1112","selectNum":selectNum,"newSelectNum":newSelectNum,"productNum":productNum,"inNum":inNum},{"productCode":"1986C","productId":1888,"productStatusName":"下架","productStatusId":5,"weight":100,"productName":"SmallRig Sony A6500 Camera Accessory Kit 1986","selectNum":selectNum,"newSelectNum":newSelectNum,"productNum":productNum,"inNum":inNum}],"shipmentid":num,"timestamp":timeStamp}
    #多sku
    # payload = {"channelName":"Amazon-CA-AC","marketId":1,"channelId":13,"marketName":"Amazon-AC-Pro","warehouseCode":"ZY_SZCPC","warehouseName":warehouseName,"id":null,"warehouseId":232,"remark":"2342324234","infoList":[{"productCode":"3025","productId":6809,"productStatusName":"在售","productStatusId":4,"weight":70,"productName":"SmallRig DJI RS 2/RSC 2滑槽拓展配件 3025","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3024","productId":6800,"productStatusName":"在售","productStatusId":4,"weight":395,"productName":"SmallRig 松下LUMIX BGH1 4k电影机专用cage 3024","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3021","productId":6831,"productStatusName":"在售","productStatusId":4,"weight":60,"productName":"SmallRig 数据传输线 (D转A) 3021","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3020","productId":6830,"productStatusName":"在售","productStatusId":4,"weight":60,"productName":"SmallRig 数据传输线 (C转A) 3020","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3019","productId":6829,"productStatusName":"在售","productStatusId":4,"weight":60,"productName":"SmallRig 数据传输线 (A转A) 3019","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3018","productId":6827,"productStatusName":"在售","productStatusId":4,"weight":98.5,"productName":"SmallRig 轻量版 NP-F 供电安装座 3018","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3016","productId":6851,"productStatusName":"在售","productStatusId":4,"weight":242,"productName":"SmallRig 标准款V口电池挂板双管夹版 3016","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3015","productId":6824,"productStatusName":"清仓待下架","productStatusId":1,"weight":56,"productName":"斯莫格内存卡盒 3015","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3011","productId":7892,"productStatusName":"在售","productStatusId":4,"weight":68,"productName":"SmallRig 管夹（带滑条）3011","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3010B","productId":8933,"productStatusName":"在售","productStatusId":4,"weight":5039.15,"productName":"导入产品测试-WS0K0U1","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3010","productId":7891,"productStatusName":"在售","productStatusId":4,"weight":498,"productName":"SmallRig mini跟焦器 3010","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3009B","productId":6936,"productStatusName":"待售","productStatusId":10,"weight":524,"productName":"SmallRig索尼Alpha 7S III兔笼手持套装3009B","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3009","productId":6638,"productStatusName":"升级待下架","productStatusId":2,"weight":550,"productName":"SmallRig A7S III A7S3兔笼线夹上手提大师套装 3009","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3008B","productId":6935,"productStatusName":"待售","productStatusId":10,"weight":504,"productName":"SmallRig索尼Alpha 7S III兔笼侧手持套装3008B","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3008","productId":6637,"productStatusName":"升级待下架","productStatusId":2,"weight":530,"productName":"SmallRig A7S III A7S3兔笼线夹侧手柄专业套装 3008","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3007B","productId":6934,"productStatusName":"待售","productStatusId":10,"weight":299,"productName":"SmallRig 索尼Alpha 7S III兔笼线夹套件3007B","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3007","productId":6633,"productStatusName":"升级待下架","productStatusId":2,"weight":325,"productName":"SmallRig A7S III A7S3兔笼和HDMI线夹套件 3007","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3006","productId":6766,"productStatusName":"在售","productStatusId":4,"weight":105.8,"productName":"SmallRig 智云CRANE 2S 稳定器拓展支架3006","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3065","productId":6945,"productStatusName":"升级待下架","productStatusId":2,"weight":198,"productName":"SmallRig SONY A7S III 兔笼 3065","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3061","productId":6816,"productStatusName":"在售","productStatusId":4,"weight":130,"productName":"SmallRig DJI RS 2 / RSC 2 / Ronin-S / RS 3 / RS 3 Pro 曼富图快装板 3061","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3059","productId":6785,"productStatusName":"下架","productStatusId":5,"weight":548,"productName":"SmallRig 通用款V口电池底座双管夹调节版 3059","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3060","productId":6828,"productStatusName":"在售","productStatusId":4,"weight":80,"productName":"SmallRig DJI Osmo Mobile 3/4手机稳定器砝码（20g x 3）3060","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3058","productId":6784,"productStatusName":"下架","productStatusId":5,"weight":468,"productName":"SmallRig 通用款V口电池底座双管夹版 3058","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3057","productId":6858,"productStatusName":"在售","productStatusId":4,"weight":1700,"productName":"SmallRig SONY FX9 专业版套件 3057","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3056","productId":6857,"productStatusName":"在售","productStatusId":4,"weight":1200,"productName":"SmallRig SONY FX9 基础版套件 3056","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3053","productId":6846,"productStatusName":"待售","productStatusId":10,"weight":31,"productName":"SmallRig Ronin-s转BMPCC 4K/6K供电线","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3048","productId":6801,"productStatusName":"在售","productStatusId":4,"weight":208,"productName":"SmallRig AJA HA5-12G  BMD HDMI-SDI 6G转接器固定夹3048","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3051","productId":6989,"productStatusName":"在售","productStatusId":4,"weight":1910,"productName":"SmallRig 多功能双肩摄影包BP-L01 3051","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3047","productId":6730,"productStatusName":"在售","productStatusId":4,"weight":446,"productName":"BMPCC 4K 6K 兔笼遮光罩套件 3047","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3046B","productId":6948,"productStatusName":"待售","productStatusId":10,"weight":596,"productName":"SmallRig专用兔笼3046适配 RED KOMODO","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3046","productId":6826,"productStatusName":"在售","productStatusId":4,"weight":596,"productName":"SmallRig专用兔笼3046适配 RED KOMODO","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3045","productId":6931,"productStatusName":"在售","productStatusId":4,"weight":96,"productName":"SmallRig KOMODO专用（EVF）监视器支架3045","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3043","productId":6835,"productStatusName":"在售","productStatusId":4,"weight":45,"productName":"SmallRig 4K超细HDMI线D转A（55cm） 3043","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3042","productId":6834,"productStatusName":"升级待下架","productStatusId":2,"weight":41,"productName":"SmallRig 4K超细D转A HDMI数据传输线（35cm） 3042","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3041","productId":6833,"productStatusName":"在售","productStatusId":4,"weight":45,"productName":"SmallRig 4K超细HDMI线C转A（55cm） 3041","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3040","productId":6832,"productStatusName":"在售","productStatusId":4,"weight":41,"productName":"SmallRig 4K超细HDMI线C转A（35cm） 3040","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3035B","productId":7012,"productStatusName":"待售","productStatusId":10,"weight":290,"productName":"影视飓风定制索尼A7S3cage（影视飓风logo）","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3035","productId":6745,"productStatusName":"升级待下架","productStatusId":2,"weight":290,"productName":"影视飓风定制索尼A7S3cage（影视飓风logo）","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3034","productId":6773,"productStatusName":"在售","productStatusId":4,"weight":228,"productName":"SmallRig铝合金全景云台 3034","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3033","productId":6772,"productStatusName":"在售","productStatusId":4,"weight":257,"productName":"SmallRig铝合金桌面三脚架3033","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3032","productId":6810,"productStatusName":"在售","productStatusId":4,"weight":40,"productName":"SmallRig DJI Ronin S/SC专用拓展滑条 3032","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3031B","productId":6959,"productStatusName":"在售","productStatusId":4,"weight":170,"productName":"SmallRig DJI RS 2  Ronin-S加长曼富图快装板 3031B","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3031","productId":6817,"productStatusName":"下架","productStatusId":5,"weight":160,"productName":"SmallRig DJI RS 2加长曼富图快装板3031","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3029B","productId":6910,"productStatusName":"在售","productStatusId":4,"weight":50,"productName":"SmallRig DJI RS 2稳定器钢化膜一对 3029B","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3029","productId":6812,"productStatusName":"下架","productStatusId":5,"weight":50,"productName":"SmallRig DJI RS 2稳定器钢化膜一对 3029","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3028C","productId":10387,"productStatusName":"待售","productStatusId":10,"weight":375,"productName":"SmallRig DJI RS 2 / RSC 2 / RS 3 / RS 3 Pro / RS 3 Mini提壶手柄 3028C","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3028B","productId":6940,"productStatusName":"在售","productStatusId":4,"weight":342,"productName":"SmallRig DJI RS 2/RSC 2提壶手柄 3028B","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3028","productId":6815,"productStatusName":"下架","productStatusId":5,"weight":350,"productName":"SmallRig DJI RS 2/RSC 2提壶手柄3028","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3027","productId":6814,"productStatusName":"待售","productStatusId":10,"weight":670,"productName":"SmallRig DJI RS 2/RSC 2 双手持手柄3027","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200},{"productCode":"3026","productId":6813,"productStatusName":"在售","productStatusId":4,"weight":170,"productName":"SmallRig DJI RS 2/RSC 2拓展监视器支架3026","selectNum":200,"newSelectNum":200,"productNum":200,"inNum":200}],"shipmentid":null,"timestamp":1698828548000}

    wms.requets_abe(urlF,payload)

    # #获取列表*
    urlF = urls + "/API/srm/otherIn/v1/queryOtherInPage"
    payload = {"pageSize":14,"pageNum":1,"id":None,"warehouseId":None,"marketId":None,"channelId":None,"remark":None,"timestamp":timeStamp}
    wms.requets_abe(urlF, payload)
    #
    # #提交其他入库
    urlF = urls + "/API/srm/otherIn/v1/submitOtherIn"
    JYorderid = getattr(RelyData, 'JYorderid')
    querystring ={
        'id': JYorderid,
        'timestamp': timeStamp
    }
    payload = []
    wms.requets_abe(urlF,payload,methon,querystring)

    print('\033[33m 请在钉钉进行审批通过  \033[0m' )

    time.sleep(10)
    wms.excutecode()

    # # WMS确认收货列表-获取id*
    otherInNo = getattr(RelyData,'otherInNo')
    payload ={"pageSize":15,"pageNum":1,"timeArr":[],"type":1,"documentsNo":"","storageNo":otherInNo,"purchaseNo":"","kingdeeNo":"","storageType":"","supplierName":"","buyer":"","status":"","skuCode":"","tallyman":"","warehouseId":"","warehouseIds":[]}
    urlF = urls + "/API/wms/documentsReceiving/v1/queryReceivingPage"
    wms.requets_abe(urlF, payload)

    # # 确认收货
    urlF = urls + "/API/wms/documentsReceiving/v1/confirmArrive"
    QRSHorderid = getattr(RelyData, 'QRSHorderid')
    querystring = {
        'id': QRSHorderid
    }
    payload = []
    wms.requets_abe(urlF, payload, methon, querystring)

    # WMS完成收货列表-获取id
    storageNo = getattr(RelyData, 'storageNo')
    payload = {"pageSize":15,"pageNum":1,"cargoOwnerId":"1597896116834062337","skuCode":"","storageNo":storageNo}
    urlF = urls + "/API/wms/documentsReceiving/v1/queryReceivingDetailPage"
    wms.requets_abe(urlF, payload)

    # WMS完成收货
    WCSHorderid1112 = getattr(RelyData, 'WCSHorderid1112')
    WCSHorderid = getattr(RelyData, 'WCSHorderid')
    receivingId = getattr(RelyData, 'receivingId')
    payload = {"id":receivingId,"infoList":[{"detailId":WCSHorderid,"skuCode":"1986C","skuNum":selectNum,"tallyingNum":0,"tallyingNumNow":selectNum,"awaitReceivingNum":0},{"detailId":WCSHorderid1112,"skuCode":"1112","skuNum":selectNum,"tallyingNum":0,"tallyingNumNow":selectNum,"awaitReceivingNum":0}]}
    urlF = urls + "/API/wms/documentsReceiving/v1/acceptFinish"
    wms.requets_abe(urlF, payload)
    #
    # WMS生成入库上架单
    urlF = urls + "/API/wms/documentsReceiving/v1/createPutaway"
    receivingId = getattr(RelyData, 'receivingId')
    querystring = {
        'id': receivingId
    }
    payload = []
    wms.requets_abe(urlF, payload, methon, querystring)

    #
    #列表-id
    urlF = urls + "/API/wms/DocumentsPutaway/v1/queryPutawayPage"
    payload = {"pageSize":14,"pageNum":1,"timeArr":[],"beginTime":"","endTime":"","documentsNo":"","warehouseId":"","receivingNo":"","kingdeeNo":"","storageType":"","canPrint":"","status":"","skuCode":"","putawayBy":""}
    wms.requets_abe(urlF, payload)

    #获取详情id
    putawayId = getattr(RelyData, 'putawayId')
    urlF = urls + "/API/wms/documentsPutawayDetail/v1/queryPutawayDetailPage"
    payload = {"pageSize":14,"pageNum":1,"putawayId":putawayId,"skuCode":""}
    wms.requets_abe(urlF, payload)
    #
    # #批量上架
    putawayId01 = getattr(RelyData, 'putawayId01')
    putawayId02 = getattr(RelyData, 'putawayId02')
    urlF = urls + "/API/wms/documentsPutawayDetail/v1/batchPutawayDetail"
    payload=[{"detailId": putawayId01, "infoList": [
        {"goodsAllocationId": goodsAllocationId, "goodsAllocationCode": goodsAllocationCode, "putawayNum": productNum,
         "waitPutawayNum": 0}]}, {"detailId": putawayId02, "infoList": [
        {"goodsAllocationId": goodsAllocationId, "goodsAllocationCode": goodsAllocationCode, "putawayNum": productNum,
         "waitPutawayNum": 0}]}]
    wms.requets_abe(urlF, payload)

    #确认上架
    putawayId = getattr(RelyData, 'putawayId')
    urlF = urls + "/API/wms/documentsPutawayDetail/v1/putawayConfirm"
    querystring = {"putawayId":putawayId}
    wms.requets_abe(urlF, payload, methon, querystring)







































