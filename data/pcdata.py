from common.base.handle_yaml import HandleYaml
from common.tool.tool import CommonUtil
import importlib,sys,time
importlib.reload(sys)


login = {
    "title": "PC登录",
    "method": "post",
    "path": "/api/memberLogin/login",
    "data":{"account":"yellowsea2057@gmail.com","passwd":"a123456","verifyCode":""}
    }


submitOrder = {
    "title": "下单",
    "method": "post",
    "path": "/api/order/submitOrder",
    # "data":{"distributionType":0,"payWay":1,"creditCard":{"receivingName":"FDSA","receivingSurname":"FDSA","receivingAddressOne":"南山区","receivingAddressTwo":"波顿18F","receivingCity":"FDSA","receivingCountry":"ANGOLA","receivingPhone":"+244 15656","receivingProvince":"116515","continentId":"","postalCode":"518000","countryId":"6"},"submitOrderSkus":[{"img":"https://stand-dev.s3.amazonaws.com/public/1653983061298_.jpg","title":"2202b 2202B","sku":"2202B","url":"cc02b.html","skuSpecInfo":[],"num":2,"skuId":"1531542220769976321","money":"12300"}],"orderActualMoney":0,"receivingSurname":"FDSA","receivingName":"FDSA","receivingAddressOne":"南山区","receivingAddressTwo":"波顿18F","receivingCity":"FDSA","receivingCountry":"ANGOLA","receivingPhone":"+244 15656","receivingProvince":"116515","continentId":"","countryId":"6","memberRemark":"","deductBalance":2597000,"deductPoints":100,"couponCodes":[],"postalCode":"518000","noSubmit":False}
    # "data":{"checkGift":True,"distributionType":0,"payWay":1,"creditCard":{"receivingName":"sea","receivingSurname":"yellow","receivingAddressOne":"南山区","receivingAddressTwo":"波顿18F","receivingCity":"深圳","receivingCountry":"ALBANIA","receivingPhone":"+355 13546155","receivingProvince":"165165","continentId":"","postalCode":"518000","countryId":"2"},"submitOrderSkus":[{"num":1,"orderSkuType":0,"skuId":"1508759569618771970"}],"orderActualMoney":"0","receivingSurname":"yellow","receivingName":"sea","receivingAddressOne":"南山区","receivingAddressTwo":"波顿18F","receivingCity":"深圳","receivingCountry":"ALBANIA","receivingPhone":"+355 13546155","receivingProvince":"165165","continentId":"","countryId":"2","memberRemark":"","deductBalance":1344000,"deductPoints":0,"couponCodes":[],"postalCode":"518000","noSubmit":False,"checkCart":True,}
    "data":{"creditCard":{"continentId":"","countryId":"2","postalCode":"518000","receivingAddressOne":"南山区888","receivingAddressTwo":"波顿18F","houseNumber":"door777","companyName":"company666","receivingCity":"深圳","receivingCountry":"ALBANIA","receivingName":"sea","receivingPhone":"+355 13444444444","receivingProvince":"广东","receivingSurname":"yellow"},"email":"","checkCart":"false","noSubmit":"true","couponCodes":[],"deductBalance":0,"deductPoints":0,"distributionType":0,"memberRemark":"","submitOrderSkus":[{"num":1,"skuId":"1601165937875152897"}],"vatNumber":"","continentId":"","countryId":"2","postalCode":"518000","houseNumber":"door777","companyName":"company666","receivingAddressOne":"南山区888","receivingAddressTwo":"波顿18F","receivingCity":"深圳","receivingCountry":"ALBANIA","receivingName":"sea","receivingPhone":"+355 13444444444","receivingProvince":"广东","receivingSurname":"yellow"}
    }

lottery_memberLottery = {
    "title": "抽奖",
    "method": "post",
    "path": "/api/lottery/memberLottery",
    # "data":{"distributionType":0,"payWay":1,"creditCard":{"receivingName":"FDSA","receivingSurname":"FDSA","receivingAddressOne":"南山区","receivingAddressTwo":"波顿18F","receivingCity":"FDSA","receivingCountry":"ANGOLA","receivingPhone":"+244 15656","receivingProvince":"116515","continentId":"","postalCode":"518000","countryId":"6"},"submitOrderSkus":[{"img":"https://stand-dev.s3.amazonaws.com/public/1653983061298_.jpg","title":"2202b 2202B","sku":"2202B","url":"cc02b.html","skuSpecInfo":[],"num":2,"skuId":"1531542220769976321","money":"12300"}],"orderActualMoney":0,"receivingSurname":"FDSA","receivingName":"FDSA","receivingAddressOne":"南山区","receivingAddressTwo":"波顿18F","receivingCity":"FDSA","receivingCountry":"ANGOLA","receivingPhone":"+244 15656","receivingProvince":"116515","continentId":"","countryId":"6","memberRemark":"","deductBalance":2597000,"deductPoints":100,"couponCodes":[],"postalCode":"518000","noSubmit":False}
    "data":{"lotteryId": 0,"usePoints": "false"}
    }

lottery_getLotteryMembers = {
    "title": "查询抽奖用户信息",
    "method": "post",
    "path": "/api/lottery/getLotteryMembers",
    # "data":{"distributionType":0,"payWay":1,"creditCard":{"receivingName":"FDSA","receivingSurname":"FDSA","receivingAddressOne":"南山区","receivingAddressTwo":"波顿18F","receivingCity":"FDSA","receivingCountry":"ANGOLA","receivingPhone":"+244 15656","receivingProvince":"116515","continentId":"","postalCode":"518000","countryId":"6"},"submitOrderSkus":[{"img":"https://stand-dev.s3.amazonaws.com/public/1653983061298_.jpg","title":"2202b 2202B","sku":"2202B","url":"cc02b.html","skuSpecInfo":[],"num":2,"skuId":"1531542220769976321","money":"12300"}],"orderActualMoney":0,"receivingSurname":"FDSA","receivingName":"FDSA","receivingAddressOne":"南山区","receivingAddressTwo":"波顿18F","receivingCity":"FDSA","receivingCountry":"ANGOLA","receivingPhone":"+244 15656","receivingProvince":"116515","continentId":"","countryId":"6","memberRemark":"","deductBalance":2597000,"deductPoints":100,"couponCodes":[],"postalCode":"518000","noSubmit":False}
    "data":{"lotteryId": 0}
    }

lottery_buyLotteryNum={
    "title": "查询抽奖用户信息",
    "method": "post",
    "path": "/api/lottery/buyLotteryNum",
    # "data":{"distributionType":0,"payWay":1,"creditCard":{"receivingName":"FDSA","receivingSurname":"FDSA","receivingAddressOne":"南山区","receivingAddressTwo":"波顿18F","receivingCity":"FDSA","receivingCountry":"ANGOLA","receivingPhone":"+244 15656","receivingProvince":"116515","continentId":"","postalCode":"518000","countryId":"6"},"submitOrderSkus":[{"img":"https://stand-dev.s3.amazonaws.com/public/1653983061298_.jpg","title":"2202b 2202B","sku":"2202B","url":"cc02b.html","skuSpecInfo":[],"num":2,"skuId":"1531542220769976321","money":"12300"}],"orderActualMoney":0,"receivingSurname":"FDSA","receivingName":"FDSA","receivingAddressOne":"南山区","receivingAddressTwo":"波顿18F","receivingCity":"FDSA","receivingCountry":"ANGOLA","receivingPhone":"+244 15656","receivingProvince":"116515","continentId":"","countryId":"6","memberRemark":"","deductBalance":2597000,"deductPoints":100,"couponCodes":[],"postalCode":"518000","noSubmit":False}
    "data":{"lotteryId": 0}
    }

memberLogin_register={
    "title": "PC注册",
    "method": "post",
    "path": "/api/memberLogin/register",
    "data":{"account":"314221719@qq.com","passwd":"a123456","subscribe":1,"inviteCode":"U76BBI"}
    }

joinShoppingCart={
    "title": "PC注册",
    "method": "post",
    "path": "/api/productShoppingCart/joinShoppingCart",
    "data":{"goodsList":[{"type":0,"typeInfo":{"type":0,"typeObject":{}},"quantity":1,"skuId":"1601165937875152897"}],"verifyStock":"true"}
    }

createQuestion={
    "title": "PC你问我答",
    "method": "post",
    "path": "/api/questionsAnswers/createQuestion",
    "data":{"detail":"Where do you ship from?(api  auto3)","picList":[],"productCode":"3667","productImages":"https://stand-prod.s3.amazonaws.com/public/1648532809099_3667-1.JPG","productName":"SmallRig Full Cage for Sony Alpha 7R V / Alpha 7 IV / Alpha 7S III / Alpha 1 / Alpha 7R IV 3667","productId":"1508683346969829376"}
    }
search={
    "title": "搜索",
    "method": "post",
    "path": "/api/search",
    "data":{"port":0,"account":"","filterFieldIdList":[],"browser":"Chrome","browserId":"2e168edba80989a2","siteCode":"en_US","sort":1,"pageNum":1,"keyWord":"3667","itemIdList":[]}
    }