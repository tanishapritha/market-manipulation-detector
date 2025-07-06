import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

def train_anomaly_model(ticker="GME"):
    df = pd.read_csv(f"../data/final/{ticker}_features.csv", parse_dates=["time"])
    features = ["price_return", "reddit_mentions", "reddit_sent", "twitter_mentions", "twitter_sent"]

    # Fill missing or extreme values
    X = df[features].fillna(0).clip(-10, 10)

    # Train Isolation Forest
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    model.fit(X)

    # Save model
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, f"models/isolation_forest_{ticker}.joblib")
    print(f"[+] Model saved to models/isolation_forest_{ticker}.joblib")

if __name__ == "__main__":
    train_anomaly_model("GME")
