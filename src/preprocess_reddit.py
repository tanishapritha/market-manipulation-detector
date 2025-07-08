import json
import os
import re
import pandas as pd
from html import unescape
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def clean_text(text):
    text = unescape(text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"\$\w+", "", text)
    text = re.sub(r"[^A-Za-z0-9.,!?'\s]", "", text)  # remove odd symbols
    text = re.sub(r"\s+", " ", text).strip()
    return text

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    return analyzer.polarity_scores(text)["compound"]

def preprocess_reddit(filepath, save_to):
    raw_data = load_json(filepath)
    cleaned = []

    for item in raw_data:
        raw_title = item.get("title", "")
        raw_text = item.get("text", "")
        time_str = item.get("time", "")
        
        try:
            time = pd.to_datetime(time_str, utc=True).tz_localize(None).floor("h")
        except Exception as e:
            print(f"[!] Skipping due to bad time: {e}")
            continue

        full_text = clean_text(f"{raw_title}. {raw_text}")
        sentiment = analyze_sentiment(full_text)

        cleaned.append({
            "time": time,
            "content": full_text,
            "sentiment_compound": sentiment
        })

    df = pd.DataFrame(cleaned)
    df.sort_values("time", inplace=True)

    os.makedirs(os.path.dirname(save_to), exist_ok=True)
    df.to_csv(save_to, index=False)
    print(f"[+] Preprocessed {len(df)} Reddit posts → {save_to}")
    print(df.head())

if __name__ == "__main__":
    preprocess_reddit(
        filepath="../data/social/reddit_GME.json",
        save_to="../data/processed/reddit_GME.csv"
    )
