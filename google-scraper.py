from bs4 import BeautifulSoup
from splinter import Browser
import time
import sys
from urllib.parse import unquote
from selenium import webdriver
import json
from proxy import *
import dateparser

def get_html(url, count):
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('--proxy-server=%s' % get_anonymous_proxy())
    browser = Browser("chrome", headless=False)
    browser.visit(url)
    time.sleep(2)
    # sort and select newest for the list
    browser.find_by_text("Sort").first.click()
    time.sleep(2)
    new_menu_item = browser.find_by_id("action-menu").find_by_tag("ul").find_by_tag("li")[1]
    new_menu_item.click()
    time.sleep(7)
    rlen = get_review_count(browser.html)
    while rlen < count:
        #div.section-layout.section-scrollbox.scrollable-y.scrollable-show
        browser.execute_script('document.querySelector("div.section-layout.section-scrollbox").scrollTop = document.querySelector("div.section-layout.section-scrollbox").scrollHeight')
        time.sleep(2)
        rlen = get_review_count(browser.html)
    html = browser.html
    browser.quit()
    return html

def get_review_count(html):
    soup = BeautifulSoup(html, "html5lib")
    reviews = soup.find_all('div', {'data-review-id': True, 'aria-label': True})
    return len(reviews)

def extract_business_name(url):
    tmp = url.split("@")
    name = tmp[0].replace('https://www.google.com/maps/place/','')
    name = unquote(name[:-1]).replace('+', ' ')
    return name

def get_reviews(html):
    soup = BeautifulSoup(html, "html5lib")
    reviews = soup.find_all('div', {'data-review-id': True, 'aria-label': True})

    for r in reviews:   
        user = r['aria-label'].encode('ascii', 'ignore').decode('UTF-8')
        review_id = r['data-review-id']
        content_div = r.find("div", {'data-review-id': review_id})
        stars = content_div.find("span", {'role':'img'})['aria-label'].strip()
        rating = int(stars.split(' ')[0])
        date = content_div.select_one('span[class*="-date"]').text.strip()
        text = content_div.select_one('span[class*="-text"]').text.strip()
        if len(text) == 0:
            continue

        yield {
            "rating": rating,
            "id": review_id,
            "user": user,
            "date": dateparser.parse(date).strftime("%d-%m-%Y"),
            "review": text.replace("\n",'').encode('ascii', 'ignore').decode('UTF-8')
        }

# python3 google-scraper.py <urls.txt> <count>
if len(sys.argv) == 3:
    f = open(sys.argv[1], "r")
    lines = f.readlines()
    f.close()
    for url in lines:
        name = extract_business_name(url)
        print("Processing URL for business: "+name)
        f = open(name.replace(' ',"_").lower()+".json", "w", encoding='utf-8')

        html = get_html(url, int(sys.argv[2]))
        for r in get_reviews(html):
            r['business'] = name
            json.dump(r, f, ensure_ascii=False, indent=4)
        f.close()
else:
    print("Usage: python3 google-scraper.py <urls.txt> <count>")
    exit()