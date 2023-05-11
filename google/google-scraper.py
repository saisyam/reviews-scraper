from bs4 import BeautifulSoup
from splinter import Browser
import time
import sys
import json
import dateparser

def get_business_info(url):
    bname = url.split("/@")[0].split("/")[5].replace('+', ' ')
    business = {}
    business['base_url'] = url
    browser = Browser("chrome", headless=True)
    browser.visit(url)
    time.sleep(5)
    soup = BeautifulSoup(browser.html, "html5lib")
    #img_div = soup.select_one('button[aria-label="Photo of '+bname+'"]')
    #img = img_div.find("img").get("src")
    #business['img'] = img
    addr_button = soup.select_one('button[data-item-id="address"]')
    addr = addr_button['aria-label'].replace("Address: ", "").strip()
    business['address'] = addr
    business_name = soup.select_one('h1[class*="fontHeadlineLarge"]').text.strip()
    business['name'] = business_name
    main_div = soup.select_one("div[role='main']")
    fnt_medium_div = main_div.find_all("div", {"class":"fontBodyMedium"})
    rating = fnt_medium_div[0].find("span", {"aria-hidden":"true"}).text.strip()
    business['rating'] = float(rating)
    total_reviews = soup.select_one('span:-soup-contains("(")').text
    business['review_count'] = int(total_reviews.replace("(", "").replace(")", "").replace(",",""))
    res_type = fnt_medium_div[1].select_one('button').text
    business['type'] = res_type.replace("·","")
    business['source'] = "Google"
    tab_div = soup.select_one("div[role='tablist']")
    tab_buttons = tab_div.find_all("button")
    reviews_button = browser.find_by_text("Reviews").click()
    time.sleep(3)
    business['reviews_url'] = browser.url
    browser.quit()
    return business

def get_html(url, count, bname):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(2)
    driver.find_element_by_xpath("//button[@data-value='Sort']").click()
    time.sleep(2)
    list_div = driver.find_element_by_id("action-menu").find_element_by_xpath("div[@data-index='1']").click()
    scrollable_div = driver.find_element_by_xpath("//div[@aria-label='"+bname+"']/div[@tabindex='-1']")
    for i in range(0,(round(count/5 - 1))):
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', 
                scrollable_div)
        time.sleep(3)
    html = driver.page_source
    driver.quit()
    return html

def get_reviews(html):
    soup = BeautifulSoup(html, "html5lib")
    reviews = soup.find_all('div', {'data-review-id': True, 'aria-label': True})

    for r in reviews:   
        user = r['aria-label'].encode('ascii', 'ignore').decode('UTF-8')
        review_id = r['data-review-id']
        content_div = r.find("div", {'data-review-id': review_id})
        stars = content_div.find("span", {'role':'img'})['aria-label'].strip()
        rating = int(stars.split(' ')[0])
        #date = content_div.select_one('span[class*="-date"]').text.strip()
        text_div = soup.find("div", {'id': review_id})
        text = ""
        if text_div:
            text = text_div.text.strip()
        if len(text) < 30:
            continue
        else:
            if "(Translated by Google)" in text: 
                text = text.replace("(Translated by Google) ", "")
                if "(Original)" in text:
                    idx = text.index("(Original)")
                    text = text[0:idx]

        yield {
            "rating": rating,
            "id": review_id,
            "user": user,
            #"date": dateparser.parse(date).strftime("%d-%m-%Y"),
            "review": text.replace("\n",'').encode('ascii', 'ignore').decode('UTF-8')
        }

# python3 google-scraper.py <urls.txt> <count>
if len(sys.argv) == 2:
    f = open(sys.argv[1], "r")
    lines = f.readlines()
    f.close()
    for l in lines:
        url = l
        business = get_business_info(url)
        business['reviews'] = []
        print("Processing URL for business: "+business['name'])
        f = open(business['name'].replace(' ',"_").lower()+".json", "w", encoding='utf-8')
        html = get_html(business['reviews_url'], business['review_count']/2, business['name'])
        for r in get_reviews(html):
            business['reviews'].append(r)
        json.dump(business, f, ensure_ascii=False, indent=4)
        f.close()
else:
    print("Usage: python3 google-scraper.py <urls.txt>")
    exit()