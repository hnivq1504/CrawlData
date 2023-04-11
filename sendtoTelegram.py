import feedparser
import json
import requests
import schedule
import time

url = "https://feeds.feedburner.com/TheHackersNews"
bot_token = "6216004222:AAHo7A_DoK5e6sCdfBHp2VpwOn_H-Hg9Og8"
chat_id = "-901299271"

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

    # Send a Telegram message with the new data
    if new_data:
        chunks = split_message(create_message(new_data))
        for chunk in chunks:
            send_telegram_message(chunk)

def create_message(new_data):
    message = "New articles on The Hacker News:\n\n"
    for article in new_data:
        message += f"{article['Title']} ({article['Link']})\n\n"
    return message

def split_message(message):
    max_length = 4096
    if len(message) <= max_length:
        return [message]
    chunks = [message[i:i+max_length] for i in range(0, len(message), max_length)]
    return chunks

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    response = requests.post(url, data=data)
    if not response.ok:
        print("Failed to send message:", response.text)

schedule.every(4).hours.do(crawl_data_thehackernews)

crawl_data_thehackernews()

while True:
    schedule.run_pending()
    time.sleep(1)