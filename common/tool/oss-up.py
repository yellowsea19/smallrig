# -*- coding: utf-8 -*-
import oss2
import os,sys

# 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
auth = oss2.Auth('', '')
# yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
# 填写Bucket名称。
bucket = oss2.Bucket(auth, 'https://oss-cn-shenzhen.aliyuncs.com', 'smallrig-test')



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
            # print(os.path.join(root, d))
            folder_list.append(folder)
    # print(file_list)
    return folder_list,file_list


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
    # is_exist("mall/static/test/tt/dj-2.jpg")

    list_diff=sys.argv[1]
    print(list_diff)
    # for i in list_diff:
    #     bucket.put_object_from_file("mall/static/test/%s"%i, 'D:\\oss-test\\%s'%i)
    # down_dir = '/data/web/mall/static'
    # up_dir = 'mall/static/test'
    # # print(up_dir)
    # folder,file = walkFile(down_dir)
    # for j in folder:
    #
    #     # bucket.put_object(up_dir+'/', '')
    #     j.replace(down_dir,"")
    #     print(j)
    # for i in file :
    #     # 判断文件是否存在
    #     print(i)
        # result = is_exist(up_dir+'/%s'%i)
        # if result :
        #     # 上传文件
        #     bucket.put_object_from_file(up_dir+'/%s'%i, down_dir+'\%s'%i)

    #填写目录名称，目录需以正斜线结尾。
    # bucket.put_object('mall/static/test/aa/bb/', '')
    #
