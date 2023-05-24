import requests , json
import re
# url='http://freetyst.nf.migu.cn/public/product9th/product46/2023/01/1323/2023%E5%B9%B401%E6%9C%8813%E6%97%A518%E7%82%B931%E5%88%86%E5%86%85%E5%AE%B9%E5%87%86%E5%85%A5%E6%97%B6%E4%BB%A3%E5%B3%B0%E5%B3%BB2%E9%A6%96115227/%E6%A0%87%E6%B8%85%E9%AB%98%E6%B8%85/MP3_128_16_Stero/69906200085235212.mp3?channelid=02&msisdn=c4d5c9a5-6978-41cc-9fa0-98ac94093d07&Tim=1673686851276&Key=90a406a90678390a'
# res=requests.get(url=url)
# content=res.content
# with open(r'D:/sougouImg/abc.mp3' , 'wb') as f:
#     f.write(content)
# f.close()






#
#
# post_code=""
# url = "https://www.nowmsg.com/findzip/uk_post_code.asp?CityName=PO14+1qh"
# headers = {
#     "accept-encoding": "gzip, deflate, br"
# }
# res = requests.get(url = url,headers = headers,verify = False)
# # print(res.encoding)
# res.encoding = res.apparent_encoding
# res=res.text
#
# ru='<tr><td >PO14 1QH</td><td >(.*?)</td>'
# result = re.findall(ru,res)
# print(result)





# 遍历文件夹
def walkFile(file):
    file_list = []
    folder_list=[]
    for root, dirs, files in os.walk(file):
        # root 表示当前访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件

        for f in files:
            filename=os.path.join(root, f)
            # print(os.path.join(root, f))
            file_list.append(filename)

        # 遍历所有的文件夹
        for d in dirs:
            folder = os.path.join(root, d)
            print(os.path.join(root, d))
            folder_list.append(folder)

    print(file_list)
    return folder_list,file_list


# -*- coding: utf-8 -*-
import oss2
import os
# 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
auth = oss2.Auth('LTAI5tNKh1StWRSV88vivH8L', '71Tx8OKTK0yYoHbs5etOuuKhBo7raI')
# yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
# 填写Bucket名称。
bucket = oss2.Bucket(auth, 'https://oss-cn-shenzhen.aliyuncs.com', 'smallrig-test')

# 必须以二进制的方式打开文件。
# 填写本地文件的完整路径。如果未指定本地路径，则默认从示例程序所属项目对应本地路径中上传文件。
# with open('D:\\oss-test\\dj-1.jpg', 'rb') as fileobj:
#     # Seek方法用于指定从第1000个字节位置开始读写。上传时会从您指定的第1000个字节位置开始上传，直到文件结束。
#     # fileobj.seek(1000, os.SEEK_SET)
#     # Tell方法用于返回当前位置。
#     # current = fileobj.tell()
#     # 填写Object完整路径。Object完整路径中不能包含Bucket名称。
#     bucket.put_object('mall/static/', fileobj)

def is_exist(filename):
    # 填写Object的完整路径，Object完整路径中不能包含Bucket名称。
    exist = bucket.object_exists(filename)
    # 返回值为true表示文件存在，false表示文件不存在。
    if exist:
        print('object exist')
        return True
    else:
        print('object not exist')
        return False









if __name__ == '__main__':
    # is_exist("mall/static/about")
    down_dir = 'D:\\oss-test-1'
    up_dir = 'mall/static/test'
    folder,file = walkFile(down_dir)
    for j in folder:
        bucket.put_object(up_dir+'/', '')
    for i in file :
        # 判断文件是否存在
        result = is_exist(up_dir+'/%s'%i)
        # if result :
        #     # 上传文件
        #     bucket.put_object_from_file(up_dir+'/%s'%i, down_dir+'\\%s'%i)

    # #填写目录名称，目录需以正斜线结尾。
    # bucket.put_object('mall/static/test/', '')
    #
