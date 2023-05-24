from locust import HttpUser, TaskSet, task
import requests,json
import os,time
import queue



def GetData():
    s = queue.Queue(maxsize=0)
    for i in range(1001, 1006):
        # 往队列里面压入1,2,3,4,5
        s.put_nowait(i)
    return s


class My_task_set(TaskSet):
    '''
    创建后台管理站点压测类，需要继承TaskSet
    可以添加多个任务
    '''
    def pcLogin(self,username=None,password=None):
        """PC登录接口
        """
        self.get_data =  {
            "title": "PC登录",
            "method": "post",
            "path": "/api/memberLogin/login",
            "data":{"account":username,
                    "passwd":"a123456",
                    "verifyCode":""}
            }

        self.url ="http://192.168.133.22:8002" + self.get_data["path"]
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


    def on_start(self):
        '''
        当任何一个task调度执行前，on_start实例方法会被调用
        先登录
        '''
        data = self.user.queueData.get()  # self.user调用websitUser类里面的数据
        self.user.queueData.put_nowait(data)#队列取出后，再把取出数据放入队尾中,以达到循环使用数据
        print(data)
        self.token,self.userId = self.pcLogin(username="auto%s@qq.com"%data, password="a123456")



    @task
    def getLotteryMembers(self,):
        """查询用户抽奖信息
        """
        self.get_data = {
            "title": "查询抽奖用户信息",
            "method": "post",
            "path": "/api/lottery/getLotteryMembers",
            "data":{"lotteryId": 0}
            }
        self.url = self.get_data["path"]
        self.headers = {
            "Access-Token": self.token,
            "Content-Type": "application/json;charset=UTF-8",
            "User-Id": self.userId,
            "System-Port": "0",
            "Flow-Sourcet": "0",
            "Accept-Language": "en_US",
        }
        self.data = self.get_data["data"]
        self.data['lotteryId'] = "1589902252424011777"
        with self.client.post(url=self.url, headers=self.headers, data=json.dumps(self.data),catch_response=True,name="getLotteryMembers") as res:

            if res.json()['code']  == 10000:
                res.success()
            else:
                res.failure("false")
            print(res.json())

    def on_stop(self):
        '''
        当任何一个task调度执行之后，on_stop实例方法会被调用
        :return:
        '''
        pass


class RunLoadTests(HttpUser):
    '''
    创建运行类
    '''
    tasks = [My_task_set]
    min_wait = 200  # 模拟负载的任务之间执行时的最小等待时间，单位为毫秒
    max_wait = 5000  # 模拟负载的任务之间执行时的最大等待时间，单位为毫秒
    host = "http://192.168.133.22:8002"
    queueData = GetData()


if __name__=="__main__":
    import os
    os.system("locust -f test_locust.py --host=http://192.168.133.22:8002")