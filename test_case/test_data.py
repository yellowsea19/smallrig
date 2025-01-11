import requests
#测试
# url = "http://192.168.133.223:15010/init/v1/modifyIncomeV2"
#uat
url = "http://10.245.1.16:15010/init/v1/modifyIncomeV3"
files = {
    'file': open(r'E:\ERP\F1 ERP V6.0.27_20241128\导入确认收入.xlsx', 'rb')
}


response = requests.post(url, files=files)

# 检查请求是否成功
if response.status_code == 200:
    with open(r'E:\ERP\F1 ERP V6.0.27_20241128\error.xls', 'wb') as f:
        f.write(response.content)
    print("文件已成功保存。")
else:
    print(f"请求失败，状态码: {response.status_code}")
