import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()


import pandas as pd

import json
from datetime import datetime
import snscrape.modules.twitter as sntwitter



# ----------- SCRAPE TWEETS FUNCTION --------------
def scrape_twitter(ticker="GME", since="2025-06-01", until="2025-07-01", max_tweets=100):
    query = f"{ticker} since:{since} until:{until}"
    tweets = []

    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= max_tweets:
            break

        tweets.append({
            "id": tweet.id,
            "time": tweet.date.strftime('%Y-%m-%dT%H:%M:%S'),
            "username": tweet.user.username,
            "content": tweet.content,
            "likeCount": tweet.likeCount,
            "retweetCount": tweet.retweetCount
        })

    return tweets

# ----------- SAVE AS JSON FUNCTION ----------------
def save_as_json(data, ticker):
    dir_path = "data/social"
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, f"twitter_{ticker}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)  # ✅ preserve emoji and UTF-8 chars

    print(f"[+] Saved {len(data)} tweets to {file_path}")


# ----------- RUN THIS SCRIPT ----------------------
if __name__ == "__main__":
    ticker = "GME"
    tweets = scrape_twitter(ticker=ticker, since="2025-06-01", until="2025-07-01", max_tweets=200)
    save_as_json(tweets, ticker)
