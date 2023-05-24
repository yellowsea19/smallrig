import unittest
from ddt import ddt,data,unpack
from common.base.handle_yaml import HandleYaml
from common.base.handle_mysql import HandleMysql
from test_suite.test_pc import PC
import time
from test_suite.admin_api import Admin
import importlib,sys,os
importlib.reload(sys)


class Order(unittest.TestCase):


    # @classmethod
    # def setUpClass(cls):
    #
    #     global token,userId
    #     # token,userId = PC().pcLogin(username="314221719@qq.com ",password="a123456")


    def setUp(self):
        self.admin = Admin()
        global token,userId
        token,userId = self.admin.adminLogin(username="huanghai",password="9ccd2600a9ce6a18e157291016099627")
        print('start {}'.format(self))


    def test_create_coupon1(self):
        """创建满减优惠券，并启用
            couponName ： 优惠券名称
            couponRule ： 0 满减    1 折扣  2 兑换  3 兑换运费
            type : 优惠券类型C-1-商品券，C-2兑换券，C-3运费券
            satisfyMoney :   使用门槛
            deductionMoney :  抵扣金额(单位：分)
            discount :   打折
        """

        couponName ="满减券 100 - 80"
        #保存优惠券
        self.admin.saveCouponInfo(token,userId,type="C-1",couponName=couponName,couponRule=0,satisfyMoney=10000,deductionMoney=8000)
        #查询保存的优惠券ID
        coupon_id = self.admin.queryCouponInfoList(token,userId,couponName,type="C-1")
        #启用优惠券
        self.admin.editCouponInfoStatus(token,userId,coupon_id)

    def test_create_coupon2(self):
        """创建满折优惠券，并启用
            couponName ： 优惠券名称
            couponRule ： 0 满减    1 折扣  2 兑换  3 兑换运费
            type : 优惠券类型C-1-商品券，C-2兑换券，C-3运费券
            satisfyMoney :   使用门槛
            deductionMoney :  抵扣金额(单位：分)
            discount :   打折
        """

        couponName ="满折券 满100 打75 折"
        #保存优惠券
        self.admin.saveCouponInfo(token,userId,type="C-1",couponName=couponName,couponRule=1,satisfyMoney=10000,discount=75)
        #查询保存的优惠券ID
        coupon_id = self.admin.queryCouponInfoList(token,userId,couponName,type="C-1")
        #启用优惠券
        self.admin.editCouponInfoStatus(token,userId,coupon_id)

    def test_create_coupon3(self):
        """创建单品兑换券，并启用
            couponName ： 优惠券名称
            couponRule ： 0 满减    1 折扣  2 兑换  3 兑换运费
            type : 优惠券类型C-1-商品券，C-2兑换券，C-3运费券
            satisfyMoney :   使用门槛
            deductionMoney :  抵扣金额(单位：分)
            discount :   打折
        """

        couponName ="兑换券"
        #保存优惠券
        self.admin.saveCouponInfo(token,userId,type="C-2",couponName=couponName,couponRule=2)
        #查询保存的优惠券ID
        coupon_id = self.admin.queryCouponInfoList(token,userId,couponName,type="C-2")
        #启用优惠券
        self.admin.editCouponInfoStatus(token,userId,coupon_id)


    def test_create_coupon4(self):
        """创建包邮券，并启用
            couponName ： 优惠券名称
            couponRule ： 0 满减    1 折扣  2 兑换  3 兑换运费
            type : 优惠券类型C-1-商品券，C-2兑换券，C-3运费券
            satisfyMoney :   使用门槛
            deductionMoney :  抵扣金额(单位：分)
            discount :   打折
        """
        couponName ="包邮券"
        #保存优惠券
        self.admin.saveCouponInfo(token,userId,type="C-3",couponName=couponName,couponRule=3)
        #查询保存的优惠券ID
        coupon_id = self.admin.queryCouponInfoList(token,userId,couponName,type="C-3")
        #启用优惠券
        self.admin.editCouponInfoStatus(token,userId,coupon_id)

    def test_create_coupon5(self):
        """创建运费满减券，并启用
            couponName ： 优惠券名称
            couponRule ： 0 满减    1 折扣  2 兑换  3 兑换运费
            type : 优惠券类型C-1-商品券，C-2兑换券，C-3运费券
            satisfyMoney :   使用门槛
            deductionMoney :  抵扣金额(单位：分)
            discount :   打折
        """
        couponName ="运费满减100-8"
        #保存优惠券
        self.admin.saveCouponInfo(token,userId,type="C-3",couponName=couponName,couponRule=0,satisfyMoney=10000,deductionMoney=800)
        #查询保存的优惠券ID
        coupon_id = self.admin.queryCouponInfoList(token,userId,couponName,type="C-3")
        #启用优惠券
        self.admin.editCouponInfoStatus(token,userId,coupon_id)

    def test_generate_coupon_code(self):
        """根据优惠券ID 和 用户邮箱 创建券码 并返回优惠券码
        """
        #查询会员ID
        account="314221719@qq.com"
        coupon_id=1544265945671815170
        memberId=self.admin.memberInfoList(token,userId,account=account)
        #根据用户生成券码
        self.admin.generateCouponCodes(token,userId,couponInfoId=coupon_id,memberEmail=account,memberId=memberId)
        #根据用户查询券码
        self.admin.queryCouponCodes(token,userId,account,couponInfoId=coupon_id)






