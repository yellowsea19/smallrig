import unittest
from ddt import ddt,data
from common.base.handle_yaml import HandleYaml
from common.base.handle_mysql import HandleMysql
from test_suite.admin_api import Admin
from common.tool.operate_execl import ExcelUtil
import importlib,sys,os
importlib.reload(sys)

do_company_yaml = HandleYaml(r"conf/base.yaml")
do_mysql = HandleMysql()
filepath = os.path.join(os.getcwd(),"前台类目.xls")
sheetName = "Sheet1"
test_data1 = ExcelUtil(filepath, sheetName)
test_data1 = test_data1.dict_data()

filepath = os.path.join(os.getcwd(),"前台导航.xls")
sheetName = "Sheet1"
test_data2 = ExcelUtil(filepath, sheetName)
test_data2 = test_data2.dict_data()

@ddt
class Testwork(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global token,userId
        token,userId = Admin().adminLogin(username="huanghai ",password="90008ab88648b8232611b13f9f4c63ff")
        # token,userId = Admin().adminLogin(username="huanghai ",password="9ccd2600a9ce6a18e157291016099627")

    def setUp(self):
        print('start {}'.format(self))
        # print(test_data)

    # def tearDown(self):
    #     """测试完毕清理环境数据
    #     """
    #     pass

    @data(*test_data1)
    def test_webClassS(self,data):      #value用来接收data的数据
        print(data)
        siteCode="en_US"
        # siteCode="ja_JP"
        if data['First'] != "":
            #查询一级类目是否存在
            res = Admin().getWebClass_name(data["First"],siteCode=siteCode)
            #存在则跳过，不存在则插入一级类目
            if res :
                print("一级类目存在: %s"%data['First'])
            else:
                Admin().webClassSave(token=token,userId=userId,clasName=data['First'],level=1,parentId="0",siteCode=siteCode)
                res = Admin().getWebClassId(data["First"],siteCode=siteCode)
                Admin().webClassEnable(token = token,userId = userId,id= res )
        else:
            print("一级类目为空")
        if data["Second"] != "":
            #查询二级类目是否存在
            res = Admin().getWebClass_name(data["Second"],siteCode=siteCode)
            #存在则跳过，不存在则插入二级类目，并启用
            if res :
                print("二级类目存在: %s"%data["Second"])
            else:
                parentId = Admin().getWebClassId(data["First"],siteCode=siteCode)
                Admin().webClassSave(token=token,userId=userId,clasName=data['Second'],level=2,parentId=parentId,siteCode=siteCode)
                res = Admin().getWebClassId(data["Second"],siteCode=siteCode)
                Admin().webClassEnable(token = token,userId = userId,id= res )
        else:
            print("二级类目为空")
        if data['Three'] != '':
            #查询三级类目是否存在
            res = Admin().getWebClass_name(data["Three"],siteCode=siteCode)
            #存在则跳过，不存在则插入三级类目，并启用
            if res :
                print("三级类目存在: %s"%data['Three'])

            else:
                parentId = Admin().getWebClassId(data["Second"],siteCode=siteCode)
                Admin().webClassSave(token=token,userId=userId,clasName=data['Three'],level=3,parentId=parentId,siteCode=siteCode)
                res = Admin().getWebClassId(data["Three"],siteCode=siteCode)
                Admin().webClassEnable(token = token,userId = userId,id= res )
        else:
            print("三级类目为空")
        # if '&' in data['Four']:
        #             Four=data['Four'].split('&')
        #             for i in Four:
        #                 print(i)
        #                 res = Admin().getWebClass_name(i,siteCode=siteCode)
        #                 if res :
        #                         print("四级类目存在： %s"%i)
        #                 else:
        #                         parentId = Admin().getWebClassId(data["Three"],siteCode=siteCode)
        #
        #                         Admin().webClassSave(token=token,userId=userId,clasName=i,level=4,parentId=parentId,siteCode=siteCode)
        #                         res = Admin().getWebClassId(i,siteCode=siteCode)
        #                         Admin().webClassEnable(token = token,userId = userId,id= res )
        # elif data['Four'] == "" :
        #     print("四级类目为空")
        #
        #
        # else:
        #     #查询四级类目是否存在
        #     res = Admin().getWebClass_name(data["Four"],siteCode=siteCode)
        #     #存在则跳过，不存在则插入四级类目，并启用
        #     if  res:
        #         parentId = Admin().getWebClassId(data["Three"],siteCode=siteCode)
        #         Admin().webClassSave(token=token,userId=userId,clasName=data['Four'],level=4,parentId=parentId,siteCode=siteCode)
        #         res = Admin().getWebClassId(data["Four"],siteCode=siteCode)
        #         Admin().webClassEnable(token = token,userId = userId,id= res )
        #     else:
        #         print("四级类目存在： %s"%data['Four'])



    @data(*test_data2)
    def test_webNavClassS(self,data):      #value用来接收data的数据
        print(data)
        siteCode="en_US"
        # siteCode="ja_JP"
        if data['First'] != "":
            #查询一级类目是否存在
            res = Admin().getwebNavClass_name(data["First"],siteCode=siteCode)
            #存在则跳过，不存在则插入一级类目
            if res :
                print("一级类目存在: %s"%data['First'])
            else:
                Admin().webNavClassSave(token=token,userId=userId,clasName=data['First'],level=1,parentId="0",siteCode=siteCode)
                res = Admin().getwebNavClassClassId(data["First"],siteCode=siteCode)
                Admin().webNavClassEnable(token = token,userId = userId,id= res )
        else:
            print("一级类目为空")
        if data["Second"] != "":
            #查询二级类目是否存在
            res = Admin().getwebNavClass_name(data["Second"],siteCode=siteCode)
            #存在则跳过，不存在则插入二级类目，并启用
            if res :
                print("二级类目存在: %s"%data["Second"])
            else:
                parentId = Admin().getwebNavClassClassId(data["First"],siteCode=siteCode)
                Admin().webNavClassSave(token=token,userId=userId,clasName=data['Second'],level=2,parentId=parentId,siteCode=siteCode)
                res = Admin().getwebNavClassClassId(data["Second"],siteCode=siteCode)
                Admin().webNavClassEnable(token = token,userId = userId,id= res )
        else:
            print("二级类目为空")
        if data['Three'] != '':
            #查询三级类目是否存在
            res = Admin().getwebNavClass_name(data["Three"],siteCode=siteCode)
            #存在则跳过，不存在则插入三级类目，并启用
            if res :
                print("三级类目存在: %s"%data['Three'])
            else:
                parentId = Admin().getwebNavClassClassId(data["Second"],siteCode=siteCode)
                Admin().webNavClassSave(token=token,userId=userId,clasName=data['Three'],level=3,parentId=parentId,siteCode=siteCode)
                res = Admin().getwebNavClassClassId(data["Three"],siteCode=siteCode)
                Admin().webNavClassEnable(token = token,userId = userId,id= res )
        else:
            print("三级类目为空")
        # if '&' in data['Four']:
        #             Four=data['Four'].split('&')
        #             for i in Four:
        #                 print(i)
        #                 res = Admin().getwebNavClass_name(i,siteCode=siteCode)
        #                 parentId = Admin().getwebNavClassClassId(data["Three"],siteCode=siteCode)
        #                 Admin().webNavClassSave(token=token,userId=userId,clasName=i,level=4,parentId=parentId,siteCode=siteCode)
        #                 res = Admin().getwebNavClassClassId(i,siteCode=siteCode)
        #                 Admin().webNavClassEnable(token = token,userId = userId,id= res )
        #                 # if res :
        #                 #         print("四级类目存在： %s"%i)
        #                 # else:
        #                 #         parentId = Admin().getwebNavClassClassId(data["Three"],siteCode=siteCode)
        #                 #         Admin().webNavClassSave(token=token,userId=userId,clasName=i,level=4,parentId=parentId,siteCode=siteCode)
        #                 #         res = Admin().getwebNavClassClassId(i,siteCode=siteCode)
        #                 #         Admin().webNavClassEnable(token = token,userId = userId,id= res )
        # elif data['Four'] == "" :
        #     print("四级类目为空")
        #
        #
        # else:
        #     #查询四级类目是否存在
        #     res = Admin().getwebNavClass_name(data["Four"],siteCode=siteCode)
        #     #存在则跳过，不存在则插入四级类目，并启用
        #     # if res:
        #     #     parentId = Admin().getwebNavClassClassId(data["Three"],siteCode=siteCode)
        #     #     Admin().webNavClassSave(token=token,userId=userId,clasName=data['Four'],level="4",parentId=parentId,siteCode=siteCode)
        #     #     res = Admin().getwebNavClassClassId(data["Four"],siteCode=siteCode)
        #     #     Admin().webNavClassEnable(token = token,userId = userId,id= res )
        #     # else:
        #     #     print("四级类目存在： %s"%data['Four'])
        #     parentId = Admin().getwebNavClassClassId(data["Three"],siteCode=siteCode)
        #     Admin().webNavClassSave(token=token,userId=userId,clasName=data['Four'],level=4,parentId=parentId,siteCode=siteCode)
        #     res = Admin().getwebNavClassClassId(data["Four"],siteCode=siteCode)
        #     Admin().webNavClassEnable(token = token,userId = userId,id= res )
        #

if __name__ == '__main__':
    unittest.main()