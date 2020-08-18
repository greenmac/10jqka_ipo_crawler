import datetime
import time
import json
import random
import requests
import os
import pandas as pd
import psycopg2
from bs4 import BeautifulSoup


def HKNewStockCalendar(page_nums=5):
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
        'Cookie': 'Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1595991283; __utma=156575163.1303265994.1596075105.1596075105.1596075105.1; __utmc=156575163; __utmz=156575163.1596075105.1.1.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; Hm_lvt_60bad21af9c824a4a0530d5dbf4357ca=1595991283,1596093102,1596093500; Hm_lvt_f79b64788a4e377c608617fba4c736e2=1595991283,1596093102,1596093500; historystock=HK9913; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1597116011; Hm_lpvt_f79b64788a4e377c608617fba4c736e2=1597116011; Hm_lpvt_60bad21af9c824a4a0530d5dbf4357ca=1597116011; v=AuogCJyJQYy2Q817qn_eWe0xPVuPW261YN_iWXSjlj3Ip4RNXOu-xTBvMmVH',
        'Host': 'data.10jqka.com.cn',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    }

    # 港股新股
    new_stocks = []
    for page_num in range(1, page_nums+1):
        url = f'http://data.10jqka.com.cn/ipo/xgsgyzq/board/hkstock/field/end_buy_time/page/{page_num}/order/desc/ajax/1/'
        res = requests.get(url, headers=headers, proxies=proxies)
        res.encoding = 'GBK'
        soup  = BeautifulSoup(res.text, 'lxml')
        tr_list = soup.select('tbody tr')

        for each_tr in tr_list:
            td_list = each_tr.select('td')
            public_price = td_list[6].text.strip().replace('-', '~')
            
            new_stocks_data = {
                'market': 'HK',
                'stock_code': str(td_list[0].text.strip()),
                'stock_name': str(td_list[1].text.strip()),
                'total_issued': str(td_list[2].text.strip()),
                'public_price': str(public_price),
                'lots_size': str(td_list[7].text.strip()),
                'currency': str(td_list[8].text.strip()),
                'subscription_date_start': str(td_list[9].text.strip()),
                'subscription_date_end': str(td_list[10].text.strip()),
                'public_date': str(td_list[13].text.strip()),
            }
            new_stocks.append(new_stocks_data)
            
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H^%M^%S')
    new_stock_list = []
    for new_stock in new_stocks:
        new_stock_list.append(new_stock.values())        
    df = pd.DataFrame(new_stock_list, columns=['市场', '股票代码', '股票名称', '发行总数(万股)', '上市价格', '每手股数', '币种', '申购起始', '申购结束', '上市时间'])
    if not os.path.exists('data/hk/'):
        os.makedirs('data/hk/')
    df.to_csv(f'data/hk/HKNewStockCalendar{now_time}.csv', index=False, encoding='utf-8')
    # df.to_excel(f'data/hk/HKNewStockCalendar{now_time}.xlsx', index=False, encoding='utf-8')

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
        
        insert_sql = f"INSERT INTO ipo_crawler (market, stock_code, stock_name, total_issued, public_price, lots_size, currency, subscription_date_start, subscription_date_end, public_date) VALUES ('{market}', '{stock_code}', '{stock_name}', '{total_issued}', '{public_price}', '{lots_size}', '{currency}', '{subscription_date_start}', '{subscription_date_end}', '{public_date}');"
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
    if not os.path.exists('data/hk/'):
        os.makedirs('data/hk/')
    df.to_csv(f'data/hk/HKNewStockCalendar{now_time}.csv', index=False, encoding='utf-8')
    # df.to_excel(f'data/hk/HKNewStockCalendar{now_time}.xlsx', index=False, encoding='utf-8')
    return new_stock_list


now_time = datetime.datetime.now().strftime('%Y-%m-%d %H^%M^%S')
HKNewStockCalendar = HKNewStockCalendar()
# print(HKNewStockCalendar)
for new_stock in HKNewStockCalendar:
    print(new_stock)
print('now_time:', now_time)

# write2excel = write2excel(HKNewStockCalendar)
# print(write2excel)

# while True:
#     now_time = datetime.datetime.now().strftime('%Y-%m-%d %H^%M^%S')
#     HKNewStockCalendar()
#     print('now_time:', now_time)
#     time.sleep(120)
