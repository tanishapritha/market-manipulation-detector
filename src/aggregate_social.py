import pandas as pd
import os
from datetime import datetime

def aggregate_social_features(ticker="GME"):
    reddit_path = f"../data/processed/reddit_{ticker}.csv"
    twitter_path = f"../data/processed/twitter_{ticker}.csv"
    output_path = f"../data/processed/{ticker}_social_agg.csv"

    # Define date range for aggregation
    START = datetime(2025, 7, 1)
    END = datetime(2025, 7, 11)

    # --- Reddit ---
    reddit = pd.read_csv(reddit_path)
    reddit["time"] = pd.to_datetime(reddit["time"], errors="coerce")
    reddit.dropna(subset=["time"], inplace=True)
    reddit["time"] = reddit["time"].dt.tz_localize(None)
    
    # ⏳ Filter Reddit by date
    reddit = reddit[(reddit["time"] >= START) & (reddit["time"] < END)]
    reddit["hour"] = reddit["time"].dt.floor("h")

    reddit_grouped = reddit.groupby("hour").agg({
        "sentiment_compound": "mean",
        "content": "count"
    }).rename(columns={
        "sentiment_compound": "reddit_sentiment_mean",
        "content": "reddit_message_count"
    })

    # --- Twitter ---
    twitter = pd.read_csv(twitter_path)
    twitter["time"] = pd.to_datetime(twitter["time"], errors="coerce")
    twitter.dropna(subset=["time"], inplace=True)
    twitter["time"] = twitter["time"].dt.tz_localize(None)

    # ⏳ Filter Twitter by date
    twitter = twitter[(twitter["time"] >= START) & (twitter["time"] < END)]
    twitter["hour"] = twitter["time"].dt.floor("h")

    twitter_grouped = twitter.groupby("hour").agg({
        "sentiment_compound": "mean",
        "content": "count"
    }).rename(columns={
        "sentiment_compound": "twitter_sentiment_mean",
        "content": "twitter_message_count"
    })

    # --- Combine ---
    combined = pd.concat([reddit_grouped, twitter_grouped], axis=1).fillna(0)

    # --- Save ---
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    combined.to_csv(output_path)
    print(f"[+] Aggregated social data saved to {output_path}")
    print(combined.tail())

if __name__ == "__main__":
    aggregate_social_features()
