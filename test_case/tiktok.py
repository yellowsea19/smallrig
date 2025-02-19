import time
from decimal import Decimal, ROUND_HALF_UP
import pandas as pd
import pymysql,requests
import unittest
from datetime import datetime
import pymongo
from pymongo import MongoClient
import json
import math
from jsonpath import jsonpath
from bson import ObjectId

from pull_order import pull_order,pull_rma_order,pull_order_fee,pull_order_return_fee

class TestMongoDB(unittest.TestCase):
    def setUp(self,env='test'):
        self.env = env
        if self.env == 'test':
            self.client = MongoClient(
                "mongodb://smallrig:smallrig@192.168.133.223:27017/?authMechanism=SCRAM-SHA-1&authSource=smallrig&directConnection=true")
            self.db = self.client['smallrig']

            self.urls = 'http://192.168.133.223:5555'
            self.xxl_url = 'http://192.168.133.223:19010'
            self.connection = pymysql.connect(host='192.168.133.213',  # 数据库地址
                                              user='root',  # 数据库用户名
                                              password='root',  # 数据库密码
                                              db='smallrig-platform',
                                              cursorclass = pymysql.cursors.DictCursor)  # 数据库名称
            self.cursor = self.connection.cursor()
        elif self.env == 'uat':
            self.client = MongoClient(
                "mongodb://smallrig:smallrig@192.168.133.233:27017/?authMechanism=DEFAULT&authSource=admin")
            self.db = self.client['smallrig']
            self.urls = 'https://bereal.smallrig.net'
            self.xxl_url = 'http://192.168.133.232:19010'
            self.connection = pymysql.connect(host='192.168.133.233',  # 数据库地址
                                              user='root',  # 数据库用户名
                                              password='Leqi!2022',  # 数据库密码
                                              db='smallrig-platform',
                                              cursorclass = pymysql.cursors.DictCursor)  # 数据库名称
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

    def delete(self, sql):
        return self.insert(sql)

    def update(self, sql):
        return self.insert(sql)

    def test_connection(self):
        self.assertIsNotNone(self.db)



    def handle_objectid(self,data):
        """递归转换 MongoDB 数据，将所有 ObjectId 转化为字符串"""
        if isinstance(data, dict):
            for key, value in data.items():
                data[key] = self.handle_objectid(value)
        elif isinstance(data, list):
            for index, item in enumerate(data):
                data[index] = self.handle_objectid(item)
        elif isinstance(data, ObjectId):
            return str(data)
        return data

    def test_pull_mongo_order_to_oms(self,platformId=59,env='test'):
        db_list = ["tiktok_order_struct"]
        for db in db_list:
            print(
                "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]
            query = {"insertTime": {"$gte": "2024-08-15 00:00:00", "$lte": "2024-09-00 23:59:59"},
                     "platformId": platformId,
                     "finishFlag": True
                     }

            results = collection.find(query).sort('insertTime', pymongo.ASCENDING)
            for k in results:
                k = self.handle_objectid(k)
                print(k)
                pull_order(env=env, id=k['_id'], platformId=platformId)
                # pull_order_fee(env=env, id=k['_id'], platformId=platformId)
                # pull_order_return_fee(env=env, id=k['_id'], platformId=48)


    def test_actual_refund(self,platformId=59,env='test'):
        """
        F1 ERP V6.0.28_20241212
       【平台账单收入项目】TikTok实退金额逻辑更新
        """
        db_list = ["return_order_struct"]
        for db in db_list:
            print(
                "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]
            query = {"insertTime": {"$gte": "2024-12-01 00:00:00", "$lte": "2024-12-29 23:59:59"},
                     "platformId": platformId,
                     # "orderId":"4035249681856041903",
                     "finishFlag": True
                     }

            results = collection.find(query).sort('insertTime', pymongo.ASCENDING)
            for k in results:
                k = self.handle_objectid(k)
                print(k['orderId'])
                actual_refund_path = '$.order.return_line_items'
                order_status = jsonpath(k,'$..return_status')
                print("状态：",order_status)
                order_source_code = jsonpath(k, '$.order.order_id')
                print("平台订单号：", order_source_code)
                if order_status[0] == 'RETURN_OR_REFUND_REQUEST_CANCEL':
                    print("实退： 0")
                else:
                    refund_total_path = '$.order.return_line_items[*].refund_amount.refund_total'
                    refund_total = jsonpath(k, refund_total_path)
                    if refund_total:
                        refund_total = refund_total
                    print("refund_total:",refund_total)
                    product_platform_discount_path = 'order.discount_amount[*].product_platform_discount'
                    product_platform_discount = jsonpath(k, product_platform_discount_path)
                    if product_platform_discount:
                        product_platform_discount = product_platform_discount
                    print("product_platform_discount:", product_platform_discount)

                    shipping_fee_platform_discount = '$.order.discount_amount[*].shipping_fee_platform_discount'
                    shipping_fee_platform_discount = jsonpath(k, shipping_fee_platform_discount)
                    if shipping_fee_platform_discount:
                        shipping_fee_platform_discount = shipping_fee_platform_discount
                    print("shipping_fee_platform_discount:", shipping_fee_platform_discount)
                    sku_actual_list = []
                    product_discount_sum_list = []
                    shipping_discount_sum_list = []
                    num = len(refund_total)
                    num_index = 1
                    for i in refund_total:
                        if  num_index == num :
                            product_discount_sum_list = sum(Decimal(x) for x in product_discount_sum_list)
                            shipping_discount_sum_list = sum(Decimal(x) for x in shipping_discount_sum_list)
                            sku_actual_list = sum(Decimal(x) for x in sku_actual_list)

                            refund_total = sum(Decimal(x) for x in refund_total)
                            product_platform_discount = sum(Decimal(x) for x in product_platform_discount)
                            shipping_fee_platform_discount = sum(Decimal(x) for x in shipping_fee_platform_discount)
                            sku_actual =  refund_total + product_platform_discount + shipping_fee_platform_discount - sku_actual_list
                            print("第%s个实退："%num_index,sku_actual)
                            num_index = num_index + 1
                        else:
                            i = Decimal(i)
                            product_discount_sum = sum(Decimal(x) for x in product_platform_discount)
                            refund_total_sum = sum(Decimal(x) for x in refund_total)
                            shipping_discount_sum = sum(Decimal(x) for x in shipping_fee_platform_discount)
                            # 计算 sku_actual
                            if refund_total_sum != 0:
                                sku_actual = (
                                        i
                                        + product_discount_sum * (i / refund_total_sum)
                                        + shipping_discount_sum * (i / refund_total_sum)    )
                                sku_actual = round(sku_actual, 9)
                                print("第%s个实退："%num_index,sku_actual)
                                sku_actual_list.append(sku_actual)
                                product_discount_sum_list.append(product_discount_sum * (i / refund_total_sum))
                                shipping_discount_sum_list.append(shipping_discount_sum * (i / refund_total_sum))


                            else:
                                print("Error: refund_total_sum is zero.")
                            num_index = num_index + 1



                print("--------------------------- end --------------------------------")


    def test_Fix_rma(self):
        """
        修复历史数据
        """
        url = "http://192.168.133.223:15010/rmaOrder/v1/fixRmaRefundAmount"
        headers = { 'Content-Type': 'application/json'}
        data = {
                "platformId": 59,
                "createTimeBegin": "2024-07-01 10:00:00",
                "createTimeEnd": "2024-12-12 10:00:00",
                "platformRmaCodes": [
                    "4035257547448684586"
                ]
            }
        res = requests.post(url=url,headers=headers,json=data)
        print(res.text)

    def test_pull_rma_to_order(self,platformId=34,platform_rma_code='24060406651HRPA'):
        """
        清洗RMA单--
        根据退货退款单号，找到订单号，清洗订单号，然后若退货退款单号存在，则先删再清洗
        """
        db_list = ["return_order_struct"]
        for db in db_list:
            print(
                "-----------------------------------------" + db + "----------------------------------------------" + "\n")
            collection = self.db[db]
            query = {
                     "platformId": platformId,
                     "orderId":f'{platform_rma_code}',
                     "finishFlag": True
                     }

            results = collection.find(query).sort('insertTime', pymongo.DESCENDING)
            try:
                #取出最新的一条RMA数据
                k = next(results)
                print("退货退款单号： ",k['orderId'],"----",k['_id'])

                #获取订单号
                if platformId == 59:
                    order_db = "tiktok_order_struct"
                    source_code  = jsonpath (k,'$.order.order_id')[0]
                elif platformId == 34:
                    order_db = "shopee_order_struct"
                    source_code = jsonpath(k, '$.order.order_sn')[0]
                elif platformId == 39:
                    order_db = "lazada_order_struct"
                    source_code = jsonpath(k, '$.order.trade_order_id')[0]
                print("平台订单号： ",source_code)
            except KeyboardInterrupt:
                print("mongo中无该退货退款单数据 ： ",platform_rma_code)
            except StopIteration:
                print("mongo中无该退货退款单数据 ： ", platform_rma_code)

            try:
                #清洗订单数据
                order_query = {"orderId":f'{source_code}',
                                "finishFlag": True}
                collection_order = self.db[order_db]
                order_result = collection_order.find(order_query).sort('insertTime', pymongo.DESCENDING)
                order_info =next(order_result)
                order_id = next(order_result)['_id']

                print(order_id)
                pull_order(env=self.env,id=order_id,platformId=platformId)
                time.sleep(3)
                # 把订单改成已发货
                update_order_status_sql = "update t_order_base set order_status = 4 where source_code = '%s'" % \
                                          order_info['orderId']
                # self.update(update_order_status_sql)
                del_rma_order_sql = 'delete from t_rma_order where platform_rma_code = "%s"'%platform_rma_code
                self.delete(del_rma_order_sql)
                pull_rma_order(env=self.env,id=k['_id'],platformId=platformId)
            except UnboundLocalError:
                print("mongo 中没有订单数据的版本，订单号： ",source_code)
            except StopIteration :
                print("mongo 中没有订单数据的版本，订单号： ", source_code)


    def test_tiktok_return_order(self,platformId = 59, platform_rma_code_list = ['2411060GWJJ1WU3']):
        out_data_list = []
        for platform_rma_code in platform_rma_code_list:
            db_list = ["return_order_struct"]
            for db in db_list:
                print(
                    "-----------------------------------------" + db + "----------------------------------------------" + "\n")
                collection = self.db[db]
                query = {
                    "platformId": platformId,
                    "orderId": f'{platform_rma_code}',
                    "finishFlag": True
                }

                results = collection.find(query).sort('insertTime', pymongo.DESCENDING)
                try:
                    # 取出最新的一条RMA数据
                    k = next(results)
                    print("退货退款单号： ", k['orderId'], "----", k['_id'])

                    # 获取订单号

                    order_db = "tiktok_order_struct"
                    source_code = jsonpath (k,'$.order.order_id')[0]
                    print("平台订单号： ", source_code)
                except KeyboardInterrupt:
                    print("mongo中无该退货退款单数据 ： ", platform_rma_code)
                except StopIteration:
                    print("mongo中无该退货退款单数据 ： ", platform_rma_code)

                try:
                    order_query = {"orderId": f'{source_code}',
                                   "finishFlag": True}
                    collection_order = self.db[order_db]
                    order_result = collection_order.find(order_query).sort('insertTime', pymongo.DESCENDING)
                    order_info = next(order_result)
                    order_id = order_info['_id']

                    # 清洗订单数据 & 售后单
                    pull_order(env=self.env, id=order_id, platformId=platformId)
                    time.sleep(1)
                    # 把订单改成已发货
                    update_order_status_sql = "update t_order_base set order_status = 4 where source_code = '%s'" % \
                                              order_info['orderId']
                    self.update(update_order_status_sql)
                    # 若退货退款单已存在，则删除重新清洗
                    del_rma_order_sql = 'delete from t_rma_order where platform_rma_code = "%s"' % platform_rma_code
                    self.delete(del_rma_order_sql)
                    pull_rma_order(env=self.env, id=k['_id'], platformId=platformId)
                    print("orderId",order_id)

                    # 查询数据库rma_type的值
                    mysql_result_rma_type_sql = "select rma_type from t_rma_order where platform_rma_code = '%s'" % platform_rma_code
                    result = self.query(mysql_result_rma_type_sql)
                    for i in result:
                        result_rma_type = i['rma_type']
                    # 查询数据库return_type 的值
                    mysql_result_return_type_sql = "select return_type from t_rma_order_return where rma_id =  (select id from t_rma_order where platform_rma_code = '%s')" % platform_rma_code
                    result = self.query(mysql_result_return_type_sql)
                    for i in result:
                        result_return_type = i['return_type']

                    # refund_type查询数据库 的值
                    mysql_result_refund_type = "select refund_type from t_rma_order_refund where rma_code =  (select rma_code from t_rma_order where platform_rma_code = '%s')" % platform_rma_code
                    result = self.query(mysql_result_refund_type)
                    for i in result:
                        result_refund_type = i['refund_type']


                except UnboundLocalError:
                    print("mongo 中没有订单数据的版本，订单号： ", source_code)
                except StopIteration:
                    print("mongo 中没有订单数据的版本，订单号： ", source_code)

    def test_0120_init(self):
        platform_rma_code_list = ["4035267864692232384","4035267663085277690","4035267530732442167","4035267530732573239","4035267452369736386","4035267447496151461","4035267410877190971","4035267410088268603","4035267410877322043","4035267374673399978","4035267375294877866","4035267325642707020","4035267316431163704","4035267286671332060","4035267232635654234","4035267139307672047","4035267124185043376","4035267097854841699","4035267095274164667","4035267062120812549","4035267056157823137","4035267045125755805","4035267044386182045","4035267039690658107","4035267014226186915","4035267004428357998","4035267003381682542","4035267004428489070","4035266971181487043","4035266940330021587","4035266892614439073","4035266887189958689","4035266775080145811","4035266701179786025","4035266666774565691","4035266610211951247","4035266606891438092","4035266550968848449","4035266530123092157","4035266459861619243","4035266375151030433","4035266355943412683","4035266270381248941","4035266240958993155","4035266093908857346","4035266033832399725","4035266019856651208","4035265989694624515","4035265885830549786","4035265812138726395","4035265763018969859","4035265695511187514","4035265680698675870","4035265674498904468","4035265673771323432","4035265652354421251","4035265634510279217","4035265568144331184","4035265427928945403","4035265403077038716","4035265377016451829","4035265211112919567","4035265145641013676","4035265109815758937","4035265081946313541","4035265061833315284","4035265039791853646","4035264920970170430","4035264863346856397","4035264852509168636","4035264687545028626","4035264682558919263","4035264647291966062","4035264643773731733","4035264486825431201","4035264445980315922","4035264425643380880","4035264347661242766","4035264315970392249","4035264307452088756","4035264194718109709","4035264172094820465","4035264167691981082","4035264142618825523","4035264104335774583","4035263946231877812","4035263864181330548","4035263719838814856","4035263687755600323","4035263641803395546","4035263596026105927","4035263582275670433","4035263443370611521","4035263332514239416","4035263322228560662","4035263280135574137","4035263236590309702","4035263203421491270","4035263161811374107","4035263117943279846","4035263062555463880","4035262996916441749","4035262997409992896","4035262983545655473","4035262826619834824","4035262801511223522","4035262795092234534","4035262784052630159","4035262779625673629","4035262675218829996","4035262657754927787","4035262644606767141","4035262450022256969","4035262432375771827","4035262397836923706","4035262302341009868","4035262224181203476","4035261973212467329","4035261865335624495","4035261865196294959","4035261794190397541","4035261765061873814","4035261631079288961","4035261586680943555","4035261509470556399","4035261504979440348","4035261419668279697","4035261399391834299","4035261356953473353","4035261299935449174","4035261260446667367","4035261241172791841","4035261212965572911","4035261057234735995","4035261046227439810","4035261038132236408","4035260958507766635","4035260838445289691","4035260781022516010","4035260706385925092","4035260692359909440","4035260595213275518","4035260538736185817","4035260531616354609","4035260483272020692","4035260411039683229","4035260402688299987","4035260382277440407","4035260383314153671","4035260331554017755","4035260313406051323","4035260203814523899","4035260188048527876","4035260184327066198","4035260128886100458","4035260124981924339","4035260097649414851","4035260088697393663","4035260079608665083","4035260021672809227","4035260014469288677","4035259943498978269","4035259943498847197","4035259911243338039","4035259900679983577","4035259867213697589","4035259740829160110","4035259581700084491","4035259568192525018","4035259515900235927","4035259492285518076","4035259367251939822","4035259316221284519","4035259290438898320","4035259188510298982","4035259120877212314","4035259101733032497","4035259101980430897","4035259044781199816","4035259032034119809","4035258982684201155","4035258980503752871","4035258733371364203","4035258725214490801","4035258711615836266","4035258667735093300","4035258661636117446","4035258605324636318","4035258590078275668","4035258584678633691","4035258576523465586","4035258576523727730","4035258576523596658","4035258576678720080","4035258571190210985","4035258559137878682","4035258559138009754","4035258559138140826","4035258517963117106","4035258481283076157","4035258286064177822","4035258262087570430","4035258225562980994","4035258224158282370","4035258218009039423","4035258210529547041","4035258184438091863","4035258178195329386","4035258136897819111","4035258119000789185","4035258112187994754","4035258079532454018","4035258023946785135","4035258014415687895","4035258014415556823","4035257998835421272","4035257991298781747","4035257982577447207","4035257982606086439","4035257962237300865","4035257895464243792","4035257881404674466","4035257854182789780","4035257827810513378","4035257741783109731","4035257741782978659","4035257708280975821","4035257658908709560","4035257587671798040","4035257586747282278","4035257547448684586","4035257485414207558","4035257465640226946","4035257408931402303","4035257399980430331","4035257313761202730","4035257289836106611","4035257246047048098","4035257188216377942","4035257182956720460","4035257154024870113","4035257146761122458","4035256987013320955","4035256901644226972","4035256901644489116","4035256901643964828","4035256901644095900","4035256901644358044","4035256894850306739","4035256863036444722","4035256808379224334","4035256803571241213","4035256788393104248","4035256776511557808","4035256754943398747","4035256702201401597","4035256624243380495","4035256599552823433","4035256599552954505","4035256523122446954","4035256451543634732","4035256418218316022","4035256412595720946","4035256393885454899","4035256353129599401","4035256305789211576","4035256283265668027","4035256269392679677","4035256264843170379","4035256264109166798","4035256179881579435","4035256165086564759","4035256118462419723","4035256065292866235","4035256014279512139","4035255999982571817","4035255985339536060","4035255956135579807","4035255947692643131","4035255847280414815","4035255833488823015","4035255821638799776","4035255773683683555","4035255754784608346","4035255748021227590","4035255678081470626","4035255636174541441","4035255573648544097","4035255537535520972","4035255534459326561","4035255479307637252","4035255456028332238","4035255453831435261","4035255453831304189","4035255437064901117","4035255405912101315","4035255384396042582","4035255342353649702","4035255339527213507","4035255191118713169","4035255036068860733","4035254905043063777","4035254905042932705","4035254826591949543","4035254738207936867","4035254734557581428","4035254697420624289","4035254609353348068","4035254609337684813","4035254500325167485","4035254482691264518","4035254482691133446","4035254389565329600","4035254310990221435","4035254252815684250","4035254246642389698","4035254241538248729","4035254241538117657","4035254229817725395","4035254213934617410","4035254211370586574","4035254163979014430","4035254114882654338","4035254098706600701","4035254095443890214","4035254088245285177","4035254081731400572","4035254076239483104","4035254037129630542","4035254035732534094","4035254022141416430","4035254015030367029","4035254004932121494","4035253985568854586","4035253960729793111","4035253960729596503","4035253888334336261","4035253811265900786","4035253679991263509","4035253673829109760","4035253670729519493","4035253633331335386","4035253602501759924","4035253579625107593","4035253579625238665","4035253501304148470","4035253499441942897","4035253399558066746","4035253362750361711","4035253360239743478","4035253337701716139","4035253321046856695","4035253304369254553","4035253238111638392","4035253167975993575","4035253120261066769","4035253085968503451","4035253069095867202","4035253069095736130","4035252955776848664","4035252912133804133","4035252861446099090","4035252693710180885","4035252638090367297","4035252612852584745","4035252610690225126","4035252575267361587","4035252503222719021","4035252495328121041","4035252477450162663","4035252473649926701","4035252443187023912","4035252404060197770","4035252376828548070","4035252312354886301","4035252168020497090","4035252168020366018","4035252110885163666","4035252055476506902","4035252055327085370","4035252043703161034","4035252012830397200","4035251808645452486","4035251715217527272","4035251706939806221","4035251706939675149","4035251706715607688","4035251624080609772","4035251625062273998","4035251625062405070","4035251625062142926","4035251578932990141","4035251579651068093","4035251524809823080","4035251509397328087","4035251481276223990","4035251466121744642","4035251441778856855","4035251386774753296","4035251373303304628","4035251344517075331","4035251321000595489","4035251317717308360","4035251285583303110","4035251263755293671","4035251238811046288","4035251206649320120","4035251179046146339","4035251169412879261","4035251122792862005","4035251056695284234","4035251023435370893","4035251023435239821","4035251014705582442","4035250989354554108","4035250951718933069","4035250912478335485","4035250806864253251","4035250806864122179","4035250783787651110","4035250783787782182","4035250767511916725","4035250762736374072","4035250751163634404","4035250682684739646","4035250673040855992","4035250667205727157","4035250667205596085","4035250632776388678","4035250620337132465","4035250608267891326","4035250597870342854","4035250597870211782","4035250597870473926","4035250587599212892","4035250571807003159","4035250564816605874","4035250562329383479","4035250559634936811","4035250559332619142","4035250532575711258","4035250480397652906","4035250477567086724","4035250418346725454","4035250416108278167","4035250409491698315","4035250394135761555","4035250383453918083","4035250308898394505","4035250295021409149","4035250263656993116","4035250242779582514","4035250242779451442","4035250242779320370","4035250243411677234","4035250243411546162","4035250234260689306","4035250224636662104","4035250222155993925","4035250201630773911","4035250201630970519","4035250120245416294","4035250109149384794","4035250108378420135","4035250076084441747","4035250066745233666","4035250059409330206","4035250057534476350","4035250038544241479","4035250001958769068","4035250002756866476","4035249981881028688","4035249942734738431","4035249920719819324","4035249910909079715","4035249901283873069","4035249876897600136","4035249826717667707","4035249820216627316","4035249731976270292","4035249708188995613","4035249683014193184","4035249681856238511","4035249680669774767","4035249681856041903","4035249675348513166","4035249668444033941","4035249655395160653","4035249653200622408","4035249636324315189","4035249635747271458","4035249627914670666","4035249615129514695","4035249597520973891","4035249568448287728","4035249568088036327","4035249559189820222","4035249550353076391","4035249502364340988","4035249502560228092","4035249482512437868","4035249465621844844","4035249449330250376","4035249448013304456","4035249448013435528","4035249444874064840","4035249429206044762","4035249374565142654","4035249335275394047","4035249315714732097","4035249298136142174","4035249290649113545","4035248904737297226","4035248286757851283","4035248178152510035","4035249206966587747","4035249160907821858","4035249096551993479","4035248966655250891","4035249017008919438","4035247967322738940","4035248718707265888","4035248719672545632","4035249017019929434","4035248996807708870","4035249031866389033","4035248966200955903","4035248812199875049","4035248816465875508","4035248817262990076","4035248817263121148","4035248831133488119","4035248735567188109","4035248713720828658","4035247972624143223","4035247972624012151","4035248153049076589","4035248714355807218","4035248618283438879","4035248660003065993","4035248694891745625","4035247797249938283","4035247509601882608","4035248579036942727","4035248575921558218","4035248590388891686","4035248579463910092","4035248513159303839","4035247428594668440","4035248302327566600","4035248401023275797","4035248352228709207","4035248217347821878","4035247502517178707","4035247509852229952","4035248281826070608","4035248304315994990","4035248166017339656","4035248039240897002","4035247061017793243","4035247079014371530","4035247041879249344","4035248103274353479","4035247217321284074","4035247127878865146","4035247452582417139","4035247117716787901","4035247117711413949","4035246436261532242","4035247481477108697","4035246476146480058","4035246533146874105","4035247304084590899","4035246456532341129","4035245991379309071","4035249247796302470","4035249114788761919","4035246912532287800","4035246940209648254","4035246284461085457","4035246744784507812","4035246969044439048","4035246116025897203","4035246163418779941","4035246228907070123","4035247295935516693","4035247373758927558","4035247376463729528","4035247251276402766","4035247293222522958","4035247220374016285","4035247232963088596","4035247316163465758","4035247346169385662","4035247565641126297","4035247658365260137","4035247740915585680","4035247013789340550","4035247793352773760","4035247866262884528","4035248163403043671","4035247099885884217","4035247595768615095","4035248262193648322","4035247806878290484","4035246927872430619","4035247883691856384","4035247923796349534","4035247940143845597","4035247492584608312","4035247522725663377","4035248013935612133","4035248024161456308","4035247933167210924","4035247566731186370","4035247566613876930","4035248093604319445","4035248124678148143","4035246499451277846","4035246615306146629","4035246612219663304","4035245952116626193","4035246685984100555","4035246979959067429","4035246985912160894","4035246998039335100","4035246939322159796","576690521981489464","4035247164594819661","4035246299619234491","4035245770446967008","4035244596585272239","4035245836910170840","4035244473995333971","4035245319443223304","4035245333922812852","4035245081458610784","4035245104252293611","4035245197829771901","4035244645022995003","4035245033105101797","4035245053164622611","4035242831495008273","4035244885562593757","4035244927573922383","4035244934964941106","4035244996428206324","4035244547721630452","4035244709920608654","4035244550876860957","4035244373605323363","4035244049093267561","576654182199497223","4035244365361550131","4035244429569921200","4035243342302843598","4035243539094672124","4035244208126333026","576655507829592873","4035244238580847357","4035243119073399394","4035243656632766819","576652469090161001","576656589200200570","576659092211667954","4035244021997867353","4035243963277742918","4035243497573814458","4035243478496547042","4035243472218264373","4035243377148727958","4035243763930665587","4035243142830789596","4035242527193665633"]
        self.test_tiktok_return_order(platformId=59,platform_rma_code_list=platform_rma_code_list)