import datetime
import psycopg2
import re
import requests
import time
from pyquery import PyQuery as pq


def HKTradingSuspension():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    }

    url = 'http://www.dbpower.com.hk/ch/news/news-exotic/?uid=&page=1&action=resume'
    resp = requests.get(url, headers=headers)
    doc = pq(resp.text)
    
    dd_data_list = []
    dt_data_list = []
    general_list = doc('.general')
    for general in general_list.items():
        dl_title = general.children('.dl_title').text()
        dt_list = general.children('dt')
        dd_list = general.children('dd')
            
        for dd in dd_list.items():
            dd = dd.filter('dd').filter('dd').text()
            
            market = str('HK')
            stock_code = re.findall(r'\[+[0-9]+\]', dd)[0][1:6]
            stock_name = dd.split('] ')[1].split(' [')[0]
            sus_trad_status = dd.split('] ')[2][:2]
            suspension_price = dd.split(' ')[-2] if sus_trad_status == '停牌' else None
            trading_price = dd.split(' ')[-2] if sus_trad_status == '復牌' else None
            currency = dd.split(' ')[-1]
            
            dd_data = {
                'market': market,
                'stock_code': stock_code,
                'stock_name': stock_name,
                'sus_trad_status': sus_trad_status,
                'suspension_price': suspension_price,
                'trading_price': trading_price,
                'currency': currency,
            }
            dd_data_list.append(dd_data)    
            
        for dt in dt_list.items():
            dt = dt.filter('dt').text()
            public_time = dl_title + ' ' + dt
            dt_data = {
                'public_time': public_time,
            }
            dt_data_list.append(dt_data)

    dt_dd_data_list = map(list, zip(dd_data_list, dt_data_list))

    dt_dd_dict_list = []
    for dt_dd_data in dt_dd_data_list:
        dd = dt_dd_data[0]
        dt = dt_dd_data[1]
        market = dt_dd_data[0]['market']
        stock_code = dt_dd_data[0]['stock_code']
        stock_name = dt_dd_data[0]['stock_name']
        sus_trad_status = dt_dd_data[0]['sus_trad_status']
        suspension_price = dt_dd_data[0]['suspension_price']
        trading_price = dt_dd_data[0]['trading_price']
        currency = dt_dd_data[0]['currency']
        public_time = dt_dd_data[1]['public_time']
        suspension_date_start = public_time if sus_trad_status == '停牌' else None
        trading_date_start = public_time if sus_trad_status == '復牌' else None
        suspension_reason = '停牌重要公告' if sus_trad_status == '停牌' else '復牌重要公告'
        
        dt_dd_dict = {
            'market': market,
            'stock_code': stock_code,
            'stock_name': stock_name,
            'sus_trad_status': sus_trad_status,
            'suspension_price': suspension_price,
            'trading_price': trading_price,
            'currency': currency,
            'suspension_date_start': suspension_date_start,
            'trading_date_start': trading_date_start,
            'suspension_reason': suspension_reason,
        }
        dt_dd_dict_list.append(dt_dd_dict)
    
    database = 'ipo_crawler'
    user = 'postgres'
    password = '@Futeng2466'
    host = '127.0.0.1'
    port ='5432'

    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cur = conn.cursor()
    
    for dt_dd_dict in dt_dd_dict_list:
        market = dt_dd_dict['market']
        stock_code = dt_dd_dict['stock_code']
        stock_name = dt_dd_dict['stock_name']
        sus_trad_status = dt_dd_dict['sus_trad_status']
        suspension_price = dt_dd_dict['suspension_price']
        trading_price = dt_dd_dict['trading_price']
        currency = dt_dd_dict['currency']
        suspension_date_start = dt_dd_dict['suspension_date_start']
        trading_date_start = dt_dd_dict['trading_date_start']
        suspension_reason = dt_dd_dict['suspension_reason']
        
        insert_sql = f"INSERT INTO stock_event (market, stock_code, stock_name, sus_trad_status, suspension_price, trading_price, currency, suspension_date_start, trading_date_start, suspension_reason) VALUES ('{market}', '{stock_code}', '{stock_name}', '{sus_trad_status}', '{suspension_price}', '{trading_price}', '{currency}', '{suspension_date_start}', '{trading_date_start}', '{suspension_reason}');"
        cur.execute(insert_sql)
    conn.commit()
    conn.close()

    return dt_dd_dict_list
    

HKTradingSuspension = HKTradingSuspension()
for HKTS in HKTradingSuspension:
    print(HKTS)
now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print('now_time:', now_time)


# while True:
#     HKTradingSuspension()
#     now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     print('now_time:', now_time)
#     time.sleep(5)