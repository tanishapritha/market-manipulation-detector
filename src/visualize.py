import pandas as pd
import matplotlib.pyplot as plt
import os

def visualize_anomalies(ticker="GME"):
    input_path = f"../data/final/{ticker}_with_anomalies.csv"
    df = pd.read_csv(input_path, parse_dates=["time"])
    df.set_index("time", inplace=True)

    # Plot price
    plt.figure(figsize=(14, 6))
    plt.plot(df.index, df["Close"], label="Close Price", color="blue")

    # Overlay anomalies
    anomalies = df[df["anomaly"] == -1]
    plt.scatter(anomalies.index, anomalies["Close"], color="red", label="Anomaly", marker="x")

    plt.title(f"{ticker} Price with Detected Anomalies")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()
    plt.tight_layout()

    # Save
    os.makedirs("../plots", exist_ok=True)
    plt.savefig(f"../plots/{ticker}_anomalies.png")
    print(f"[+] Saved plot to ../plots/{ticker}_anomalies.png")

if __name__ == "__main__":
    visualize_anomalies()
