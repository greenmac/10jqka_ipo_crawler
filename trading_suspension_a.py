import datetime
import requests
import time


def ATradingSuspension():
    url = 'http://data.eastmoney.com/tfpxx/'
    res = requests.get(url)
    print(res.text)


while True:
    ATradingSuspension()
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(now_time)
    time.sleep(5)