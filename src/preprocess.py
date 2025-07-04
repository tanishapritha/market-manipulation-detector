import pandas as pd
import os

def preprocess_all(ticker="GME"):
    # File paths
    reddit_path = f"data/processed/reddit_{ticker}.csv"
    twitter_path = f"data/processed/twitter_{ticker}.csv"
    market_path = f"data/market/{ticker}_1h.csv"
    output_path = f"data/final/{ticker}_features.csv"

    # Load data
    reddit = pd.read_csv(reddit_path, parse_dates=["time"])
    twitter = pd.read_csv(twitter_path, parse_dates=["time"])
    market = pd.read_csv(market_path, parse_dates=["Datetime"])

    # Rename and set datetime index
    market.rename(columns={"Datetime": "time"}, inplace=True)
    reddit.set_index("time", inplace=True)
    twitter.set_index("time", inplace=True)
    market.set_index("time", inplace=True)

    # ⚠️ Strip timezone info from index (important fix)
    reddit.index = reddit.index.tz_localize(None)
    twitter.index = twitter.index.tz_localize(None)
    market.index = market.index.tz_localize(None)

    # Resample Reddit data to hourly
    reddit_hourly = reddit.resample("1h").agg({
        "sentiment_compound": "mean",
        "content": "count"
    }).rename(columns={
        "sentiment_compound": "reddit_sent",
        "content": "reddit_mentions"
    })

    # Resample Twitter data to hourly
    twitter_hourly = twitter.resample("1h").agg({
        "sentiment_compound": "mean",
        "content": "count"
    }).rename(columns={
        "sentiment_compound": "twitter_sent",
        "content": "twitter_mentions"
    })

    # Merge datasets
    merged = market.join([reddit_hourly, twitter_hourly], how="left").fillna(0)

    # Add price return feature
    merged["price_return"] = merged["Close"].pct_change().fillna(0)

    # Save to final CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    merged.to_csv(output_path)
    print(f"[+] Final merged features saved to {output_path}")

    # Optional preview
    print(merged.head())

if __name__ == "__main__":
    preprocess_all(ticker="GME")
