import datetime
import time
import json
import random
import requests
import os
import pandas as pd
import psycopg2
import re
from bs4 import BeautifulSoup


def ANewStockCalendar(page_nums=5):
    proxyMeta = "http://H8529Z74T50DA54P:9333CB6DFBF464B6@http-pro.abuyun.com:9010";
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }

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

    # A股新股
    new_stocks = []
    for page_num in range(page_nums+1):
        url = f'http://data.10jqka.com.cn/ipo/xgsgyzq/board/all/field/SGDATE/page/{page_num}/order/desc/ajax/1/'
        res = requests.get(url, headers=headers, proxies=proxies)
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
            public_date = start_year + '-' + public_date_origin
            if public_date_origin == '-':
                public_date = public_date_origin
            
            new_stocks_data = {
                'market': market,
                'stock_code': str(td_list[0].text.strip()),
                'stock_name': str(td_list[1].text.strip()),
                'total_issued': str(td_list[3].text.strip()),
                'public_price': str(public_price),
                'lots_size': '100',
                'currency': '人民币',
                'subscription_date_start': str(subscription_date_start),
                'subscription_date_end': str(subscription_date_end),
                'public_date': str(public_date),
            }
            new_stocks.append(new_stocks_data)
            
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H^%M^%S')
    new_stock_list = []
    for new_stock in new_stocks:
        new_stock_list.append(new_stock.values())        
    df = pd.DataFrame(new_stock_list, columns=['市场', '股票代码', '股票名称', '发行总数(万股)', '上市价格', '每手股数', '币种', '申购起始', '申购结束', '上市时间'])
    if not os.path.exists('data/a/'):
        os.makedirs('data/a/')
    df.to_csv(f'data/a/ANewStockCalendar{now_time}.csv', index=False, encoding='utf-8')
    # df.to_excel(f'data/a/ANewStockCalendar{now_time}.xlsx', index=False, encoding='utf-8')

    database = 'ipo_crawler'
    user = 'postgres'
    password = '@Futeng2466'
    host = '127.0.0.1'
    port ='5432'

    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cur = conn.cursor()
    
    for new_stock in new_stocks:
        market = new_stock['market']
        stock_code = new_stock['stock_code']
        stock_name = new_stock['stock_name']
        total_issued = new_stock['total_issued']
        public_price = new_stock['public_price']
        lots_size = new_stock['lots_size']
        currency = new_stock['currency']
        subscription_date_start = new_stock['subscription_date_start']
        subscription_date_end = new_stock['subscription_date_end']
        public_date = new_stock['public_date']
        
        insert_sql = f"INSERT INTO ipocrawler (market, stock_code, stock_name, total_issued, public_price, lots_size, currency, subscription_date_start, subscription_date_end, public_date) VALUES ('{market}', '{stock_code}', '{stock_name}', '{total_issued}', '{public_price}', '{lots_size}', '{currency}', '{subscription_date_start}', '{subscription_date_end}', '{public_date}');"
        cur.execute(insert_sql)
    conn.commit()
    conn.close()
    
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
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H^%M^%S')
    ANewStockCalendar()
    print('now_time:', now_time)
    time.sleep(120)