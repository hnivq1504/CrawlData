import feedparser
import json
import schedule
import time

url = "https://feeds.feedburner.com/TheHackersNews"

def crawl_data_thehackernews():
    # Parse the RSS feed
    feed = feedparser.parse(url)

    # Load existing data from file
    try:
        with open("hacker_news_data.json", "r") as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []

    # Create a list to store the new data
    new_data = []

    # Loop through each article and add its details to the new data list
    for item in feed["items"]:
        article = {
            "Title": item["title"],
            "Published": item["published"],
            "Author": item["author"],
            "Description": item["description"],
            "Link": item["link"] 
        }

        # Check if the article already exists in the existing data
        if article not in existing_data:
            new_data.append(article)

    # Combine the existing and new data and save it in JSON format
    with open("hacker_news_data.json", "w") as outfile:
        json.dump(existing_data + new_data, outfile, indent=6)

schedule.every(4).hours.do(crawl_data_thehackernews)

crawl_data_thehackernews()

while True:
    schedule.run_pending()
    time.sleep(1)
