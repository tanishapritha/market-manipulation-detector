import pandas as pd
import joblib
import os

def detect_anomalies(ticker="GME"):
    # Paths
    model_path = f"../models/isolation_forest.joblib"
    data_path = f"../data/final/{ticker}_features.csv"
    output_path = f"../data/final/{ticker}_with_anomalies.csv"

    # Load model
    model = joblib.load(model_path)
    print("[+] Model loaded.")

    # Load data
    df = pd.read_csv(data_path, parse_dates=["time"])
    df.set_index("time", inplace=True)
    print(f"[+] Loaded {len(df)} rows from {data_path}")

    # ❗ Use only the features the model was trained on
    features = ['price_return', 'return_3h_mean', 'return_3h_std', 'volume_zscore']

    # Predict anomalies
    df["anomaly"] = model.predict(df[features])

    # Save with anomaly column
    df.to_csv(output_path)
    print(f"[+] Anomaly results saved to {output_path}")
    print(df["anomaly"].value_counts())

if __name__ == "__main__":
    detect_anomalies()
