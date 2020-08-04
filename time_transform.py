import datetime
import json
import requests
import time


'''
# sting add 2 days
start_year = str(datetime.datetime.now().year)
start_date = '11-12'
subscription_date_start = start_year + '-' + start_date

dt = datetime.datetime.strptime(subscription_date_start, "%Y-%m-%d")
subscription_date_end = (dt + datetime.timedelta(days=2)).strftime("%Y-%m-%d")

print(subscription_date_end)
'''

# now time format
def now_time():
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return now_time

while True:
    print(now_time())
    time.sleep(5)