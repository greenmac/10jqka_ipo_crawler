import requests


proxyMeta = "http://H8529Z74T50DA54P:9333CB6DFBF464B6@http-pro.abuyun.com:9010";
proxy = {
	"http": proxyMeta,
	"https": proxyMeta,
}

# 第一步
deposit_url = 'https://bizfundprod.alipay.com/allocation/deposit/index.htm'  # 1、点击访问充值页面
order_headers = {
	"origin": "https://excashier.alipay.com",
	"referer": "https://mrchportalweb.alipay.com/user/home.htm#/",
	"user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3554.0 Safari/537.36',
}

post_arr = {
	'url': deposit_url,
	'headers': order_headers,
	'timeout': 10,
}
if proxy:
	post_arr['proxies'] = proxy
	
print(post_arr)
# deposit_result = requests.get(**post_arr)
# print(deposit_result.text)