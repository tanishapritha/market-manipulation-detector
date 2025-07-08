import json
import pandas as pd
from datetime import datetime
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def preprocess_twitter(ticker="GME"):
    input_path = f"../data/social/twitter_{ticker}.json"
    output_path = f"../data/processed/twitter_{ticker}.csv"

    # Load tweets
    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)

    rows = []
    for tweet in data:
        time_str = tweet.get("created_at")
        try:
            # Parse with UTC awareness, then convert to naive + floor to hour
            time = pd.to_datetime(time_str, utc=True).tz_localize(None).floor("h")
        except Exception as e:
            print(f"[!] Skipped tweet due to time parse error: {e}")
            continue

        content = tweet.get("text", "")

        if content:
            rows.append({"time": time, "content": content})

    df = pd.DataFrame(rows)

    # Add sentiment
    analyzer = SentimentIntensityAnalyzer()
    df["sentiment_compound"] = df["content"].astype(str).apply(
        lambda x: analyzer.polarity_scores(x)["compound"]
    )

    # Save CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[+] Preprocessed {len(df)} Twitter posts → {output_path}")
    print(df.head())

if __name__ == "__main__":
    preprocess_twitter()
