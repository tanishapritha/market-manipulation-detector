import json
import os
import re
import pandas as pd
from html import unescape
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load JSON
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Clean text
def clean_text(text):
    text = unescape(text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"\$\w+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# Sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    return analyzer.polarity_scores(text)

# Main function
def preprocess_reddit(filepath, save_to):
    raw_data = load_json(filepath)
    cleaned = []

    for item in raw_data:
        raw_title = item.get("title", "")
        raw_text = item.get("text", "")
        combined_text = f"{raw_title}. {raw_text}"
        text = clean_text(combined_text)
        sentiment = analyze_sentiment(text)

        cleaned.append({
            "time": pd.to_datetime(item.get("time", ""), errors='coerce'),
            "content": text,
            "sentiment_compound": sentiment["compound"]
        })

    # DataFrame creation
    df = pd.DataFrame(cleaned)
    df.dropna(subset=["time"], inplace=True)
    df["time"] = df["time"].dt.tz_localize(None)
    df.sort_values("time", inplace=True)

    os.makedirs(os.path.dirname(save_to), exist_ok=True)
    df.to_csv(save_to, index=False)
    print(f"[+] Preprocessed {len(df)} Reddit posts → {save_to}")

if __name__ == "__main__":
    preprocess_reddit(
        filepath="../data/social/reddit_GME.json",
        save_to="../data/processed/reddit_GME.csv"
    )
