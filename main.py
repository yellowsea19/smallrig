import time
import unittest
import os
from BeautifulReport import BeautifulReport
from common.base.handle_yaml import HandleYaml

do_yaml = HandleYaml(r"conf/base.yaml")
now = time.strftime("%Y-%m-%d %H：%M：%S", time.localtime(time.time()))
localpath = os.getcwd()
filepath = os.path.join(localpath, 'test_case')
# 按类加载全部testxxx测试用例
suite = unittest.defaultTestLoader.discover(filepath, 'test_[a,b,p]*.py')

# 加载执行用例生成报告
result = BeautifulReport(suite)
# 定义报告属性
result.report(description=do_yaml.get_data("report", "description"),
              filename=os.path.join("Reports", do_yaml.get_data("report", "filename") + now),
              theme='theme_default', log_path=filepath)

