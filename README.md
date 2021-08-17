# Reviews scraper
This repo contains scrapers to scrape reviews from Google, TripAdvisor etc. You can find the domain specific reviews under the following URLs:

1. [Google](https://github.com/saisyam/reviews-scraper/tree/main/google)
2. Trip Advisor - TBD

I am using Google Chrome browser to load the page and do the scrolling. So, you need to have [Google Chrome web driver](https://chromedriver.chromium.org/downloads) in your path in order to make this scraper work. Make sure you download the version same as your Chrome browser.

I am using [Splinter](https://splinter.readthedocs.io/en/latest/) and [Beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to extract and parsing the HTML respectively.

# Webdriver security issue on MacOS
Mac will throw a security error while running chromedriver. To make the chromedriver binary file `trusted` run the following command:
```shell
$ xattr -d com.apple.quarantine <path to chromedriver>
```