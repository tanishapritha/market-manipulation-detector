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
    text = re.sub(r"@\w+", "", text)                  # Remove mentions
    text = re.sub(r"\$\w+", "", text)                 # Remove cashtags
    text = re.sub(r"\s+", " ", text).strip()          # Normalize whitespace
    return text

# -------- SENTIMENT --------
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    return analyzer.polarity_scores(text)

# -------- MAIN FUNCTION --------
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
            "id": item.get("id", ""),
            "time": item.get("time", ""),
            "author": item.get("author", ""),
            "title": raw_title,
            "content": text,
            "original": combined_text,
            "score": item.get("score", 0),
            "num_comments": item.get("num_comments", 0),
            "sentiment_neg": sentiment["neg"],
            "sentiment_neu": sentiment["neu"],
            "sentiment_pos": sentiment["pos"],
            "sentiment_compound": sentiment["compound"]
        })

    # Save as CSV
    df = pd.DataFrame(cleaned)
    os.makedirs(os.path.dirname(save_to), exist_ok=True)
    df.to_csv(save_to, index=False)
    print(f"[+] Preprocessed {len(df)} Reddit posts → {save_to}")


# -------- RUN ------------
if __name__ == "__main__":
    ticker = "GME"
    preprocess_reddit(
        filepath=f"data/social/reddit_{ticker}.json",
        save_to=f"data/processed/reddit_{ticker}.csv"
    )
