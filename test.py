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


url = 'http://www.aastocks.com/sc/stocks/analysis/moneyflow.aspx?symbol=00002&type=l'
# res = requests.get(url, headers=headers, proxies=proxies)
res = requests.get(url)
print(res.text)
# res.encoding = 'GBK'
# soup  = BeautifulSoup(res.text, 'lxml')
