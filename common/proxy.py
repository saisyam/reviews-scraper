import requests
import os
from useragent import *
from bs4 import BeautifulSoup
import random

proxies = []
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

def get_anonymous_proxy():
    if len(proxies) == 0:
        headers = {'User-Agent':get_useragent()}
        r = requests.get('https://free-proxy-list.net/anonymous-proxy.html', headers=headers)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html5lib")
            table = soup.find("table", {'id':'proxylisttable'})
            rows = table.find('tbody').find_all('tr')
            for r in rows:
                tds = r.find_all('td')
                proxies.append(tds[0].get_text()+":"+tds[1].get_text())
    return proxies[random.randint(0, len(proxies))]