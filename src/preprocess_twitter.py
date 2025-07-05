import json
import pandas as pd
from datetime import datetime
import os

def preprocess_twitter(ticker="GME"):
    input_path = f"../data/social/twitter_{ticker}.json"
    output_path = f"../data/processed/twitter_{ticker}.csv"

    # Load tweets
    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)

    rows = []
    for tweet in data:
        # Parse timestamp
        time_str = tweet.get("created_at")
        try:
            time = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
        except:
            continue

        # Get content
        content = tweet.get("text", "")

        # Append only if content and time are valid
        if content and time:
            rows.append({"time": time, "content": content})

    df = pd.DataFrame(rows)

    # Save processed CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[+] Preprocessed {len(df)} Twitter posts → {output_path}")

    # Optional preview
    print(df.head())

if __name__ == "__main__":
    preprocess_twitter()
