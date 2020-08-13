import datetime
import requests
import time
from pyquery import PyQuery as pq


def HKTradingSuspension():   
    url = 'http://www.dbpower.com.hk/ch/news/news-exotic/?uid=&page=1&action=resume'
    res = requests.get(url)
    print(res.text)
    doc = pq(res.text)
    class_docs = doc('.news_hidden')
    
    trading_suspension_lists = []
    for class_doc in class_docs.items():
        trading_suspension = class_doc.text().split(' ')
        trading_suspension_lists.append(trading_suspension)
    # print(trading_suspension_list)
    
    trading_suspension_data_list = []
    for data in trading_suspension_lists:
        market = str('HK')
        stock_code = data[2][1:6]
        stock_name = data[1]
        status = data[3][:2]
        suspension_price = None
        if status == '停牌':
            suspension_price = data[4]
        trading_price = None
        if status == '復牌':
            trading_price = data[4]
        currency = data[5]
        trading_suspension_data = {
            'market': market,
            'stock_code': stock_code,
            'stock_name': stock_name,
            'status': status,
            'suspension_price': suspension_price,
            'trading_price': trading_price,
            'currency': currency,
        }
        trading_suspension_data_list.append(trading_suspension_data)
    
    # print(trading_suspension_data_list)
    # for i in trading_suspension_data_list:
    #     print(i)

HKTradingSuspension()
now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(now_time)


# while True:
#     HKTradingSuspension()
#     now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     print(now_time)
#     time.sleep(5)