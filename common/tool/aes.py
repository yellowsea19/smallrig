#coding=utf8


"""
ECB没有偏移量
"""
# from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


def add_to_16(text):
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')


# 加密函数
def encrypt(text):
    key = 'N6EtqC7hKC8mYIET'.encode('utf-8')
    mode = AES.MODE_ECB
    text = add_to_16(text)
    cryptos = AES.new(key, mode)

    cipher_text = cryptos.encrypt(text)
    return b2a_hex(cipher_text)


# 解密后，去掉补足的空格用strip() 去掉
def decrypt(text):
    key = 'N6EtqC7hKC8mYIET'.encode()
    mode = AES.MODE_ECB
    cryptor = AES.new(key, mode)
    plain_text = cryptor.decrypt(a2b_hex(text))
    print(plain_text)
    return bytes.decode(plain_text)
    # return bytes.decode(plain_text).rstrip('\0')


if __name__ == '__main__':
    e = encrypt('{"createOrderDelverSkuList": [{"count": 1,"skuId": 1493426762476945410,"thirdpartySkuCode": "156848"}],"deliverNo": "1645412451272","deliverTime": "2022-02-21 11:00:51","logisticsCode": "15618","logisticsName": "顺丰快递","logisticsNo": "36009075","orderNo": "220221025515019520","warehouseCode": "1","warehouseName": "2号仓库","weight": 2.0}')  # 加密
    print("加密:", e.decode('utf-8'))
    # c='639cf2ea895a223400211e907caa9e7ae7de96328236cbd2517e7d65414cb38f6141995688592b23e8152528d3df8a6e3d245597d4b73ac8fc7fdb7b50c4fa3302b51e5268105e2b6911be47e3a6e01aa471284b7707a330f4ed6abd47e1c13b9c0dd6069be265b4ec669922adc675584f719aa910fb91b475c6693d3e0098b08f628aab0aa6b5831380c3eb1ba66e2c0fedbadeb129754c1a3e145b7b242ebca69e54094ce6b94c909232d3ce2de6b7e99c7c91508ee4d422e5c336e5758ebc733f510a0b98f0c6f8cd0eb7b21b880c8db041c16dd5ba3109399628ef1a9fddbe991af9d3e54c85cc523fb83c7c964a7f12f65c441fd99908fee4fa01add25b082be339e16988f4f243af9b6260ed6c6fefc4e0009071fae82e41151e70c58876de07e3009a651e0c6f2a6f7b9a60448f4baddaed39ecf50ada576f1e8c16cd26babd93cc4b8c4c8e3d66e26a125768348cecced9c27b79cd83ae3f63bcf1fbd8838d5bfd279f15342472c5fd7b6ad5'
    # print(type(e))
    # print(e)
    print(decrypt(e))
    # print(decrypt(c))
    # print(type(c))
    # print(decrypt(c.encode()))



