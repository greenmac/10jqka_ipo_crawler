from pyquery import PyQuery as pq
from lxml import etree


url = 'http://data.10jqka.com.cn/ipo/xgsgyzq/board/hkstock/field/end_buy_time/page/1/order/desc/ajax/1/'
# doc = pq(url=url,encoding='utf-8')
doc = pq(etree.fromstring(url))

# print(doc('title'))
