import pandas as pd
import os

def preprocess_market_social(ticker="GME", interval_hours=6):
    # --- Paths ---
    market_path = f"../data/market/{ticker}_1h.csv"
    social_path = f"../data/processed/{ticker}_social_agg.csv"
    output_path = f"../data/final/{ticker}_features.csv"

    # --- Load Market Data ---
    market = pd.read_csv(market_path, parse_dates=["Datetime"])
    market.rename(columns={"Datetime": "time"}, inplace=True)
    market["time"] = pd.to_datetime(market["time"], utc=True).dt.tz_localize(None)
    market.sort_values("time", inplace=True)
    market = market[market["time"] >= pd.Timestamp("2025-07-06")]


    # --- Market Features ---
    market["price_return"] = market["Close"].pct_change().fillna(0)
    market["return_3h_mean"] = market["price_return"].rolling(window=3).mean()
    market["return_3h_std"] = market["price_return"].rolling(window=3).std()
    market["volume_mean"] = market["Volume"].rolling(window=24).mean()
    market["volume_std"] = market["Volume"].rolling(window=24).std()
    market["volume_zscore"] = (market["Volume"] - market["volume_mean"]) / market["volume_std"]
    market.drop(columns=["volume_mean", "volume_std"], inplace=True)

    # --- Load Social Data ---
    social = pd.read_csv(social_path, parse_dates=["hour"])
    social.rename(columns={"hour": "bucket_time"}, inplace=True)
    social["bucket_time"] = pd.to_datetime(social["bucket_time"]).dt.tz_localize(None)
    social = social.sort_values("bucket_time")

    # --- Merge (asof backwards) ---
    merged = pd.merge_asof(
        market,
        social,
        left_on="time",
        right_on="bucket_time",
        direction="backward",
        tolerance=pd.Timedelta(f"{interval_hours}h") - pd.Timedelta("1s")
    )

    # Drop bucket_time after merge
    if "bucket_time" in merged.columns:
        merged.drop(columns=["bucket_time"], inplace=True)

    # Fill only non-datetime columns with 0
    for col in merged.select_dtypes(exclude=["datetime64[ns]"]).columns:
        merged[col] = merged[col].fillna(0)

    # Save
    merged.set_index("time", inplace=True)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    merged.to_csv(output_path)
    print(f"[+] Final market + social features saved to {output_path}")

    # --- Sanity ---
    print("[Sanity Check]")
    print("Sorted:", merged.index.is_monotonic_increasing)
    print("Duplicates?:", merged.index.has_duplicates)
    print(merged.head())

    print("[DEBUG] Market time range:", merged.index.min(), "to", merged.index.max())
    print("[DEBUG] Nonzero Reddit:", merged['reddit_message_count'].sum())
    print("[DEBUG] Nonzero Twitter:", merged['twitter_message_count'].sum())
    print("[DEBUG] First nonzero rows:")
    print(merged[(merged["reddit_message_count"] > 0) | (merged["twitter_message_count"] > 0)].head())


if __name__ == "__main__":
    preprocess_market_social(ticker="GME", interval_hours=6)
