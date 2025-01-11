import requests
import unittest
import json
import urllib.parse

class TestAPIRequest(unittest.TestCase):

    #执行定时任务 【流水补齐】
    def test_job01(self):
        print("执行定时任务【流水补齐】")
        url = "http://192.168.133.223:19010/smallrig-job-admin/jobinfo/trigger"

        payload = {
            'id': 540,
            'executorParam': {
                "type": 1,
                "beginTime": "2023-09-01",
                "endTime": "2023-09-01",
                "warehouseId": [225]
            },
            'addressList': ''
        }
        payload['executorParam'] = json.dumps(payload['executorParam'])
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,sq;q=0.7,ar;q=0.6,an;q=0.5',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'NG_TRANSLATE_LANG_KEY=%22en%22; XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d; _SIGN_ON_token=%22eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5naGFpIiwidXNlcklkIjoiNTM2Iiwibmlja05hbWUiOiLpu4TmtbciLCJ0aW1lc3RhbXAiOjE2OTQzOTg3ODgxMzF9.4rgA1CmEa0WsTf8EnW8iRzC2oXhe6E6HzpNZY9hajZo%22; _SIGN_ON_userId=%22536%22; _SIGN_ON_userName=%22%E9%BB%84%E6%B5%B7%22',
            'Origin': 'http://192.168.133.223:19010',
            'Referer': 'http://192.168.133.223:19010/smallrig-job-admin/jobinfo?jobGroup=1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        self.assertEqual(response.status_code, 200)

    #执行定时任务 【流水匹配业务单据】
    def test_job02(self):
        print("执行定时任务【流水匹配业务单据】")
        url = "http://192.168.133.223:19010/smallrig-job-admin/jobinfo/trigger"

        payload = {
            'id': 540,
            'executorParam': {
                "type": 2,
                "beginTime": "2023-09-01",
                "endTime": "2023-09-19",
                "warehouseId": [154]
            },
            'addressList': ''
        }
        payload['executorParam'] = json.dumps(payload['executorParam'])

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,sq;q=0.7,ar;q=0.6,an;q=0.5',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'NG_TRANSLATE_LANG_KEY=%22en%22; XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d; _SIGN_ON_token=%22eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5naGFpIiwidXNlcklkIjoiNTM2Iiwibmlja05hbWUiOiLpu4TmtbciLCJ0aW1lc3RhbXAiOjE2OTQzOTg3ODgxMzF9.4rgA1CmEa0WsTf8EnW8iRzC2oXhe6E6HzpNZY9hajZo%22; _SIGN_ON_userId=%22536%22; _SIGN_ON_userName=%22%E9%BB%84%E6%B5%B7%22',
            'Origin': 'http://192.168.133.223:19010',
            'Referer': 'http://192.168.133.223:19010/smallrig-job-admin/jobinfo?jobGroup=1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        response = requests.request("POST", url, headers=headers, params=payload)
        print(response.text)
        # Do your assertion checking here
        self.assertEqual(response.status_code, 200)


    def test_job03(self):
        print("执行定时任务【流水生成出入库】")
        url = "http://192.168.133.223:19010/smallrig-job-admin/jobinfo/trigger"

        payload = {
            'id': 540,
            'executorParam': {
                "type": 3,
                "beginTime": "2023-09-01",
                "endTime": "2023-09-19",
                "warehouseId": [154,99]
            },
            'addressList': ''
        }
        payload['executorParam'] = json.dumps(payload['executorParam'])

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,sq;q=0.7,ar;q=0.6,an;q=0.5',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'NG_TRANSLATE_LANG_KEY=%22en%22; XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d; _SIGN_ON_token=%22eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5naGFpIiwidXNlcklkIjoiNTM2Iiwibmlja05hbWUiOiLpu4TmtbciLCJ0aW1lc3RhbXAiOjE2OTQzOTg3ODgxMzF9.4rgA1CmEa0WsTf8EnW8iRzC2oXhe6E6HzpNZY9hajZo%22; _SIGN_ON_userId=%22536%22; _SIGN_ON_userName=%22%E9%BB%84%E6%B5%B7%22',
            'Origin': 'http://192.168.133.223:19010',
            'Referer': 'http://192.168.133.223:19010/smallrig-job-admin/jobinfo?jobGroup=1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        response = requests.request("POST", url, headers=headers, params=payload)
        print(response.text)
        # Do your assertion checking here
        self.assertEqual(response.status_code, 200)

    def test_job04(self):
        print("执行定时任务【生成批次】")
        url = "http://192.168.133.223:19010/smallrig-job-admin/jobinfo/trigger"

        payload = {
            'id': 540,
            'executorParam': {
                "type": 4,
                "beginTime": "2023-09-01",
                "endTime": "2023-09-19",
                "warehouseId": [154]
            },
            'addressList': ''
        }
        payload['executorParam'] = json.dumps(payload['executorParam'])

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,sq;q=0.7,ar;q=0.6,an;q=0.5',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'NG_TRANSLATE_LANG_KEY=%22en%22; XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a223962326431636164333937653538653063663139393262373933306138373434222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d; _SIGN_ON_token=%22eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Imh1YW5naGFpIiwidXNlcklkIjoiNTM2Iiwibmlja05hbWUiOiLpu4TmtbciLCJ0aW1lc3RhbXAiOjE2OTQzOTg3ODgxMzF9.4rgA1CmEa0WsTf8EnW8iRzC2oXhe6E6HzpNZY9hajZo%22; _SIGN_ON_userId=%22536%22; _SIGN_ON_userName=%22%E9%BB%84%E6%B5%B7%22',
            'Origin': 'http://192.168.133.223:19010',
            'Referer': 'http://192.168.133.223:19010/smallrig-job-admin/jobinfo?jobGroup=1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        response = requests.request("POST", url, headers=headers, params=payload)
        print(response.text)
        # Do your assertion checking here
        self.assertEqual(response.status_code, 200)


    def test_get(self):
        url = 'http://192.168.133.223:41010/api/financial/repartition/queryRepartitionCostSku'
        data = [
    "HS23091900002"
    ]
        res =  requests.post(url=url,json=data)
        print(json.dumps(res.json(),ensure_ascii=False,indent=2))





if __name__ == '__main__':
    unittest.main()