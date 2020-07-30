import time
import json
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup


headers = {
    'host':'q.10jqka.com.cn',
    'Referer':'http://q.10jqka.com.cn/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3554.0 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest',
}
url = 'http://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/1/ajax/1/'
res = requests.get(url,headers=headers)
print(res.text)