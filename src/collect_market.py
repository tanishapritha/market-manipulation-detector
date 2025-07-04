# src/collect_market.py

import yfinance as yf
import os
import pandas as pd

def collect_market_data(ticker="GME", start="2025-06-01", end="2025-07-01", interval="1h"):
    # Fetch hourly data
    data = yf.download(ticker, start=start, end=end, interval=interval)

    # Reset index to make 'Datetime' a column
    data.reset_index(inplace=True)

    # Save
    dir_path = "data/market"
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, f"{ticker}_{interval}.csv")
    data.to_csv(file_path, index=False)

    print(f"[+] Saved market data to {file_path}")
    return data

if __name__ == "__main__":
    collect_market_data(ticker="GME", start="2025-06-01", end="2025-07-01", interval="1h")
