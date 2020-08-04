import datetime
import time
import json
import random
import requests
import os
import pandas as pd
import re
from bs4 import BeautifulSoup


def ANewStockCalendar():
    headers = {
        'Host':'data.10jqka.com.cn',
        'Referer':'http://data.10jqka.com.cn/ipo/xgsgyzq',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3554.0 Safari/537.36',
        'Upgrade-Insecure-Requests':'1',
        'X-Requested-With': 'XMLHttpRequest',
    }

    # A股新股
    new_stocks = []
    for i in range(6):
        url = f'http://data.10jqka.com.cn/ipo/xgsgyzq/board/all/field/SGDATE/page/{i}/order/desc/ajax/1/'
        res = requests.get(url, headers=headers)
        res.encoding = 'GBK'
        soup  = BeautifulSoup(res.text, 'lxml')
        tr_list = soup.select('tbody tr')

        for each_tr in tr_list:
            td_list = each_tr.select('td')
            stock_code_first = td_list[0].text.strip()[0]
            if stock_code_first in ('0', '3'):
                market = 'SZ'
            if stock_code_first in ('6'):
                market = 'SH'
            
            public_price_origin = td_list[7].text.strip().replace('\n', '')
            public_price = re.sub(' +', '~', public_price_origin)
            
            start_year = str(datetime.datetime.now().year)
            
            start_date = str(td_list[10].text.strip()[:5])
            subscription_date_start = start_year + '-' + start_date
            
            dt = datetime.datetime.strptime(subscription_date_start, '%Y-%m-%d')
            subscription_date_end = (dt + datetime.timedelta(days=2)).strftime(
                '%Y-%m-%d') # A股规定 申购日+2day 为 截止日
            
            public_date_origin = str(td_list[14].text.strip())
            public_date = start_year + '-' +public_date_origin
            if public_date_origin == '-':
                public_date = public_date_origin
            
            new_stocks_data = {
                'market': market,
                'stock_code': str(td_list[0].text.strip()),
                'stock_name': str(td_list[1].text.strip()),
                'total_issued': str(td_list[3].text.strip()),
                'public_price': str(public_price),
                'lots_size': '100',
                'currency': 'CNY',
                'subscription_date_start': str(subscription_date_start),
                'subscription_date_end': str(subscription_date_end),
                'public_date': str(public_date),
            }
            new_stocks.append(new_stocks_data)
            
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_stock_list = []
    for new_stock in new_stocks:
        new_stock_list.append(new_stock.values())        
    df = pd.DataFrame(new_stock_list, columns=['市场', '股票代码', '股票名称', '发行总数(万股)', '上市价格', '每手股数', '币种', '申购起始', '申购结束', '上市时间'])
    if not os.path.exists('data/a/'):
        os.makedirs('data/a/')
    df.to_csv(f'data/a/ANewStockCalendar{now_time}.csv', index=False, encoding='utf-8')
    # df.to_excel(f'data/a/ANewStockCalendar{now_time}.xlsx', index=False, encoding='utf-8')

    return new_stocks

def write2excel(new_stocks):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_stock_list = []
    for new_stock in new_stocks:
        new_stock_list.append(new_stock.values())        
    
    df = pd.DataFrame(new_stock_list, columns=['市场', '股票代码', '股票名称', '发行总数(万股)', '上市价格', '每手股数', '币种', '申购起始', '申购结束', '上市时间'])
    if not os.path.exists('data/a/'):
        os.makedirs('data/a/')
    df.to_csv(f'data/a/ANewStockCalendar{now_time}.csv', index=False, encoding='utf-8')
    # df.to_excel(f'data/a/ANewStockCalendar{now_time}.xlsx', index=False, encoding='utf-8')
    return new_stock_list


# ANewStockCalendar = ANewStockCalendar()
# print(HKNewStockCalendar)
# for new_stock in ANewStockCalendar:
#     print(new_stock)

# write2excel = write2excel(ANewStockCalendar)
# print(write2excel)

while True:
    try:
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ANewStockCalendar()
        print('now_time:', now_time)
        time.sleep(5)
    except Exception as e:
        raise e