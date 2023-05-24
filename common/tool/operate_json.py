#!-*-coding:utf-8 -*-

import json
import os

class OperationJson():

    def __init__(self,filepath=None):
        self.data=self.read_data(filepath)

    #读取json文件数据
    def read_data(self,file_path=None):
        if file_path==None:
            CONF_PATH = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            filename = os.path.join(CONF_PATH, "data\\bumperscase.yaml")
            with open(filename,encoding='UTF-8') as fp:
                data=json.load(fp)
                return data
        else:
            CONF_PATH = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            filename = os.path.join(CONF_PATH, file_path)
            with open(filename,encoding='UTF-8') as fp:
                data=json.load(fp)
                return data

    #根据关键字获取数据
    def get_data(self,id):
        return self.data[id]


if __name__ == '__main__':
    opjson=OperationJson('data\\agentdata.json')
    data = opjson.get_data('account_login')["data"]
    data["loginKey"] = '14579653214'
    print(data)
    # print(opjson.get_data('account_login')["title"])
