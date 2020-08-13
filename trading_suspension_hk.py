import datetime
import requests
import time


def HKTradingSuspension():   
    url = 'http://www.dbpower.com.hk/ch/news/news-exotic/?uid=&page=1&action=resume'
    res = requests.get(url)
    print(res.text)


while True:
    HKTradingSuspension()
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(now_time)
    time.sleep(5)