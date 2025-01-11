import requests
import json
def make_request():
    url = 'https://www.amazon.de/hz/reviews-render/ajax/reviews/get/ref=cm_cr_arp_d_paging_btm_next_2'

    headers = {
        'authority': 'www.amazon.de',
        'accept': 'text/html,*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'text/plain',
        'cookie': 'session-id=259-5687688-5757026; ubid-acbde=258-2488282-7798632; x-amz-captcha-1=1691991885150093; x-amz-captcha-2=YIhheSUMg878j/ccDDMmKg==; sst-acbde=Sst1|PQGg95jF4M3AjcFMqasne-vdBwWRbVW-e-Di1Y82j_3_Q5Uexx0YwmTigy-LFSTjVhbq35P2xCjlGfNkOGBVahfHW3FH5tniwROFG8MAzzr3tJ10Ha-065hOOCg8uVmD0ssvhsErvYo0uHYsYbavdXnLoq1c8VshdR_lBdzShbBzKPNkfxv_Ph4YEZchjgm1BihSVFtaAmdfgXuvfUWOn9VYX9aSzw9DSrecyc7efsEoewQlRGWkh_ayW-Ua_uUZdZL5; session-id-time=2082787201l; i18n-prefs=EUR; lc-acbde=de_DE; sp-cdn="L5Z9:HK"; session-token=...',
        'device-memory': '8',
        'downlink': '8.45',
        'dpr': '1',
        'ect': '4g',
        'origin': 'https://www.amazon.de',
        'referer': 'https://www.amazon.de/HIYATO-Atmungsaktive-Sportsocken-Baumwolle-Laufsocken/product-reviews/B0BMWNXFFR/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews',
        'rtt': '250',
        'sec-ch-device-memory': '8',
        'sec-ch-dpr': '1',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-ch-viewport-width': '1920',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'viewport-width': '1920',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = "sortBy=&reviewerType=all_reviews&formatType=&mediaType=&filterByStar=&filterByAge=&pageNumber=2&filterByLanguage=&filterByKeyword=&shouldAppend=undefined&deviceType=desktop&canShowIntHeader=undefined&reftag=cm_cr_arp_d_paging_btm_next_2&pageSize=10&asin=B0BMWNXFFR&scope=reviewsAjax0"

    response = requests.post(url, headers=headers, data=data)

    print(response.status_code)
    print(response.text)

make_request()