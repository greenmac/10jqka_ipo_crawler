import datetime
import time
import json
import random
import requests
import os
import pandas as pd
from bs4 import BeautifulSoup


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1595991283; __utma=156575163.1303265994.1596075105.1596075105.1596075105.1; __utmc=156575163; __utmz=156575163.1596075105.1.1.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; Hm_lvt_60bad21af9c824a4a0530d5dbf4357ca=1595991283,1596093102,1596093500; Hm_lvt_f79b64788a4e377c608617fba4c736e2=1595991283,1596093102,1596093500; historystock=HK9913; Hm_lpvt_60bad21af9c824a4a0530d5dbf4357ca=1596594795; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1596594795; Hm_lpvt_f79b64788a4e377c608617fba4c736e2=1596594795; v=Av40TFDtLYCif3mnwhuCxXmdSR9DP8K5VAN2nagHasE8S5AJEM8SySSTxqF7',    
    'Host': 'data.10jqka.com.cn',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3554.0 Safari/537.36',
}

url = 'http://data.10jqka.com.cn/ipo/xgsgyzq/board/all/field/SGDATE/page/1/order/desc/ajax/1/'
res = requests.get(url, headers=headers)
print(res.text)