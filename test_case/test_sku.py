import pymysql
import unittest
from concurrent.futures import ThreadPoolExecutor
import time
from logs.log import logger


class DatabaseComparisonTestCase(unittest.TestCase):

    def setUp(self):
        # 连接数据库1 --冷库
        self.conn1 = pymysql.connect(
            host='192.168.133.235',
            user='root',
            password='root',
            db='smallrig-platform-cold'
        )

        # 连接数据库2 --热库
        self.conn2 = pymysql.connect(
            host='192.168.133.235',
            user='root',
            password='root',
            db='smallrig-platform'
        )


    def tearDown(self):
        # 关闭数据库连接
        import time
        time.sleep(5)
        self.conn1.close()
        self.conn2.close()

    def test_data_comparison(self):
        # 执行数据库1的查询 --冷 库
        cursor1 = self.conn1.cursor()
        #按天查询数据冷 库
        #查询t_order_base数据
        # SQL= """SELECT id from t_order_base where del_flag = 1 and (order_status = 4 or order_status = 6)and logistics_status = 1 AND signing_time >= '2020-05-06 00:00:00' AND signing_time <= '2020-05-06 23:59:59'
        #     union all
        #         select id from t_order_base where del_flag = 1 and (order_status = 4 or order_status = 6)and platform_id = 30  AND send_time >= '2020-05-06 00:00:00'	AND send_time <= '2020-05-06 23:59:59'
        #         """
        #查询t_order_address 数据
        SQL= """SELECT base_id FROM t_order_sys_item WHERE base_id IN (SELECT id   from t_order_base where del_flag = 1 and (order_status = 4 or order_status = 6)  and logistics_status = 1	AND signing_time >= "2020-06-06 00:00:00" AND signing_time <= "2020-06-06 23:59:59"    
                union all                                                                                                                                                                                                                                                          
                select id  from t_order_base  where del_flag = 1  and (order_status = 4 or order_status = 6) and platform_id = 30  AND send_time >= "2020-06-06 00:00:00"	AND send_time <= "2020-06-06 23:59:59");      
         """
        cursor1.execute(SQL)
        result1 = cursor1.fetchall()
        logger.info("smallrig-platform-cold冷表数据总数： "+str(len(result1)))
        for row in result1:
            self.compare_data(row)
        # # 创建线程池
        # with ThreadPoolExecutor() as executor:
        #
        #     for row in    result1 :
        #
        #         # 创建任务列表
        #         tasks = [executor.submit(self.compare_data, row) ]
        #
        #     # 获取任务结果
        #     for task in tasks:
        #         task.result()

    def compare_data(self, row):
        # 对每一行数据进行比对
        self.cursor2 = self.conn2.cursor()
        #SQL="SELECT order_code FROM t_order_base WHERE order_code='%s'; "%row[0];
        # SQL = "SELECT order_code FROM t_order_base WHERE id ='%s';"%row
        SQL =    "SELECT id FROM t_order_sys_item WHERE base_id ='%s';"%row
        # print(SQL)

        try:
            self.cursor2.execute(SQL)
        except Exception as e:
            logger.error( "error----------------------------------------------------------",e)
            # print(e)
        result2 = self.cursor2.fetchall()

        # logger.info("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        logger.info(SQL)
        # 如果在数据库2中找不到匹配的数据，则断言失败
        self.assertEqual(result2,())
        logger.info("\n"+"smallrig-platform-cold : "+str(row[0])+";"+"\n"+"smallrig-platform      ： "+ str(result2))

        # logger.info("------------------------------------------------------------------------------------")
        self.cursor2.close()

if __name__ == '__main__':
    unittest.main()







