# Scraper for Google Reviews
The scraper takes the maps url like, https://www.google.com/maps/place/The+Breslin/@40.745572,-73.9902777,17z/data=!4m7!3m6!1s0x89c259a61b874f57:0xc5fd887f907ea722!8m2!3d40.745568!4d-73.988089!9m1!1b1 and scrapes the reviews. The review count is sent as a parameter to scroll the reviews section to collect the required number of reviews.

I am using Google Chrome browser in headless mode to load the page and do the scrolling. So, you need to have [Google Chrome web driver](https://chromedriver.chromium.org/downloads) in your path in order to make this scraper work. Make sure you download the version same as your Chrome browser.

I am using [Splinter](https://splinter.readthedocs.io/en/latest/) and [Beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to extract the HTML and parsing the HTML respectively.

