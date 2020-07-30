def proxy_get(num_retries=2):
    PROXY_POOL_API = "http://127.0.0.1:5555/random"
    """
    #代理获取模块
    """
    print('num_retries:', num_retries)
    try:
        print(PROXY_POOL_API)
        r_proxy = requests.get(PROXY_POOL_API, timeout = 5)
        print(r_proxy)
        proxy = r_proxy.text    #指定代理
        print("代理是:", proxy)
        proxies = {
            "http": 'http://' + proxy,
            "https": 'https://' + proxy,
            }
        return proxies
    except:
        if num_retries > 0:
            print("代理获取失败，重新获取")


num_retries = 0
proxy_get(num_retries-1)