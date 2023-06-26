# -*- coding: utf-8 -*-
import oss2
import os,sys

# 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
auth = oss2.Auth('LTAI5tNKh1StWRSV88vivH8L', '71Tx8OKTK0yYoHbs5etOuuKhBo7raI')
# yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
# 填写Bucket名称。
bucket = oss2.Bucket(auth, 'https://oss-cn-shenzhen.aliyuncs.com', 'smallrig-test')



# 获取命令行参数，如果没有提供文件路径则退出
if len(sys.argv) < 2:
    print("Usage: python read_file.py <file-path>")
    sys.exit()

# 获取文件路径并打开文件，读取每一行并输出到控制台
file_path = sys.argv[1]
with open(file_path, 'r') as f:
    # 遍历每一行并输出
    for line in f:
        # 输出当前行，并去掉行末的换行符
        a=line.strip()
        bucket.put_object_from_file("mall/static/test/%s" %a, 'D:\\oss-test\\%s' %a)