from bs4 import BeautifulSoup
from splinter import Browser
import time

url = "https://www.google.com/maps/place/The+Breslin/@40.745572,-73.9902777,17z/data=!4m7!3m6!1s0x89c259a61b874f57:0xc5fd887f907ea722!8m2!3d40.745568!4d-73.988089!9m1!1b1"


def get_html(url, count):
    browser = Browser("chrome", headless=True)
    browser.visit(url)
    time.sleep(2)
    rlen = get_review_count(browser.html)
    while rlen < count:
        browser.execute_script('document.querySelector("div.section-layout.section-scrollbox.scrollable-y.scrollable-show").scrollTop = document.querySelector("div.section-layout.section-scrollbox.scrollable-y.scrollable-show").scrollHeight')
        time.sleep(2)
        rlen = get_review_count(browser.html)
    html = browser.html
    browser.quit()
    return html

def get_review_count(html):
    soup = BeautifulSoup(html, "html5lib")
    section_div = soup.find('div',{'class':'section-layout'})
    reviews = section_div.find_all('div', {'class':'section-review'})
    return len(reviews)

def get_reviews(html):
    soup = BeautifulSoup(html, "html5lib")
    section_div = soup.find('div',{'class':'section-layout'})
    reviews = section_div.find_all('div', {'class':'section-review'})
    for r in reviews:
        rsection = r.find_all('div', {'class':'section-review-line'})
        stars = rsection[1].find('span', {'class':'section-review-stars'})['aria-label'].strip()
        review_text = rsection[1].find('div',{'class':'section-review-review-content'}).find('span',{'class':'section-review-text'}).get_text().strip()
        rating = int(stars.split(' ')[0])
        yield {
            "rating": rating,
            "review": review_text.replace("\n",'')
        }

html = get_html(url, 25)
for r in get_reviews(html):
    print(r)