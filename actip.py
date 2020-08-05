import requests
from bs4 import BeautifulSoup
# from selenium import webdriver
import pandas as pd
import re


IPPool = []
for i in range(1,6):
    # 用迴圈逐一打開分頁
    url = f'http://free-proxy.cz/zh/proxylist/country/US/https/ping/all/{i}'
    # print(f'Dealing with {url}')
    
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    tr_list = soup.select('tbody tr')
    
    for each_tr in tr_list:
        td_list = each_tr.select('td')
        print(td_list[0].text)
    
    
    # for j in soup.select('tbody tr'):
    #     # 用正則表達式抓取IP
    #     if re.findall(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', str(j)):
    #         IP = re.findall(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', str(j))[0]
    #         Port = re.findall(r'class="fport" style="">(.*?)</span>', str(j))
    #         print('IP:',IP, 'Port:',Port)
#             IPPool.append(pd.DataFrame([{'IP':IP, 'Port':Port}]))
#     print('There are {} IPs in Pool'.format(len(IPPool)))
# IPPool = pd.concat(IPPool, ignore_index=True)
# print(IPPool)