import redis
import unittest
import pymysql
import time




class DatabaseOperations(unittest.TestCase):

    def setUp(self):
        # self.connection = pymysql.connect(host='192.168.133.233',  # 数据库地址
        #                                   user='root',  # 数据库用户名
        #                                   password='Leqi!2022',  # 数据库密码
        #                                   db='smallrig-external-platform')  # 数据库名称
        self.connection = pymysql.connect(host='192.168.133.213',  # 数据库地址
                                          user='root',  # 数据库用户名
                                          password='root',  # 数据库密码
                                          db='smallrig-external-platform')  # 数据库名称
        self.cursor = self.connection.cursor()
        # 连接 Redis 数据库---线上香港
        self.r = redis.Redis(host='r-j6cnx6188q8fzk05nkpd.redis.rds.aliyuncs.com', port=6379, db=0,
                        password="smallrig_read:jAPb3cpeV5FyFOp6")  # 默认连接本地数据库，端口为6379，db是数据库的索引值
        # 连接 Redis 数据库---线上深圳
        self.r2 = redis.Redis(host='r-wz91durbvf3wyj16fvpd.redis.rds.aliyuncs.com', port=6379, db=0,
                             password="erp_redis_read:WUrG8h9wF&^btE5J")  # 默认连接本地数据库，端口为6379，db是数据库的索引值

    def query_redis(self,key):
        res = self.r.get(key)
        return res.decode('utf-8')




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

    def delete(self, sql):
        return self.insert(sql)

    def update(self, sql):
        return self.insert(sql)

    def tearDown(self):
        self.cursor.close()
        self.connection.close()

    def test_update_IPO_token(self):
        """更新IPO环境token
        """
        print("更新IPO环境shoppe token")
        token = self.query_redis("shopee_access_token_105343606").replace('"','')
        SQL = "UPDATE `t_shopee_inter_config` SET `id`=22, `platform_id`=34, `own_warehouse_id`=57, `iss_warehouse_id`=144, `market_id`=8, `channel_id`=236, `channel_key`='channel_236', `platform_account`=NULL, `partner_id`='2004136', `partner_key`='497fcf709a4e4f71cf82d6385ac1168f6ecf11c5829e2e8f629c1de115e395e4', `shop_id`='105343606', `site`='马来(EB_Shopee)', `site_url`='https://partner.shopeemobile.com', `country_code`='MY', `del_flag`=1, `create_by`='admin', `create_time`='2020-09-27 16:01:14', `update_by`='admin', `update_time`='2020-09-27 16:01:23', `valid_begin_time`='2022-06-27 00:20:49', `valid_end_time`='2023-06-20 00:20:49', `refresh_token`='4b734c7361784e4e50624575426c5853', `refresh_valid_begin`='2023-11-22 09:00:36', `refresh_valid_end`='2023-12-22 09:00:36', `expire_time`='2043-10-22 17:23:30', `token`='%s' WHERE `id`=22;" % token
        self.update(SQL)
        token = self.query_redis("shopee_access_token_414004692").replace('"','')
        SQL = "UPDATE `t_shopee_inter_config` SET `id`=23, `platform_id`=34, `own_warehouse_id`=57, `iss_warehouse_id`=144, `market_id`=8, `channel_id`=219, `channel_key`='channel_219', `platform_account`=NULL, `partner_id`='2004136', `partner_key`='497fcf709a4e4f71cf82d6385ac1168f6ecf11c5829e2e8f629c1de115e395e4', `shop_id`='414004692', `site`='马来', `site_url`='https://partner.shopeemobile.com', `country_code`='MY', `del_flag`=1, `create_by`='admin', `create_time`='2021-07-02 14:18:26', `update_by`='admin', `update_time`='2021-07-02 14:18:34', `valid_begin_time`='2022-06-27 00:20:49', `valid_end_time`='2023-06-20 00:20:49', `refresh_token`='7553427a474c6f56474f466451564848', `refresh_valid_begin`='2023-11-22 09:04:00', `refresh_valid_end`='2023-12-22 09:04:00', `expire_time`='2043-10-22 17:23:30', `token`='%s' WHERE `id`=23;" % token
        self.update(SQL)
        token = self.query_redis("shopee_access_token_414029413").replace('"','')
        SQL = "UPDATE `t_shopee_inter_config` SET `id`=24, `platform_id`=34, `own_warehouse_id`=57, `iss_warehouse_id`=146, `market_id`=8, `channel_id`=218, `channel_key`='channel_218', `platform_account`=NULL, `partner_id`='2004136', `partner_key`='497fcf709a4e4f71cf82d6385ac1168f6ecf11c5829e2e8f629c1de115e395e4', `shop_id`='414029413', `site`='泰国', `site_url`='https://partner.shopeemobile.com', `country_code`='TH', `del_flag`=1, `create_by`='admin', `create_time`='2021-07-02 14:19:56', `update_by`='admin', `update_time`='2021-07-02 14:20:02', `valid_begin_time`='2022-06-27 00:20:49', `valid_end_time`='2023-06-20 00:20:49', `refresh_token`='434c47684b7271455a594778494e5874', `refresh_valid_begin`='2023-11-22 09:07:26', `refresh_valid_end`='2023-12-22 09:07:26', `expire_time`='2043-10-22 17:23:30', `token`='%s' WHERE `id`=24;" % token
        self.update(SQL)
        token = self.query_redis("shopee_access_token_414030866").replace('"','')
        SQL = "UPDATE `t_shopee_inter_config` SET `id`=25, `platform_id`=34, `own_warehouse_id`=57, `iss_warehouse_id`=145, `market_id`=8, `channel_id`=217, `channel_key`='channel_217', `platform_account`=NULL, `partner_id`='2004136', `partner_key`='497fcf709a4e4f71cf82d6385ac1168f6ecf11c5829e2e8f629c1de115e395e4', `shop_id`='414030866', `site`='菲律宾', `site_url`='https://partner.shopeemobile.com', `country_code`='PH', `del_flag`=1, `create_by`='admin', `create_time`='2021-07-02 14:21:02', `update_by`='admin', `update_time`='2021-07-02 14:21:06', `valid_begin_time`='2022-06-27 00:20:49', `valid_end_time`='2023-06-20 00:20:49', `refresh_token`='7476766d6c54435575685a4e714b6f46', `refresh_valid_begin`='2023-11-22 09:10:49', `refresh_valid_end`='2023-12-22 09:10:49', `expire_time`='2043-10-22 17:23:30', `token`='%s' WHERE `id`=25;" % token
        self.update(SQL)
        token = self.query_redis("shopee_access_token_631082011").replace('"','')
        SQL = "UPDATE `t_shopee_inter_config` SET `id`=26, `platform_id`=34, `own_warehouse_id`=57, `iss_warehouse_id`=57, `market_id`=8, `channel_id`=216, `channel_key`='channel_216', `platform_account`=NULL, `partner_id`='2004136', `partner_key`='497fcf709a4e4f71cf82d6385ac1168f6ecf11c5829e2e8f629c1de115e395e4', `shop_id`='631082011', `site`='香港', `site_url`='https://partner.shopeemobile.com', `country_code`='HK', `del_flag`=1, `create_by`='admin', `create_time`=NULL, `update_by`='admin', `update_time`=NULL, `valid_begin_time`='2022-06-27 00:20:49', `valid_end_time`='2023-06-20 00:20:49', `refresh_token`='4d784f434869456a7041785779556276', `refresh_valid_begin`='2023-11-22 09:55:04', `refresh_valid_end`='2023-12-22 09:55:04', `expire_time`='2043-10-22 17:23:30', `token`='%s' WHERE `id`=26;" % token
        self.update(SQL)
        token = self.query_redis("shopee_access_token_910396411").replace('"','')
        SQL = "UPDATE `t_shopee_inter_config` SET `id`=30, `platform_id`=34, `own_warehouse_id`=57, `iss_warehouse_id`=234, `market_id`=8, `channel_id`=213, `channel_key`='channel_213', `platform_account`='', `partner_id`='2004136', `partner_key`='497fcf709a4e4f71cf82d6385ac1168f6ecf11c5829e2e8f629c1de115e395e4', `shop_id`='910396411', `site`='菲律宾', `site_url`='https://partner.shopeemobile.com', `country_code`='PH', `del_flag`=1, `create_by`='admin', `create_time`='2022-12-07 17:23:42', `update_by`='admin', `update_time`='2022-12-07 17:23:47', `valid_begin_time`='2022-12-07 14:20:49', `valid_end_time`='2023-12-07 14:21:07', `refresh_token`='45705355704e4c6d70684962446d795a', `refresh_valid_begin`='2023-11-22 10:30:20', `refresh_valid_end`='2023-12-22 10:30:20', `expire_time`='2043-10-22 17:23:30', `token`='%s' WHERE `id`=30;" % token
        self.update(SQL)
        token = self.query_redis("shopee_access_token_911017735").replace('"','')
        SQL = "UPDATE `t_shopee_inter_config` SET `id`=29, `platform_id`=34, `own_warehouse_id`=57, `iss_warehouse_id`=57, `market_id`=8, `channel_id`=215, `channel_key`='channel_215', `platform_account`='', `partner_id`='2004136', `partner_key`='497fcf709a4e4f71cf82d6385ac1168f6ecf11c5829e2e8f629c1de115e395e4', `shop_id`='911017735', `site`='泰国', `site_url`='https://partner.shopeemobile.com', `country_code`='TH', `del_flag`=1, `create_by`='admin', `create_time`='2022-12-07 17:23:42', `update_by`='admin', `update_time`='2022-12-07 17:23:47', `valid_begin_time`='2022-12-07 14:20:49', `valid_end_time`='2023-12-07 14:21:07', `refresh_token`='575179694e6761716467516e4e577465', `refresh_valid_begin`='2023-11-22 10:25:03', `refresh_valid_end`='2023-12-22 10:25:03', `expire_time`='2043-10-22 17:23:30', `token`='%s' WHERE `id`=29;" % token
        self.update(SQL)
        token = self.query_redis("shopee_access_token_911019240").replace('"','')
        SQL = "UPDATE `t_shopee_inter_config` SET `id`=28, `platform_id`=34, `own_warehouse_id`=57, `iss_warehouse_id`=57, `market_id`=8, `channel_id`=214, `channel_key`='channel_214', `platform_account`=NULL, `partner_id`='2004136', `partner_key`='497fcf709a4e4f71cf82d6385ac1168f6ecf11c5829e2e8f629c1de115e395e4', `shop_id`='911019240', `site`='菲律宾', `site_url`='https://partner.shopeemobile.com', `country_code`='PH', `del_flag`=1, `create_by`='admin', `create_time`='2022-12-07 17:23:42', `update_by`='admin', `update_time`='2022-12-07 17:23:47', `valid_begin_time`='2022-12-07 14:20:49', `valid_end_time`='2023-12-07 14:21:07', `refresh_token`='6475624c6f58774c474e466878744b4c', `refresh_valid_begin`='2023-11-22 10:30:55', `refresh_valid_end`='2023-12-22 10:30:55', `expire_time`='2043-10-22 17:23:30', `token`='%s' WHERE `id`=28;" % token
        self.update(SQL)
        token = self.query_redis("shopee_access_token_911019866").replace('"','')
        SQL = "UPDATE `t_shopee_inter_config` SET `id`=27, `platform_id`=34, `own_warehouse_id`=57, `iss_warehouse_id`=57, `market_id`=8, `channel_id`=212, `channel_key`='channel_212', `platform_account`=NULL, `partner_id`='2004136', `partner_key`='497fcf709a4e4f71cf82d6385ac1168f6ecf11c5829e2e8f629c1de115e395e4', `shop_id`='911019866', `site`='马来', `site_url`='https://partner.shopeemobile.com', `country_code`='MY', `del_flag`=1, `create_by`='admin', `create_time`='2022-12-07 17:20:36', `update_by`='admin', `update_time`='2022-12-07 17:20:43', `valid_begin_time`='2022-12-07 14:20:49', `valid_end_time`='2023-12-07 14:21:07', `refresh_token`='6f6b4353514d43734a4f7a5051734d72', `refresh_valid_begin`='2023-11-22 09:00:01', `refresh_valid_end`='2023-12-22 09:00:01', `expire_time`='2043-10-22 17:23:30', `token`='%s' WHERE `id`=27;" % token
        self.update(SQL)
        token = self.query_redis("shopee_access_token_950539910").replace('"','')
        SQL = "UPDATE `t_shopee_inter_config` SET `id`=31, `platform_id`=34, `own_warehouse_id`=57, `iss_warehouse_id`=57, `market_id`=8, `channel_id`=204, `channel_key`='channel_204', `platform_account`='', `partner_id`='2004136', `partner_key`='497fcf709a4e4f71cf82d6385ac1168f6ecf11c5829e2e8f629c1de115e395e4', `shop_id`='950539910', `site`='巴西', `site_url`='https://partner.shopeemobile.com', `country_code`='BR', `del_flag`=1, `create_by`='admin', `create_time`='2023-03-01 10:23:42', `update_by`='admin', `update_time`='2023-03-01 10:23:47', `valid_begin_time`='2023-03-01 10:20:49', `valid_end_time`='2024-03-01 10:21:07', `refresh_token`='567a6b446554784e486f484741727767', `refresh_valid_begin`='2023-11-22 09:00:25', `refresh_valid_end`='2023-12-22 09:00:25', `expire_time`='2043-10-22 17:23:30', `token`='%s' WHERE `id`=31;" % token
        self.update(SQL)
        token = self.query_redis("shopee_access_token_950540393").replace('"','')
        SQL = "UPDATE `t_shopee_inter_config` SET `id`=32, `platform_id`=34, `own_warehouse_id`=57, `iss_warehouse_id`=57, `market_id`=8, `channel_id`=203, `channel_key`='channel_203', `platform_account`='', `partner_id`='2004136', `partner_key`='497fcf709a4e4f71cf82d6385ac1168f6ecf11c5829e2e8f629c1de115e395e4', `shop_id`='950540393', `site`='墨西哥', `site_url`='https://partner.shopeemobile.com', `country_code`='MX', `del_flag`=1, `create_by`='admin', `create_time`='2023-03-01 10:23:42', `update_by`='admin', `update_time`='2023-03-01 10:23:47', `valid_begin_time`='2023-03-01 10:20:49', `valid_end_time`='2024-03-01 10:21:07', `refresh_token`='586b5248667274415166746e47726864', `refresh_valid_begin`='2023-11-22 10:30:21', `refresh_valid_end`='2023-12-22 10:30:21', `expire_time`='2043-10-22 17:23:30', `token`='%s' WHERE `id`=32;" % token
        self.update(SQL)
        token = self.query_redis("shopee_access_token_950543695").replace('"','')
        SQL = "UPDATE `t_shopee_inter_config` SET `id`=33, `platform_id`=34, `own_warehouse_id`=57, `iss_warehouse_id`=57, `market_id`=8, `channel_id`=202, `channel_key`='channel_202', `platform_account`='', `partner_id`='2004136', `partner_key`='497fcf709a4e4f71cf82d6385ac1168f6ecf11c5829e2e8f629c1de115e395e4', `shop_id`='950543695', `site`='台湾', `site_url`='https://partner.shopeemobile.com', `country_code`='TW', `del_flag`=1, `create_by`='admin', `create_time`='2023-03-01 10:23:42', `update_by`='admin', `update_time`='2023-03-01 10:23:47', `valid_begin_time`='2023-03-01 10:20:49', `valid_end_time`='2024-03-01 10:21:07', `refresh_token`='65765641694a61737972727056674679', `refresh_valid_begin`='2023-11-22 07:55:05', `refresh_valid_end`='2023-12-22 07:55:05', `expire_time`='2043-10-22 17:23:30', `token`='%s' WHERE `id`=33;" % token
        self.update(SQL)
        # print("更新快手token")
        # token = self.query_redis2("external-platform:kuaishou:ks_access_token:1").replace('"', '')
        # print("快手token:")
        # SQL = "UPDATE `t_ks_inter_config` SET `id`=1, `platform_id`=58, `own_warehouse_id`=57, `iss_warehouse_id`=57, `market_id`=10, `channel_id`=150, `channel_key`='channel_150', `app_key`='ks654992271087362695', `app_secret`='oyd480-nqZIGCNT6DIbiJA', `sign_secret`='175767886208db99fef0db1eafc120a2', `redirect_uri`='https://sysmall.smallrig.com/#/', `app_scope`='merchant_shop,merchant_refund,merchant_funds,merchant_item,merchant_order,user_info,merchant_promotion,merchant_user,merchant_comment,merchant_logistics', `refresh_token`='ChJvYXV0aC5yZWZyZXNoVG9rZW4SsAEknn9KeOJHnjWRs3hNs_0QA8pTVXrnOiyGM57PE73SESNORH0aIdNKp176i37n12ONQkgBUrt2z1Jn-5gW1wHXbh_-q6RHWhpp8NN9SK2NYuH_N8WlUq3dzKu4BiWdStSpE_-US_Fm6bjpOr_7DjGHHG2kX7uFnt_eeQtVdyq0J-sojMfUCgWxGfJc_iA2SBNdFai3qB0O-xqmv4xq0QHnQtVkXEts2Xu9SVUu-2LX3xoSDGKw_gblK2yrw7KBQ7UhJH0KIiDDd25EL54s7VrPkYZhCv-VAvjWF_ty4KCv6Q-HXvPkUigFMAE', `valid_begin_time`='2023-11-19 06:58:00', `valid_end_time`='2024-05-17 06:58:00', `del_flag`=1, `create_by`='sys', `create_time`='2022-05-19 18:03:20', `update_by`='sys', `update_time`='2023-11-19 06:58:00', `expire_time`='2053-10-22 17:23:30', `token`='%s' WHERE `id`=1;" % token
        # print(token)
        # self.update(SQL)

        # time.sleep(1800)

        # self.test_update_shopee()

    def test_update_token_pro(self):
        #香港数据库--线上
        self.connection2 = pymysql.connect(host='jump.smallrig.net',  # 数据库地址
                                          user='066383c9-8158-4a4f-af34-046bd7da870a',  # 数据库用户名
                                          password='AN7dab2Ij6cbQrTI',  # 数据库密码
                                          port=30007,
                                          db='smallrig-external-platform')  # 数据库名称
        self.cursor2 = self.connection2.cursor()
        #查询线上token
        sql = "select auth_token from  t_allegro_inter_config"
        self.cursor2.execute(sql)
        auth_token = self.cursor2.fetchall()[0][0]
        SQL = "UPDATE `t_allegro_inter_config` SET `id`=5, `platform_id`=35, `market_id`=7, `channel_id`=51, `channel_key`='channel_51', `platform_account`='smallrig', `client_id`='b866ae42126a41129da3e7e37793eab1', `client_secret`='jLxGIViWOTaknLjT9dFj34dwKA2ZrRgwV30C9zdzkMiKyll0HQNWf5b3Y3cSh1eu', `auth_token`='%s', `refresh_token`='', `redirect_uri`='https://sysmall.smallrig.com/', `expires_in`=43199, `del_flag`=1, `create_by`='liqilin', `create_time`='2021-03-16 09:25:02', `update_by`='liqilin', `update_time`='2033-11-28 11:02:46', `request_token_url`='https://allegro.pl', `request_api_url`='https://api.allegro.pl', `valid_begin_time`='2022-01-24 12:02:49', `valid_end_time`='2040-01-24 12:02:52' WHERE `id`=5;"%auth_token
        print("更新allegro token:")
        self.update(SQL)
        #-----------------------------------------------------------------------
        sql = "select token from  t_youzan_config"
        self.cursor2.execute(sql)
        token = self.cursor2.fetchall()[0][0]
        SQL = "UPDATE `t_youzan_config` SET `id`=1, `user_account`='18127064716', `own_warehouse_id`=57, `iss_warehouse_id`=57, `platform_id`=49, `market_id`=10, `channel_id`=123, `channel_key`='channel_123', `grant_id`='91371958', `token`='%s', `expiration_time`='2025-12-03 00:00:00', `valid_begin_time`=NULL, `valid_end_time`=NULL WHERE `id`=1;" % token
        print("更新友赞token:")
        self.update(SQL)


    def test_redis(self):
        token = self.r2.get("ks_access_token_1")
        print(token)




    def test_update_token_to_IPO(self):
        self.test_update_IPO_token()
        self.test_update_token_pro()







