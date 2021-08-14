from bs4 import BeautifulSoup
from splinter import Browser
import time
import sys
import json
import dateparser

def get_business_info(url):
    business = {}
    business['base_url'] = url
    browser = Browser("chrome", headless=False)
    browser.visit(url)
    time.sleep(5)
    soup = BeautifulSoup(browser.html, "html5lib")
    img_div = soup.select_one('div[class*="section-hero-header-image-hero-container"]')
    img = img_div.find("img").get("src")
    business['img'] = img
    addr_button = soup.select_one('button[data-item-id="address"]')
    addr = addr_button['aria-label'].replace("Address: ", "").strip()
    business['address'] = addr
    business_name = soup.select_one('h1[class*="header-title-title"]').text.strip()
    business['name'] = business_name
    rating = soup.find("ol", {"class":"section-star-array"})['aria-label'].replace("stars", "").strip()
    business['rating'] = float(rating)
    total_reviews = soup.select_one('button:-soup-contains("reviews")').text
    business['review_count'] = int(total_reviews.replace("reviews", "").strip().replace(",","")) 
    res_type = soup.select_one('div[class="gm2-body-2"]').text
    business['type'] = res_type.replace("·","")
    business['source'] = "Google"
    reviews_button = browser.find_by_text(total_reviews).click()
    time.sleep(3)
    business['reviews_url'] = browser.url
    browser.quit()
    return business

def get_html(url, count):
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
            "date": dateparser.parse(date).strftime("%d-%m-%Y"),
            "review": text.replace("\n",'').encode('ascii', 'ignore').decode('UTF-8')
        }

# python3 google-scraper.py <urls.txt> <count>
if len(sys.argv) == 3:
    f = open(sys.argv[1], "r")
    lines = f.readlines()
    f.close()
    for url in lines:
        business = get_business_info(url)
        business['reviews'] = []
        print("Processing URL for business: "+business['name'])
        f = open(business['name'].replace(' ',"_").lower()+".json", "w", encoding='utf-8')
        html = get_html(business['reviews_url'], int(sys.argv[2]))
        for r in get_reviews(html):
            business['reviews'].append(r)
        json.dump(business, f, ensure_ascii=False, indent=4)
        f.close()
else:
    print("Usage: python3 google-scraper.py <urls.txt> <count>")
    exit()