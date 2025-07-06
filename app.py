import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIG ---
ticker = "GME"

# --- LOAD DATA ---
features_df = pd.read_csv("data/final/GME_features.csv", parse_dates=["time"])
anomaly_df = pd.read_csv("data/final/GME_with_anomalies.csv", parse_dates=["time"])

# --- TABS SETUP ---
tabs = {
    "Dashboard": "📊 Executive Dashboard",
    "Raw Data": "📂 Raw Data",
    "Processed Features": "🧹 Processed Features",
    "Anomaly Graph": "📈 Anomaly Graph",
    "Model Details": "🧠 Model Details",
    "Output Summary": "📤 Output Summary"
}

# --- SESSION STATE FOR ACTIVE TAB ---
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Dashboard"

# --- SIDEBAR STYLING ---
st.markdown("""
<style>
section[data-testid="stSidebar"] {
    background: #1a1a2f;
    padding-top: 2rem;
}
button.sidebar-tab {
    background-color: transparent;
    border: none;
    color: white;
    text-align: left;
    padding: 0.8rem 1rem;
    width: 100%;
    font-size: 1rem;
    border-radius: 6px;
    cursor: pointer;
    transition: 0.2s ease;
    display: block;
}
button.sidebar-tab:hover {
    background-color: #2d2d44;
}
button.sidebar-tab.selected {
    background-color: #44446b;
    font-weight: 600;
    border-left: 4px solid #5e60ce;
}
h1, h2, h3 {
    color: #222222;
}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAV ---
st.sidebar.markdown(f"<h1 style='color:white;'>📊 Market Anomaly</h1>", unsafe_allow_html=True)
for key, label in tabs.items():
    selected = "selected" if st.session_state.active_tab == key else ""
    if st.sidebar.button(label, key=key, use_container_width=True):
        st.session_state.active_tab = key
    st.markdown(f"""
        <script>
        var b = window.parent.document.querySelector('button[data-testid="{key}"]');
        if (b) {{ b.classList.add("sidebar-tab"); b.classList.add("{selected}"); }}
        </script>
    """, unsafe_allow_html=True)

# ------------------ VIEWS ------------------

# === EXECUTIVE DASHBOARD ===
if st.session_state.active_tab == "Dashboard":
    st.title(f"📊 Executive Dashboard – {ticker}")

    st.markdown("### 📘 What is Market Manipulation?")
    st.info("""
    Market manipulation refers to illegal or unethical practices that artificially influence a stock's price or trading volume.  
    It includes tactics like **pump-and-dump**, **spoofing**, or spreading **false news** to mislead investors and create false demand or panic.
    """)

    st.markdown("### 🧠 How This Model Works")
    st.markdown(f"""
    Our system uses **machine learning** to detect potential signs of manipulation in the `{ticker}` trading data:
    1. **Collects** hourly Open, High, Low, Close, Volume data.
    2. **Creates engineered features** like returns, volume z-score, rolling stats.
    3. **Trains an Isolation Forest model** to learn "normal" vs. "abnormal" behavior.
    4. **Predicts anomalies**: Flags suspicious price or volume patterns.
    5. **Visualizes results** for investigation and alerting.
    """)

    # KPIs
    k1, k2, k3 = st.columns(3)
    k1.metric("Total Rows", len(anomaly_df))
    k2.metric("Anomalies", (anomaly_df["anomaly"] == -1).sum())
    k3.metric("Anomaly %", f"{100 * (anomaly_df['anomaly'] == -1).sum() / len(anomaly_df):.2f}%")

    last_anomaly = anomaly_df[anomaly_df["anomaly"] == -1]["time"].max()
    if pd.notna(last_anomaly):
        st.warning(f"🚨 Last anomaly detected on `{last_anomaly}`")
    else:
        st.success("✅ No anomalies detected in the dataset.")

    st.markdown("### 📈 Price Trend")
    st.line_chart(anomaly_df.set_index("time")["Close"])


# === RAW DATA VIEW ===
elif st.session_state.active_tab == "Raw Data":
    st.title(f"📂 Raw Market Data – {ticker}")
    st.dataframe(features_df[["time", "Close", "High", "Low", "Open", "Volume"]].head(50))

# === PROCESSED FEATURES VIEW ===
elif st.session_state.active_tab == "Processed Features":
    st.title("🧹 Processed Data Summary")
    st.dataframe(features_df.describe())
    st.markdown("**Price Return Distribution:**")
    st.bar_chart(features_df["price_return"])

# === ANOMALY GRAPH ===
elif st.session_state.active_tab == "Anomaly Graph":
    st.title("📈 Anomaly Detection Output")
    fig, ax = plt.subplots(figsize=(12, 6))
    normal = anomaly_df[anomaly_df["anomaly"] == 1]
    outliers = anomaly_df[anomaly_df["anomaly"] == -1]

    ax.plot(anomaly_df["time"], anomaly_df["Close"], label="Close Price", color="gray", alpha=0.5)
    ax.scatter(outliers["time"], outliers["Close"], color="red", label="Anomalies", zorder=5)

    ax.set_title(f"Anomalies in {ticker} Price")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")
    ax.legend()
    st.pyplot(fig)

# === MODEL DETAILS ===
elif st.session_state.active_tab == "Model Details":
    st.title("🧠 Trained Model Insights")
    st.markdown("- **Model**: Isolation Forest")
    st.markdown(f"- Detected **{(anomaly_df['anomaly'] == -1).sum()}** anomalies out of **{len(anomaly_df)}** rows.")
    st.bar_chart(anomaly_df["anomaly"].value_counts())

# === OUTPUT SUMMARY ===
elif st.session_state.active_tab == "Output Summary":
    st.title("📤 Final Output: Anomaly CSV")
    st.dataframe(anomaly_df.tail(20))
    st.download_button("📥 Download CSV", anomaly_df.to_csv(index=False), file_name=f"{ticker}_anomalies.csv")
