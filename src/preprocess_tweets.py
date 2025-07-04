import json
import os
import re
import pandas as pd
from html import unescape
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# -------- LOAD JSON --------
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# -------- CLEAN TEXT --------
def clean_text(text):
    text = unescape(text)                             # Convert HTML entities
    text = re.sub(r"http\S+", "", text)               # Remove URLs
    text = re.sub(r"@\w+", "", text)                  # Remove @mentions
    text = re.sub(r"#", "", text)                     # Remove hashtags symbol
    text = re.sub(r"\$\w+", "", text)                 # Remove cashtags
    text = re.sub(r"\s+", " ", text).strip()          # Normalize whitespace
    return text

# -------- SENTIMENT --------
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    return analyzer.polarity_scores(text)

# -------- MAIN FUNCTION --------
def preprocess_tweets(filepath, save_to):
    raw_data = load_json(filepath)
    cleaned = []

    for item in raw_data:
        raw_text = item.get("text", "")
        text = clean_text(raw_text)
        sentiment = analyze_sentiment(text)

        cleaned.append({
            "id": item["id"],
            "time": item["created_at"],
            "username": item.get("author_id", "N/A"),
            "content": text,
            "original": raw_text,
            "likeCount": item["public_metrics"]["like_count"],
            "retweetCount": item["public_metrics"]["retweet_count"],
            "sentiment_neg": sentiment["neg"],
            "sentiment_neu": sentiment["neu"],
            "sentiment_pos": sentiment["pos"],
            "sentiment_compound": sentiment["compound"]
        })

    # Save as CSV
    df = pd.DataFrame(cleaned)
    os.makedirs(os.path.dirname(save_to), exist_ok=True)
    df.to_csv(save_to, index=False)
    print(f"[+] Preprocessed {len(df)} tweets → {save_to}")


# -------- RUN ------------
if __name__ == "__main__":
    ticker = "GME"
    preprocess_tweets(
        filepath=f"data/social/twitter_{ticker}.json",
        save_to=f"data/processed/twitter_{ticker}.csv"
    )
