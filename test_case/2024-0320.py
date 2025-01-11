"""
根据execl写入菜单
"""

import openpyxl
import pandas as pd
import pymysql
import unittest
from datetime import datetime
import pymongo
from pymongo import MongoClient
import json
from bson import ObjectId
from pull_order import pull_order

class TestMongoDB(unittest.TestCase):
    def setUp(self):
        self.connection = pymysql.connect(host='192.168.133.213',  # 数据库地址
                                          user='root',  # 数据库用户名
                                          password='root',  # 数据库密码
                                          db='smallrig-platform')  # 数据库名称
        self.cursor = self.connection.cursor()

    def query(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def insert(self, sql):
        try:
            res = self.cursor.execute(sql)
            print(res)
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            return False





    def read_excel_data(self,file_path):
        # 打开 Excel 文件
        workbook = openpyxl.load_workbook(file_path)
        # 选择第一个工作表
        sheet = workbook.active
        data = []
        # 遍历每一行数据
        for row in sheet.iter_rows(values_only=True):
            row_data = {}
            for i, value in enumerate(row):
                row_data[f'Column{i + 1}'] = value
            data.append(row_data)
        return data

    def test_write_data(self):
        """获取execl数据"""
        file_path = r'C:\Users\huanghai\Downloads\menu.xlsx'
        excel_data = self.read_excel_data(file_path)
        for i in excel_data:
            # 拿到上级所有目录
            if i['Column2'] == '-':
                # 上级是第5列
                if i['Column5'] is not None and i['Column4'] == '-':
                    parend_name = i['Column5']
                    SQL = f'select id from sys_menu where name = "{parend_name}"and del_flag=1 and system_code="SCXT_SUB"'
                    res = self.query(SQL)
                    if len(res) != 1:
                        raise NameError('无法找到%s'%parend_name)
                    else:
                        parend_id = res[0][0]

                # 上级是第3列
                elif i['Column5'] ==i['Column4']  is None  and i['Column3'] is not None and i['Column2'] == '-':
                    parend_name = i['Column3']
                    SQL = f'select id from sys_menu where name = "{parend_name}"and del_flag=1 and system_code="SCXT_SUB"'
                    res = self.query(SQL)
                    if len(res) != 1:
                        raise NameError('无法找到%s' % parend_name)
                    else:
                        parend_id = res[0][0]
            else:
                sql = f"INSERT INTO `sys_menu` ( `parent_id`, `name`, `url`, `permission_url`, `perms`, `type`, `icon`, `sort`, `is_hide`, `system_code`, `privilage`, `remark`, `del_flag`, `create_by`, `create_time`, `update_by`, `update_time`, `project_code`) VALUES ( {parend_id}, '{i['Column1']}', '', NULL, '{i['Column2']}', 2, '', 0, 0, 'SCXT_SUB', 1, NULL, 1, '姚权株', '2024-03-20 17:46:26', '姚权株', '2024-03-20 17:46:26', '0');"
                print(sql)
                self.insert(sql)





