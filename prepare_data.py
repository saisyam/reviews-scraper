import os
import glob
import json
import csv

folder_path = "/Users/saisyam/work/reviews_data"

json_files = glob.glob(os.path.join(folder_path, "*.json"))
reviews = []

for f in json_files:
    with open(f, 'r') as file:
        json_data = json.load(file)
        restaurant = json_data['name']
        type = json_data['type']
        for review in json_data['reviews']:
            data = {
                "review": review['review'],
                "rating": review['rating'],
                "restaurant": restaurant,
                "type": type
            }
            reviews.append(data)

with open('reviews.csv', 'w', newline='') as csvfile:
    fieldnames = ['review', 'rating', 'restaurant', 'type']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for review in reviews:
        writer.writerow(review)
print(len(reviews))