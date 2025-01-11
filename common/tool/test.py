import requests
import json

def beihuo_request():

    url = 'http://192.168.133.223:5555/API/isu/stockPlanNew/v1/saveOrUpdateStockPlan'

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,ja;q=0.8,sq;q=0.7,ar;q=0.6,an;q=0.5",
        "Access-Token": "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5naGFpIiwidXNlcklkIjoiNTM2Iiwibmlja05hbWUiOiLpu4TmtbciLCJ0aW1lc3RhbXAiOjE2OTEzNzQ2NDY3MjB9.UKufFhPNVJ19kIlGLIEPDhzZd2BiIEQyg9mhfrlFrg4",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Cookie": 'XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d; NG_TRANSLATE_LANG_KEY=^%^22en^%^22; _SIGN_ON_token=^%^22eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5naGFpIiwidXNlcklkIjoiNTM2Iiwibmlja05hbWUiOiLpu4TmtbciLCJ0aW1lc3RhbXAiOjE2OTAxOTE0MzQ4NTB9.imLXCDPRJ2RGwIm_arGkzTGkLKOVNrvSuxo92twZYUM^%^22; _SIGN_ON_userId=^%^22536^%^22; _SIGN_ON_userName=^%^22^%^E9^%^BB^%^84^%^E6^%^B5^%^B7^%^22',
        "Origin": "http://192.168.133.223:5555",
        "Pragma": "no-cache",
        "Referer": "http://192.168.133.223:5555/YWZT/stockUp/stockUpManage/stockUpPlanningNew",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "User-Id": "536",
        "system-code": "ERP",
    }


    data = {"distributionLevel":"SO","marketName":"Website-Pro","marketId":9,"channelName":"LeqiMall-All","channelId":159,"planStartTime":"2023-08-31 00:00:00","planEndTime":"2023-08-31 23:59:59","planTimeType":1,"goodsList":[{"id":"","stockPlanId":"","productId":3085,"productCode":"1078","productName":"SmallRig Dual 15mm Rod Clamp with 1/4\" Threads 1078","skuGradeName":"停产","expectedDeliveryDate":"2023-08-30 00:00:00","lastReceivedTime":"","needNum":"1","receivedQuantity":"","skuFillRate":"","skuStatus":""},{"id":"","stockPlanId":"","productId":1888,"productCode":"1986C","productName":"SmallRig Sony A6500 Camera Accessory Kit 1986","skuGradeName":"停产","expectedDeliveryDate":"2023-08-30 00:00:00","lastReceivedTime":"","needNum":"1","receivedQuantity":"","skuFillRate":"","skuStatus":""},{"id":"","stockPlanId":"","productId":1872,"productCode":"2147B","productName":"SmallRig Accessory Kit for Sony A6500/A6300/A6000/ILCE-6000/ILCE-6300/ILCE-6500 NEX7 2147","skuGradeName":"停产","expectedDeliveryDate":"2023-08-30 00:00:00","lastReceivedTime":"","needNum":"1","receivedQuantity":"","skuFillRate":"","skuStatus":""},{"id":"","stockPlanId":"","productId":6913,"productCode":"3157","productName":"SmallRig Pix M160 RGBWW LED补光灯3157","skuGradeName":"","expectedDeliveryDate":"2023-08-30 00:00:00","lastReceivedTime":"","needNum":"1","receivedQuantity":"","skuFillRate":"","skuStatus":""}],"warehouseId":57,"timestamp":1691398222000}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    return response

def audit_beihuo(beihuo_id):
    url = "http://192.168.133.223:5555/API/isu/stockPlanNew/v1/auditPass?id=%s"%beihuo_id

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,ja;q=0.8,sq;q=0.7,ar;q=0.6,an;q=0.5",
        "Access-Token": "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5naGFpIiwidXNlcklkIjoiNTM2Iiwibmlja05hbWUiOiLpu4TmtbciLCJ0aW1lc3RhbXAiOjE2OTEzNzQ2NDY3MjB9.UKufFhPNVJ19kIlGLIEPDhzZd2BiIEQyg9mhfrlFrg4",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Cookie": "NG_TRANSLATE_LANG_KEY=^%^22en^%^22; XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d; _SIGN_ON_token=^%^22eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5naGFpIiwidXNlcklkIjoiNTM2Iiwibmlja05hbWUiOiLpu4TmtbciLCJ0aW1lc3RhbXAiOjE2OTEzNzQ2NDY3MjB9.UKufFhPNVJ19kIlGLIEPDhzZd2BiIEQyg9mhfrlFrg4^%^22; _SIGN_ON_userId=^%^22536^%^22; _SIGN_ON_userName=^%^22^%^E9^%^BB^%^84^%^E6^%^B5^%^B7^%^22",
        "Pragma": "no-cache",
        "Referer": "http://192.168.133.223:5555/YWZT/stockUp/stockUpManage/stockUpPlanningNew",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "User-Id": "536",
        "system-code": "ERP",
    }

    response = requests.get(url, headers=headers, verify=False)

    print(response.status_code)
    print(response.text)



def XQ_request():
    url = 'http://192.168.133.223:5555/API/isu/needPlan/v1/saveOrUpdateNeedPlan'
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,ja;q=0.8,sq;q=0.7,ar;q=0.6,an;q=0.5",
        "Access-Token": "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5naGFpIiwidXNlcklkIjoiNTM2Iiwibmlja05hbWUiOiLpu4TmtbciLCJ0aW1lc3RhbXAiOjE2OTEzNzQ2NDY3MjB9.UKufFhPNVJ19kIlGLIEPDhzZd2BiIEQyg9mhfrlFrg4",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Cookie": 'XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d; NG_TRANSLATE_LANG_KEY=^%^22en^%^22; _SIGN_ON_token=^%^22eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5naGFpIiwidXNlcklkIjoiNTM2Iiwibmlja05hbWUiOiLpu4TmtbciLCJ0aW1lc3RhbXAiOjE2OTAxOTE0MzQ4NTB9.imLXCDPRJ2RGwIm_arGkzTGkLKOVNrvSuxo92twZYUM^%^22; _SIGN_ON_userId=^%^22536^%^22; _SIGN_ON_userName=^%^22^%^E9^%^BB^%^84^%^E6^%^B5^%^B7^%^22',
        "Origin": "http://192.168.133.223:5555",
        "Pragma": "no-cache",
        "Referer": "http://192.168.133.223:5555/YWZT/inventory/purchase/needPlanNew",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "User-Id": "536",
        "system-code": "ERP",
    }

    data = {"needType":1,"expectedDeliveryDate":"2023-08-31 00:00:00","goodsList":[{"id":"","needPlanId":"","productId":3085,"productCode":"1078","productName":"SmallRig Dual 15mm Rod Clamp with 1/4\" Threads 1078","skuGradeName":"停产","expectedDeliveryDate":"2023-08-30 00:00:00","lastReceivedTime":"","needNum":10,"receivedQuantity":"","skuFillRate":"","skuRemark":"","skuStatus":"","notReceivedNum":""},{"id":"","needPlanId":"","productId":1888,"productCode":"1986C","productName":"SmallRig Sony A6500 Camera Accessory Kit 1986","skuGradeName":"停产","expectedDeliveryDate":"2023-08-30 00:00:00","lastReceivedTime":"","needNum":10,"receivedQuantity":"","skuFillRate":"","skuRemark":"","skuStatus":"","notReceivedNum":""},{"id":"","needPlanId":"","productId":1872,"productCode":"2147B","productName":"SmallRig Accessory Kit for Sony A6500/A6300/A6000/ILCE-6000/ILCE-6300/ILCE-6500 NEX7 2147","skuGradeName":"停产","expectedDeliveryDate":"2023-08-30 00:00:00","lastReceivedTime":"","needNum":10,"receivedQuantity":"","skuFillRate":"","skuRemark":"","skuStatus":"","notReceivedNum":""},{"id":"","needPlanId":"","productId":6913,"productCode":"3157","productName":"SmallRig Pix M160 RGBWW LED补光灯3157","skuGradeName":"","expectedDeliveryDate":"2023-08-30 00:00:00","lastReceivedTime":"","needNum":10,"receivedQuantity":"","skuFillRate":"","skuRemark":"","skuStatus":"","notReceivedNum":""}],"timestamp":1691389432000}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    return response

def audit_xq(xq_id):
    url = "http://192.168.133.223:5555/API/isu/needPlan/v1/auditPass?id=%s"%xq_id

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,ja;q=0.8,sq;q=0.7,ar;q=0.6,an;q=0.5",
        "Access-Token": "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5naGFpIiwidXNlcklkIjoiNTM2Iiwibmlja05hbWUiOiLpu4TmtbciLCJ0aW1lc3RhbXAiOjE2OTEzNzQ2NDY3MjB9.UKufFhPNVJ19kIlGLIEPDhzZd2BiIEQyg9mhfrlFrg4",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Cookie": "NG_TRANSLATE_LANG_KEY=^%^22en^%^22; XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726d616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d",
        "Pragma": "no-cache",
        "Referer": "http://192.168.133.223:5555/YWZT/inventory/purchase/needPlanNew",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "User-Id": "536",
        "system-code": "ERP",
    }

    response = requests.get(url, headers=headers, verify=False)

    # print(response.status_code)
    print(response.text)


# #生成需求计划
# for i in range(1):
#     response = XQ_request()
#     print(response.text)


# xq_id = ["1131886007512211457","1131887290562387969","1131888063950102529","1131963559421435905","1132372111520698369","1133039216888954881","1134491769501683713","1135973698717634561","1138115298449195009","1138115704956944385","1138115705594478593","1138115706190069761","1138115706773078017","1138115707339309057","1138115707943288833","1138115708559851521","1138115709159636993","1138115709738450945","1138115710342430721","1138115757721288705","1138115758312685569","1138115758899888129","1138115759495479297","1138115760099459073","1138115760707633153","1138115761290641409","1138115761882038273","1138115762465046529","1138115763035471873","1138115829137702913","1138115829708128257","1138115830265970689","1138115830861561857","1138115831427792897"]
#
# for i in xq_id :
#     audit_xq(i)

# for i in range(30):
#     #生成备货计划
#     res = beihuo_request()
#     print(res.json())

beihuo_id = ["1138152166368845825","1138152736139878401","1138152736798384129","1138152737381392385","1138152737964400641","1138152738534825985","1138152739151388673","1138152739713425409","1138152740439040001","1138152741068185601","1138152783623593985","1138152784177242113","1138152784726695937","1138152785288732673","1138152785850769409","1138152786475720705","1138152787050340353","1138152787650125825","1138152788279271425","1138152852108189697","1138152877890576385","1138152878481973249","1138152879035621377","1138152879585075201","1138152880142917633","1138152880704954369","1138152881275379713","1138152881837416449","1138152882407841793","1138152882986655745","1138152883544498177","1138152884106534913","1138152884660183041","1138152885230608385","1138152885784256513","1138152886346293249","1138152886929301505","1138152887596195841","1138152888170815489","1138152888716075009","1138152889324249089","1138152889869508609","1138152890519625729","1138152891069079553","1138152891618533377","1138152892193153025","1138152892750995457","1138152893875068929","1138152894424522753"]

for i in beihuo_id:
    audit_beihuo(i)