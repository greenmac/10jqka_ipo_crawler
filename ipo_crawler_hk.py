import time
import json
import random
import requests
import os
import pandas as pd
from bs4 import BeautifulSoup


def HKNewStockCalendar():
    headers = {
        'Host':'data.10jqka.com.cn',
        'Referer':'http://data.10jqka.com.cn/ipo/xgsgyzq',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3554.0 Safari/537.36',
        'Upgrade-Insecure-Requests':'1',
        'X-Requested-With': 'XMLHttpRequest',
    }

    # 港股新股
    new_stocks = []
    for i in range(6):
        url = f'http://data.10jqka.com.cn/ipo/xgsgyzq/board/hkstock/field/end_buy_time/page/{i}/order/desc/ajax/1/'
        res = requests.get(url, headers=headers)
        res.encoding = 'GBK'
        soup  = BeautifulSoup(res.text, 'lxml')
        tr_list = soup.select('tbody tr')

        for each_tr in tr_list:
            td_list = each_tr.select('td')
            new_stocks_data = {
                'market': 'HK',
                'stock_code': str(td_list[0].text.strip()),
                'stock_name': str(td_list[1].text.strip()),
                'total_issued': str(td_list[2].text.strip()),
                'public_price': str(td_list[6].text.strip()),
                'lots_size': str(td_list[7].text.strip()),
                'currency': str(td_list[8].text.strip()),
                'subscription_date_start': str(td_list[9].text.strip()),
                'subscription_date_end': str(td_list[10].text.strip()),
                'public_date': str(td_list[13].text.strip()),
            }
            new_stocks.append(new_stocks_data)
    return new_stocks

def write2excel(new_stocks):
    new_stock_list = []
    for new_stock in new_stocks:
        new_stock_list.append(new_stock.values())        
    
    df = pd.DataFrame(new_stock_list, columns=['市场', '股票代码', '股票名称', '发行总数(万股)', '上市价格', '每手股数', '币种', '申购起始', '申购结束', '上市时间'])
    if not os.path.exists('data/'):
        os.makedirs('data/')
    df.to_csv('data/HKNewStockCalendar.csv', index=False, encoding='utf-8')
    df.to_excel('data/HKNewStockCalendar.xlsx', index=False, encoding='utf-8')
    return new_stock_list


HKNewStockCalendar = HKNewStockCalendar()
# # print(HKNewStockCalendar)
# for new_stock in HKNewStockCalendar:
#     print(new_stock)

write2excel = write2excel(HKNewStockCalendar)
print(write2excel)