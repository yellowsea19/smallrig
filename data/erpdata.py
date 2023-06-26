job_taobao_data = {
    "title": "【订单拉取】淘宝订单拉取",
    "method": "post",
    "path": "",
    "data": "id=113&executorParam=%7B+%22status%22%3A%22SELLER_CONSIGNED_PART%2CWAIT_SELLER_SEND_GOODS%22%2C%0A+++++%22minuteConfig%22%3A%221440%22+%2C%0A++++%22url%22%3A%22http%3A%2F%2F39.98.37.249%3A3389%2FtaoBao%2Fv2%2Flist%22%0A%7D&addressList="
    }
job_taobao_addr = {
    "title": "【订单拉取】淘宝订单地址拉取",
    "method": "post",
    "path": "",
    "data": "id=312&executorParam=&addressList="
    }


job_taobao_to_mysql = {
    "title": "【订单拉取】淘宝订单地址拉取",
    "method": "post",
    "path": "",
    "data": "id=118&executorParam=&addressList="
    }

job_yicang_data = {
    "title": "【审单】易仓异步审核订单&WMS",
    "method": "post",
    "path": "",
    "data": "id=108&executorParam=&addressList="
    }
job_tmall_data = {
    "title": "【天猫订单拉取】天猫订单列表获取",
    "method": "post",
    "path": "",
    "data": "id=75&executorParam=%7B+%22status%22%3A%22SELLER_CONSIGNED_PART%2CWAIT_SELLER_SEND_GOODS%22%2C%0A+++++%22minuteConfig%22%3A%221440%22+%0A+++%0A%7D&addressList="
    }


job_tmall_addr = {
    "title": "【天猫订单地址】天猫订单地址拉取",
    "method": "post",
    "path": "",
    "data": "id=74&executorParam=&addressList="
    }


job_tmall_to_mysql = {
    "title": "【天猫订单地址】天猫订单地址拉取",
    "method": "post",
    "path": "",
    "data": "id=73&executorParam=&addressList="
    }

job_ks_addr = {
    "title": "【订单拉取】快手订单数据解密",
    "method": "post",
    "path": "",
    "data": "id=310&executorParam=&addressList="
    }

job_ks_data = {
    "title": "【订单拉取】快手订单拉取",
    "method": "post",
    "path": "",
    "data": "id=227&executorParam=%7B%22beginTime%22%3A%222023-05-05+09%3A01%3A20%22%2C%22endTime%22%3A%222023-05-25+20%3A31%3A20%22%7D&addressList="
    }

job_ks_to_mysql = {
    "title": "【订单同步】快手订单同步MySQL",
    "method": "post",
    "path": "",
    "data": "id=228&executorParam=&addressList="
    }


job_douyin_data = {
    "title": "【订单拉取】抖音订单拉取",
    "method": "post",
    "path": "",
    "data": "id=164&executorParam=%7B%22url%22%3A%22https%3A%2F%2Fopenapi-fxg.jinritemai.com%22%2C%22minute%22%3A600%7D&addressList="
    }

job_douyin_addr = {
    "title": "【订单拉取】抖音数据解密",
    "method": "post",
    "path": "",
    "data": "id=165&executorParam=%7B%22url%22%3A%22https%3A%2F%2Fopenapi-fxg.jinritemai.com%22%7D&addressList="
    }

job_douyin_to_mysql = {
    "title": "【抖音】订单同步到数据库",
    "method": "post",
    "path": "",
    "data": "id=167&executorParam=&addressList="
    }

job_jd_data ={
    "title": "【订单拉取】京东订单列表获取",
    "method": "post",
    "path": "",
    "data": "id=58&executorParam=1440&addressList="
    }


job_jd_to_mysql ={
    "title": "【京东订单】京东订单插入MySQL",
    "method": "post",
    "path": "",
    "data": "id=59&executorParam=&addressList="
    }



oms_audit_data = {
    "title": "发货单审核",
    "method": "post",
    "path": "/API/oms/order/v1/audit",
    "data": {"warehouseId":232,"logistics":"SFCRD","hasMagento":"false","showReceiverRegion":"false","expressType":"SFCRD","expressTypeName":"顺丰次日达","ids":[4124527],"timestamp":1685607067000}
    }


SellerSKU_save = {
    "title": "SellerSKU映射关系",
    "method": "post",
    "path": "/API/sku/platform/v1/save",
    "data": {"platformProduct":{"platformCode":"10024082682486","channelId":88,"sonAsin":"","operators":"","channel":"JD-CN-SmallRig影视器材"},"productRelationList":[{"productId":2066,"productCode":"1128","productName":"三脚架固定板","productNum":1}],"timestamp":1685611576000}
    }



update_sellerSkuMatch = {
    "title": "发货单更新SellerSKU",
    "method": "get",
    "path": "/API/oms/order/v1/sellerSkuMatch",
    "data": {"id":4124560}
    }

stockTaking_saveOrUpdate = {
    "title": "创建盘盈盘亏单",
    "method": "post",
    "path": "/API/srm/stockTaking/v1/saveOrUpdate",
    "data": {"id":"","warehouseType":0,"productTotalNum":10000,"productVarietyNum":1,"remark":"","stockType":7,"stockTakingAssignDetailList":[{"productId":2066,"productName":"三脚架固定板","productCode":"1128","stockType":7,"marketId":10,"channelId":88,"marketName":"China-Pro","channelName":"JD-CN-SmallRig影视器材","productNum":10000}],"warehouseId":103,"stockTakingDetailList":[{"productCode":"1128","productId":2066,"productName":"三脚架固定板","productNum":10000,"stockType":7,"waitAignedNum":0}],"timestamp":1685673682000}

    }