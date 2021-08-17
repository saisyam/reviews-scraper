# Scraper for Google Reviews
Google scraper extracts business information and reviews for that busiess. The base URL looks like
https://www.google.com/maps/place/Royal+35+Steakhouse/@40.7489998,-73.9856977,17z/data=!3m2!4b1!5s0x89c259a9e791203f:0x8595c59bdb667435!4m5!3m4!1s0x89c259a9e73148ff:0x7d419f214495eeb3!8m2!3d40.7489998!4d-73.9835037. We will scrape the following business information:
* Image of the business
* Name of the business
* Overall rating and review count
* Business type
* Location
Clicking on `reviews` will take the user to the [reviews page](https://www.google.com/maps/place/Royal+35+Steakhouse/@40.7489998,-73.9856924,17z/data=!3m1!5s0x89c259a9e791203f:0x8595c59bdb667435!4m7!3m6!1s0x89c259a9e73148ff:0x7d419f214495eeb3!8m2!3d40.7489998!4d-73.9835037!9m1!1b1). We will sort the reviews by latest. Then we will start scraping the reviews. Google uses dynamic loading of reviews, so we need to scroll down the page to get the new set of reviews. We will scroll till we get the desired count (which is passed as a parameter) and then scrape the content.

# Running the scraper
You need to create `urls.txt` file as shown [here](https://github.com/saisyam/reviews-scraper/blob/main/google/urls.txt). You have pass the file path as parameter to the scraper along with the count of reviews you want to scrape.

```shell
$ python3 google-scraper.py urls.txt 30
```
The above command will scrape 30 reviews from each URL.