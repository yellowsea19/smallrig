# -*- coding : utf-8 -*-
#    @Author : Sen
#    @IDE    : PyCharm  sku_test
#    @Time   : 2024/11/25 19:45

import mysql.connector
from openpyxl import Workbook
import pandas as pd

class MySQLDatabase:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close_connection(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()


# 链接 smallrig-platform 库
# db = MySQLDatabase(host='localhost', user='your_username', password='your_password', database='your_database')
db = MySQLDatabase(host='192.168.133.213', user='root', password='root', database='smallrig-platform')
db.connect()

# 执行查询  新品
result = db.execute_query("""
SELECT
	p.id,
	p.product_code AS '新品',
	i.start_on_sale_time,
	DATEDIFF( NOW(), i.start_on_sale_time ),
CASE

		WHEN DATEDIFF( NOW(), i.start_on_sale_time ) >= 90 THEN
		i.start_on_sale_time ELSE DATE(
		DATE_SUB( CURDATE(), INTERVAL 90 DAY )) 
	END AS result 
FROM
	`t_product_plan_info` i,
	t_product p 
WHERE
	i.start_on_sale_time IS NOT NULL 
	AND i.del_flag = 1 
	AND p.del_flag = 1 
	AND p.id = i.product_id 
	AND DATEDIFF( NOW(), i.start_on_sale_time ) > 0 
	AND DATEDIFF( NOW(), i.start_on_sale_time ) < 60;""")
for row in result:
    print('新品:', row[1])

# 执行查询  成长期
result = db.execute_query("""SELECT
	p.id,
	p.product_code AS '成长期',
	i.start_on_sale_time,
	DATEDIFF( NOW(), i.start_on_sale_time ),
CASE

		WHEN DATEDIFF( NOW(), i.start_on_sale_time ) >= 90 THEN
		i.start_on_sale_time ELSE DATE(
		DATE_SUB( CURDATE(), INTERVAL 90 DAY )) 
	END AS result 
FROM
	`t_product_plan_info` i,
	t_product p 
WHERE
	i.start_on_sale_time IS NOT NULL 
	AND i.del_flag = 1 
	AND p.del_flag = 1 
	AND p.id = i.product_id 
	AND DATEDIFF( NOW(), i.start_on_sale_time ) >= 60 
	AND DATEDIFF( NOW(), i.start_on_sale_time ) < 120;""")
for row in result:
    print('成长期:', row[1])

# 注意 新品与成长期，也要计入到 销量与销售额中
result_a = db.execute_query("""SELECT
	p.id,
	p.product_code,
	i.start_on_sale_time,
	DATEDIFF( NOW(), i.start_on_sale_time ),
CASE

		WHEN DATEDIFF( NOW(), i.start_on_sale_time ) >= 90 THEN
		i.start_on_sale_time ELSE DATE(
		DATE_SUB( CURDATE(), INTERVAL 90 DAY )) 
	END AS result 
FROM
	`t_product_plan_info` i,
	t_product p 
WHERE
	i.start_on_sale_time IS NOT NULL 
	AND i.del_flag = 1 
	AND p.del_flag = 1 
	AND p.id = i.product_id ;""")

# 关闭连接
db.close_connection()

# 链接 smallrig-report 库
db_r = MySQLDatabase(host='192.168.133.213', user='root', password='root', database='smallrig-report')
db_r.connect()

"""    

     配置取销量与销售额的状态    
        !!! 记得配置 !!!

"""
data = " '在售', '升级待下架', '清仓待下架' "

# 创建一个Workbook对象
wb = Workbook()

# 激活默认的工作表
ws = wb.active
ws.append(['product_id', 'product_code', 'pro_num', 'sell_fee'])

for row in result_a:
    sqldata = """ 
    SELECT
	sum( product_quantity ),
	sum( actual_sell_fee ) 
FROM
	`t_sell_stat` 
WHERE
	order_time >= '%s' 
	AND product_id = '%s' 
	AND product_code = '%s' 
	AND product_status_name IN (%s) 
GROUP BY
	product_id;""" % (row[4], row[0], row[1], data)
    result_sku = db_r.execute_query(sqldata)
    # print(result_sku)
    # ws.append(result_sku)
    # print(row[0], row[1], result_sku)
    if len(result_sku) != 0:
        print(row[0], row[1], result_sku[0][0], result_sku[0][1])
        excel_data = [row[0], row[1], result_sku[0][0], result_sku[0][1]]
    else:
        print(row[0], row[1], 0, 0)
        excel_data = [row[0], row[1], 0, 0]
    ws.append(excel_data)
    wb.save("data.xlsx")

# 关闭连接
db_r.close_connection()