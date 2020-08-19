import datetime
import os
import pandas as pd
import psycopg2
import re
import requests
import time
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq


def ATradingSuspension():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    }

    url = 'http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?cb=datatable1756876&type=FD&sty=SRB&st=0&sr=-1&mkt=1&fd=2020-08-19&p=1&pageNo=1&ps=50&js=(%7Bpages%3A(pc)%2Cdata%3A%5B(x)%5D%7D)&_=1597825800397'
    resp = requests.get(url, headers=headers) 
    doc = pq(resp.text)
    doc = pq(url)
    print(doc)
    # tbody = doc('.table-model')
    # print(tbody)
    
    
    
    # general_list = doc('.general')
    # dd_data_list = []
    # dt_data_list = []
    # for general in general_list.items():
    #     dl_title = general.children('.dl_title').text()
    #     dt_list = general.children('dt')
    #     dd_list = general.children('dd')
            
    #     for dd in dd_list.items():
    #         dd = dd.filter('dd').filter('dd').text()
            
    #         market = str('HK')
    #         stock_code = re.findall(r'\[+[0-9]+\]', dd)[0][1:6]
    #         stock_name = dd.split('] ')[1].split(' [')[0]
    #         sus_trad_status = dd.split('] ')[2][:2]
    #         suspension_price = dd.split(' ')[-2] if sus_trad_status == '停牌' else None
    #         trading_price = dd.split(' ')[-2] if sus_trad_status == '復牌' else None
    #         currency = dd.split(' ')[-1]
            
    #         dd_data = {
    #             'market': market,
    #             'stock_code': stock_code,
    #             'stock_name': stock_name,
    #             'sus_trad_status': sus_trad_status,
    #             'suspension_price': suspension_price,
    #             'trading_price': trading_price,
    #             'currency': currency,
    #         }
    #         dd_data_list.append(dd_data)    
            
    #     for dt in dt_list.items():
    #         dt = dt.filter('dt').text()
    #         public_time = dl_title + ' ' + dt
    #         dt_data = {
    #             'public_time': public_time,
    #         }
    #         dt_data_list.append(dt_data)

    # dt_dd_data_list = map(list, zip(dd_data_list, dt_data_list))

    # dt_dd_dict_list = []
    # for dt_dd_data in dt_dd_data_list:
    #     dd = dt_dd_data[0]
    #     dt = dt_dd_data[1]
    #     market = dt_dd_data[0]['market']
    #     stock_code = dt_dd_data[0]['stock_code']
    #     stock_name = dt_dd_data[0]['stock_name']
    #     sus_trad_status = dt_dd_data[0]['sus_trad_status']
    #     suspension_price = dt_dd_data[0]['suspension_price']
    #     trading_price = dt_dd_data[0]['trading_price']
    #     currency = str('HKD')
    #     public_time = dt_dd_data[1]['public_time']
    #     suspension_date_start = public_time if sus_trad_status == '停牌' else None
    #     trading_date_start = public_time if sus_trad_status == '復牌' else None
    #     suspension_reason = '停牌重要公告' if sus_trad_status == '停牌' else '復牌重要公告'
        
    #     dt_dd_dict = {
    #         'market': market,
    #         'stock_code': stock_code,
    #         'stock_name': stock_name,
    #         'sus_trad_status': sus_trad_status,
    #         'suspension_price': suspension_price,
    #         'trading_price': trading_price,
    #         'currency': currency,
    #         'suspension_date_start': suspension_date_start,
    #         'trading_date_start': trading_date_start,
    #         'suspension_reason': suspension_reason,
    #     }
    #     dt_dd_dict_list.append(dt_dd_dict)
            
    # now_time = datetime.datetime.now().strftime('%Y-%m-%d %H^%M^%S')
    # dt_dd_list = []
    # for dt_dd_dict in dt_dd_dict_list:
    #     dt_dd_list.append(dt_dd_dict.values())        
    # df = pd.DataFrame(dt_dd_list, columns=['股票市场', '股票代码', '股票名称', '停复牌状态', '停牌价格', '复牌价格', '币种', '停牌開始', '复牌開始', '停盘原因'])
    # if not os.path.exists('data/hk/'):
    #     os.makedirs('data/hk/')
    # df.to_csv(f'data/hk/HKStockEvent{now_time}.csv', index=False, encoding='utf-8')
    # # df.to_excel(f'data/hk/HKStockEvent{now_time}.xlsx', index=False, encoding='utf-8')

    # database = 'ipo_crawler'
    # user = 'postgres'
    # password = '@Futeng2466'
    # host = '127.0.0.1'
    # port ='5432'

    # conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    # cur = conn.cursor()
    
    # for dt_dd_dict in dt_dd_dict_list:
    #     market = dt_dd_dict['market']
    #     stock_code = dt_dd_dict['stock_code']
    #     stock_name = dt_dd_dict['stock_name']
    #     sus_trad_status = dt_dd_dict['sus_trad_status']
    #     suspension_price = dt_dd_dict['suspension_price']
    #     trading_price = dt_dd_dict['trading_price']
    #     currency = dt_dd_dict['currency']
    #     suspension_date_start = dt_dd_dict['suspension_date_start']
    #     trading_date_start = dt_dd_dict['trading_date_start']
    #     suspension_reason = dt_dd_dict['suspension_reason']
        
    #     insert_sql = f"INSERT INTO stock_event (market, stock_code, stock_name, sus_trad_status, suspension_price, trading_price, currency, suspension_date_start, trading_date_start, suspension_reason) VALUES ('{market}', '{stock_code}', '{stock_name}', '{sus_trad_status}', '{suspension_price}', '{trading_price}', '{currency}', '{suspension_date_start}', '{trading_date_start}', '{suspension_reason}');"
    #     cur.execute(insert_sql)
    # conn.commit()
    # conn.close()

    # return dt_dd_dict_list
    
ATradingSuspension()
# ATradingSuspension = ATradingSuspension()
# for ATS in ATradingSuspension:
#     print(ATS)
now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print('now_time:', now_time)


# while True:
#     ATradingSuspension()
#     now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     print(now_time)
#     time.sleep(5)