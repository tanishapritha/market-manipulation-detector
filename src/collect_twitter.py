import requests
import json
import os

# 🔐 Paste your actual Bearer Token here (keep it secret!)
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAHSj2wEAAAAAN1c1ptkPDxifGyrn4JH1MtJGVOs%3Do07hqlwAEPFYPUKy366CBvFGpheQUGMuIB1aNFdBfbroo89uRV"

# 📌 Create headers for authentication
def create_headers():
    return {"Authorization": f"Bearer {BEARER_TOKEN}"}

# 🔍 Search tweets via Twitter v2 API
def search_tweets(query, max_results=100):
    url = "https://api.twitter.com/2/tweets/search/recent"
    params = {
        "query": query,
        "max_results": max_results,
        "tweet.fields": "id,text,created_at,public_metrics,author_id"
    }

    response = requests.get(url, headers=create_headers(), params=params)

    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")

    return response.json().get("data", [])

# 💾 Save tweets to JSON
def save_to_json(tweets, ticker):
    os.makedirs("data/social", exist_ok=True)
    filepath = f"data/social/twitter_{ticker}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(tweets, f, indent=4, ensure_ascii=False)
    print(f"[+] Saved {len(tweets)} tweets to {filepath}")

# 🚀 Run the script
if __name__ == "__main__":
    ticker = "GME"
    query = f"{ticker} lang:en -is:retweet"  # filter out retweets
    tweets = search_tweets(query, max_results=100)
    save_to_json(tweets, ticker)
