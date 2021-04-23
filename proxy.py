import requests
import os

def get_oxy_proxy():
    username = os.environ['RES_USER']
    password = os.environ['OXY_PASS']

    proxy = ('http://customer-%s:%s@pr.oxylabs.io:7777' %(username, password))

    proxies = {
        'http': proxy,
        'https': proxy
    }

    resp = requests.get("https://ipinfo.io", proxies=proxies)
    return resp.json()['ip']