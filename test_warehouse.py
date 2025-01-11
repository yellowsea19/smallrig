import time

import requests
from datetime import datetime, timedelta




def test_1212():

    url = 'http://192.168.133.223:19010/smallrig-job-admin/jobinfo/trigger'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,sq;q=0.7,ar;q=0.6,an;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'NG_TRANSLATE_LANG_KEY=%22en%22; _SIGN_ON_token=%22eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5naGFpIiwidXNlcklkIjoiNTM2Iiwibmlja05hbWUiOiLpu4TmtbciLCJ0aW1lc3RhbXAiOjE3MzM3MDgyODg3NzN9.oK-087LP-k1FXIcoLUV9q-ni4X_BEjbckr2jVXZnNsw%22; _SIGN_ON_userId=%22536%22; _SIGN_ON_userName=%22%E9%BB%84%E6%B5%B7%22; XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d',
        'Origin': 'http://192.168.133.223:19010',
        'Referer': 'http://192.168.133.223:19010/smallrig-job-admin/jobinfo?jobGroup=11',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 10)

    current_date = start_date
    while current_date <= end_date:
        data = {
            'id': '672',
            'executorParam': '{"vendorCode": "0090011", "businessCode": "0090011", "beginTime": "' + current_date.strftime('%Y-%m-%d') + ' 00:00:00", "endTime": "' + current_date.strftime('%Y-%m-%d') + ' 23:59:59"}',
            'addressList': ''
        }

        response = requests.post(url, headers=headers, data=data, verify=False)
        print(f'Request for date {current_date.strftime("%Y-%m-%d")}: {response.text}')

        current_date += timedelta(days=1)
        time.sleep(1)


test_1212()

