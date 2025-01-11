from faker import Faker
import requests
fake = Faker()

# 生成虚拟IP地址
def get_ip():
    ip_list = []
    for i in range (100):
        ip_address = fake.ipv4()
        ip_list.append(ip_address)
    return ip_list

def get_country(ip_list):
    result = {}
    for ip in ip_list:
        url = f'https://ip100.info/ipaddr?ip={ip}'
        res = requests.get(url)
        res = res.json()['country']
        country_list = ["美国","日本","韩国"]

        if res in country_list:
            result[f'{res}'] = ip
            # print(ip)
            # print(res)
    print(result)
    return result



if __name__ == "__main__":
    ip = get_ip()
    country = get_country(ip)


