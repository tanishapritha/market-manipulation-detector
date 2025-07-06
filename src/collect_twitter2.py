import requests
import json
import os
import re

# 🔐 Bearer Token
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAHSj2wEAAAAAN1c1ptkPDxifGyrn4JH1MtJGVOs%3Do07hqlwAEPFYPUKy366CBvFGpheQUGMuIB1aNFdBfbroo89uRV"

# 📌 Headers for Twitter API
def create_headers():
    return {"Authorization": f"Bearer {BEARER_TOKEN}"}

# 🔍 Twitter API search
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

# 🧠 Smart filter for relevance
def is_relevant_tweet(text, ticker):
    text_lower = text.lower()
    ticker_lower = ticker.lower()

    if ticker_lower not in text_lower and f"${ticker_lower}" not in text_lower:
        return False

    tickers = re.findall(r'\$\w+', text)

    # If too many tickers, keep only if keyword is contextually relevant
    if len(tickers) > 3:
        keywords = [ticker_lower, 'gamestop', 'short squeeze', 'r/gme', 'stock', 'volatility', 'earnings']
        if not any(keyword in text_lower for keyword in keywords):
            return False

    return True

# 💾 Save to social folder
def save_to_json(tweets, ticker):
    os.makedirs("../data/social", exist_ok=True)
    filepath = f"../data/social/twitter_{ticker}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(tweets, f, indent=4, ensure_ascii=False)
    print(f"[+] Saved {len(tweets)} relevant tweets to {filepath}")

# 🚀 Main
if __name__ == "__main__":
    ticker = "GME"
    query = f"{ticker} lang:en -is:retweet"
    raw_tweets = search_tweets(query, max_results=100)

    # Apply relevance filter
    filtered_tweets = [tweet for tweet in raw_tweets if is_relevant_tweet(tweet["text"], ticker)]

    save_to_json(filtered_tweets, ticker)
