from pymongo import MongoClient
import  json
import pandas as pd

# 连接到 MongoDB
client = MongoClient("mongodb://smallrig:smallrig@192.168.133.223:27017/?authMechanism=SCRAM-SHA-1&authSource=smallrig&directConnection=true")
db = client['smallrig']
collection_name_list = ["ALIEXPRESS_INVENTORY_LOG_TABLE_NAME","GET_FBA_FULFILLMENT_CUSTOMER_RETURNS_DATA","GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA","GET_LEDGER_DETAIL_VIEW_DATA","GET_RESERVED_INVENTORY_DATA","LAZADA_INVENTORY_LOG_TABLE_NAME","WINIT_INVENTORY_LOG_TABLE_NAME","amazon_order_struct","chenglian_INVENTORY_LOG_TABLE_NAME","douyin_order_struct","f_amazon_settlement_ziniao","feedbackCollection","jd_manual_order_struct","jd_pop_order_struct","kuaishou_order_struct","lazada_order_struct","leqimall_order_struct","magento_order_struct","pdd_order_struct","qimen_return_confirm_param","return_order_struct","t_aliexpress_order","t_aliexpress_order_address","t_aliexpress_order_address_old","t_aliexpress_order_old","t_allegro_order","t_amazon_order","t_amazon_order_20201103","t_amazon_order_item","t_amazon_order_item_new","t_amazon_order_new","t_amazon_order_report","t_amazon_settlement_reports","t_amazon_storage_age_snapshot_reports","t_bigcommerce_order","t_bigcommerce_order_address","t_bigcommerce_order_address_new","t_bigcommerce_order_item","t_bigcommerce_order_item_new","t_bigcommerce_order_new","t_douyin_order","t_douyin_order_detail","t_douyin_refund","t_ebay_location_1","t_ebay_location_new","t_ebay_order","t_ebay_order_new","t_ebay_return_order","t_eccang_order","t_excel_order","t_iml_refund_order","t_jingdong_manufactory_order","t_jingdong_order","t_ks_order","t_ks_order_fee","t_ks_order_new","t_ks_order_refund","t_lazada_order","t_lazada_order_item","t_lazada_return_order","t_magento_order","t_pdd_order_detail","t_pinshen_refund_order","t_rakuten_order","t_shopee_order","t_shopee_order_details","t_shopee_order_my_income","t_shopee_return_order","t_shopify_order","t_shopify_order_new","t_smallRig_mall_order","t_taobao_order","t_taobao_order_decode_info","t_taobao_return_order","t_tmall_exchange_receive_order","t_tmall_order","t_tmall_order_address_fullinfo","t_tmall_order_decode_info","t_tmall_return_order","t_wx_channel_order_detail","t_wx_channel_order_id","t_yahoo_order","t_youzan_order","t_youzan_order_fee","t_youzan_refund","taobao_order_struct","tmall_order_struct","wdt_order_struct","webLog","wechat_order_struct","youzan_order_struct"]
is_exist = {}
not_exist = []
collection_data = []
for collection_name in collection_name_list:
    collection = db[collection_name]
    # 检查集合是否存在
    if collection_name in db.list_collection_names():
        # 集合存在，查询文档总数
        total_documents = collection.count_documents({})
        # print(f"集合 {collection_name} 存在，文档总数为: {total_documents}")
        is_exist[f"{collection_name}"] = total_documents
        collection_data.append({'Collection Name': collection_name, 'Total Documents': total_documents})
    else:
        collection_data.append({'Collection Name': collection_name, 'Total Documents': "不存在"})
        not_exist.append(collection_name)

print("存在： ",json.dumps(is_exist,indent=2))
print("不存在：",not_exist)

# 创建 DataFrame
df = pd.DataFrame(collection_data)

# 输出到 Excel 文件
excel_file = 'mongodb_collections_data.xlsx'
df.to_excel(excel_file, index=False)
print(f"数据已成功输出到 {excel_file}")

# 关闭连接
client.close()
