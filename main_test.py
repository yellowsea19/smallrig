import time
import unittest
import os
import shutil
from BeautifulReport import BeautifulReport
import importlib,sys
importlib.reload(sys)



import xmlrunner

from common.base.handle_yaml import HandleYaml

do_yaml = HandleYaml("conf/base.yaml")
now = time.strftime("%Y-%m-%d %H：%M：%S", time.localtime(time.time()))
localpath = os.getcwd()
filepath = os.path.join(localpath, 'test_case')
# 按类加载全部testxxx测试用例
suite = unittest.defaultTestLoader.discover(filepath, 'test_[101]*.py')



xmlrunner.XMLTestRunner(output='report').run(suite) # test-reports为生成报告的目录名
