import time
import json
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup

proxies = {"http": "116.231.96.146:8118"}
headers = {
    # 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 'Cookie':'Hm_lvt_60bad21af9c824a4a0530d5dbf4357ca=1595991283; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1595991283; Hm_lvt_f79b64788a4e377c608617fba4c736e2=1595991283; __utma=156575163.1303265994.1596075105.1596075105.1596075105.1; __utmc=156575163; __utmz=156575163.1596075105.1.1.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; Hm_lpvt_f79b64788a4e377c608617fba4c736e2=1596092723; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1596092723; Hm_lpvt_60bad21af9c824a4a0530d5dbf4357ca=1596092723; v=AiTu2ubvJ7XRZFP5nwaObAAm8ykVvUgnCuHcaz5FsO-y6cqfZs0Yt1rxrPeN',
    'Host':'data.10jqka.com.cn',
    'Referer':'http://data.10jqka.com.cn/ipo/xgsgyzq',
    # 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3554.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
url = 'http://data.10jqka.com.cn/ipo/xgsgyzq/board/hkstock/field/end_buy_time/page/1/order/desc/ajax/1/'
# url = 'http://data.10jqka.com.cn/ipo/xgsgyzq/'
# url = 'http://data.10jqka.com.cn'
# res = requests.get(url)
res = requests.get(url, headers=headers)
# res = requests.get(url, headers=headers, proxies=proxies)
# # res.encoding = 'GBK'
# print(res)
# time.sleep(1)
print(res.text)
# time.sleep(1)
# # soup  = BeautifulSoup(res.text, 'lxml')
# # print(soup)

