import pandas as pd
import os

def preprocess_market_only(ticker="GME"):
    # File paths
    market_path = f"../data/market/{ticker}_1h.csv"
    output_path = f"../data/final/{ticker}_features.csv"

    # Load market data
    market = pd.read_csv(market_path, parse_dates=["Datetime"])

    # Rename column for consistency
    market.rename(columns={"Datetime": "time"}, inplace=True)

    # Fix timezone issues: make tz-naive
    market["time"] = pd.to_datetime(market["time"]).dt.tz_localize(None)

    # Set datetime index and sort
    market.set_index("time", inplace=True)
    market.sort_index(inplace=True)

    # Calculate price return (hourly % change in Close price)
    market["price_return"] = market["Close"].pct_change().fillna(0)

    # Rolling average and std of returns (window = 3 hours)
    market["return_3h_mean"] = market["price_return"].rolling(window=3).mean()
    market["return_3h_std"] = market["price_return"].rolling(window=3).std()

    # Volume Z-Score (window = 24 hours for stability)
    market["volume_mean"] = market["Volume"].rolling(window=24).mean()
    market["volume_std"] = market["Volume"].rolling(window=24).std()
    market["volume_zscore"] = (market["Volume"] - market["volume_mean"]) / market["volume_std"]

    # Drop intermediate columns
    market.drop(columns=["volume_mean", "volume_std"], inplace=True)

    # Save to final CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    market.to_csv(output_path)
    print(f"[+] Final market-only features saved to {output_path}")

    # Optional: Sanity check
    print("[Sanity Check]")
    print("Chronologically sorted:", market.index.is_monotonic_increasing)
    print("Any duplicate timestamps?:", market.index.has_duplicates)
    print(market.head())

if __name__ == "__main__":
    preprocess_market_only(ticker="GME")
