import json
import time

import requests

def pull_order(env,id,platformId):
    if env == 'test' or env == 'TEST':
        url = "http://192.168.133.223:15010/api/oms/pullOrderFromMongo"
    if env =='uat' or env == 'UAT':
        url = "http://10.245.1.16:15010/api/oms/pullOrderFromMongo"
    data = {
            "id":"%s"%id,
            "platformId":platformId
            }
    headers = {
        "content-type":"application/json"
    }

    res = requests.post(url=url,data=json.dumps(data),headers=headers)
    print(res.text)

def order_compensation(platformId,channel_key,startTime,endTime,orderSnSources,env='test'):
    if env == 'test':
        url = "http://192.168.133.223:19010/smallrig-job-admin/jobinfo/trigger"
    elif env == 'uat':
        url = "http://10.245.1.16:15010/smallrig-job-admin/jobinfo/trigger"

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9,ja;q=0.8,sq;q=0.7,ar;q=0.6,an;q=0.5",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": '_SIGN_ON_token=^%^22eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5naGFpIiwidXNlcklkIjoiNTM2Iiwibmlja05hbWUiOiLpu4TmtbciLCJ0aW1lc3RhbXAiOjE3MDgyMjExNjkzNTZ9.21Qj4aLWfpD_guMphu-h_KAqhW8rhyQ3RNcOJY8Uwxc^%^22; _SIGN_ON_userId=^%^22536^%^22; _SIGN_ON_userName=^%^22^%^E9^%^BB^%^84^%^E6^%^B5^%^B7^%^22; XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d',
        "Origin": "http://192.168.133.223:19010",
        "Referer": "http://192.168.133.223:19010/smallrig-job-admin/jobinfo?jobGroup=1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    data = {
    'id': '551',
    'executorParam': f'{{"platformId":{platformId},"startTime":"{startTime}","endTime":"{endTime}","channel_key":"{channel_key}","orderSnSources":["{orderSnSources}"]}}',
    'addressList': ''
    }
    print(data)

    response = requests.post(url, headers=headers, data=data)

    return response.json()


def pull_order_mq(env,id,platformId):
    if env == 'test' or env == 'TEST':
        url = "http://192.168.133.223:8881/init/v1/sendOrderMq"
    if env =='uat' or env == 'UAT':
        url = "http://192.168.133.232:8881/init/v1/sendOrderMq"
    data = [{
            "id":"%s"%id,
            "platformId":platformId
            }]
    headers = {
        "content-type":"application/json"
    }

    res = requests.post(url=url,data=json.dumps(data),headers=headers)
    print(res.text)

def pull_rma_order(env,id,platformId):
    if env == 'test' or env == 'TEST':
        url = "http://192.168.133.223:15010/api/oms/pullRmaOrderFromMongo"
    if env =='uat' or env == 'UAT':
        url = "http://10.245.1.16:15010/api/oms/pullRmaOrderFromMongo"
    data = {
            "id":"%s"%id,
            "platformId":platformId
            }
    headers = {
        "content-type":"application/json"
    }

    res = requests.post(url=url,data=json.dumps(data),headers=headers)
    print(res.text)


def clod_data():
    url = "http://192.168.133.232:15010/order/job/orderDataMigration"

    data = {
    "startTime":"2024-06-12 00:00:00",
    "endTime":"2024-04-29 23:59:00"
    }
    headers = {
        "content-type": "application/json"
    }

    res = requests.post(url=url, data=json.dumps(data), headers=headers)
    print(res.text)
    return res.text

def pull_order1():

    url = "http://192.168.133.232:8881/init/v1/sendPullOrderMq"

    data = {
        "platformId": 43,

    }
    headers = {
        "content-type":"application/json"
    }

    res = requests.post(url=url,data=json.dumps(data),headers=headers)
    print(res.text)

def order_sign(env,order_base_id):
    if env == 'test':
        url = "http://192.168.133.223:9999/topic/sendTopicMessage.do"
    elif env == 'uat':
        url = "http://192.168.133.233:8082/topic/sendTopicMessage.do"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,ja;q=0.8,sq;q=0.7,ar;q=0.6,an;q=0.5",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Cookie": "XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d; NG_TRANSLATE_LANG_KEY=^%^22en^%^22; _SIGN_ON_token=^%^22eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5naGFpIiwidXNlcklkIjoiNTM2Iiwibmlja05hbWUiOiLpu4TmtbciLCJ0aW1lc3RhbXAiOjE3MjE2MTI5OTI0NzF9.uIW7sxa8zh3Fshch68kWREvkIOocufPvPjqmNSFNMdY^%^22; _SIGN_ON_userId=^%^22536^%^22; _SIGN_ON_userName=^%^22^%^E9^%^BB^%^84^%^E6^%^B5^%^B7^%^22^",
        "Origin": "http://192.168.133.223:9999",
        "Referer": "http://192.168.133.223:9999/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    data = {
        "topic": "topic_oms_sign",
        "key": "",
        "tag": "",
        "messageBody": f"{order_base_id}"
    }

    response = requests.post(url, json=data, headers=headers, verify=False)

    print(response.text)

def pull_order_fee(env,id,platformId,insertTimeBegin=None,insertTimeEnd=None):
    if env == 'test' or env == 'TEST':
        url = "http://192.168.133.223:41010/orderFee/pullOrderFromMongo"
    if env =='uat' or env == 'UAT':
        url = "http://192.168.133.233:41010/orderFee/pullOrderFromMongo"
    data = {
            "id":"%s"%id,
            "platformId":platformId
            }
    if insertTimeBegin != None:
        data['insertTimeBegin'] = insertTimeBegin
    if insertTimeEnd !=None:
        data['insertTimeEnd'] = insertTimeEnd
    headers = {
        "content-type":"application/json"
    }

    res = requests.post(url=url,data=json.dumps(data),headers=headers)
    print(res.text)

def pull_order_return_fee(env,id,platformId,insertTimeBegin=None,insertTimeEnd=None):
    if env == 'test' or env == 'TEST':
        url = "http://192.168.133.223:41010/returnOrderFee/pullOrderFromMongo"
    if env =='uat' or env == 'UAT':
        url = "http://192.168.133.233:41010/returnOrderFee/pullOrderFromMongo"
    data = {
            "id":"%s"%id,
            "platformId":platformId
            }
    if insertTimeBegin != None:
        data['insertTimeBegin'] = insertTimeBegin
    if insertTimeEnd !=None:
        data['insertTimeEnd'] = insertTimeEnd
    headers = {
        "content-type":"application/json"
    }

    res = requests.post(url=url,data=json.dumps(data),headers=headers)
    print(res.text)




if __name__ == "__main__":
    #标发
    # order_sign(env='uat',order_base_id=1807305290430144513)
    # clod_data()
    # pull_order_mq(env='test',id='6653fd68681a580cb8fa7aa5',platformId=47)
    # order_compensation(platformId=30,channel_key = "channel_29",startTime='2024-12-14 15:20:05',endTime='2024-12-14 15:40:05',orderSnSources="112-1246426-6900203",env='test')
    #订单清洗
    # pull_order(env='test',id='677fb81f8f189276e1bb68f9',platformId=48)
    #RMA单清洗
    pull_rma_order(env='test', id='677fb9161cf4ed47a8405290', platformId=48)
    #清洗订单费用
    # pull_order_fee(env='test', id='66f0af82146639634a56d374', platformId=31)
    # pull_order_fee(env='test', id='66f0af82146639634a56d374', platformId=31,insertTimeBegin='2024-09-23 08:00:02',insertTimeEnd='2024-09-23 08:00:02')
    # 清洗RMA单费用
    # pull_order_return_fee(env='test', id='66dec72187960054f6e4295e', platformId=59)
    # pull_order_return_fee(env='test', id='66dec72187960054f6e4295e', platformId=59,insertTimeBegin='',insertTimeEnd='')


