import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
features_df = pd.read_csv("data/final/GME_features.csv", parse_dates=["time"])
anomaly_df = pd.read_csv("data/final/GME_with_anomalies.csv", parse_dates=["time"])

# Tab Options
tabs = {
    "Raw Data": "📂 Raw Data",
    "Processed Features": "🧹 Processed Features",
    "Anomaly Graph": "📈 Anomaly Graph",
    "Model Details": "🧠 Model Details",
    "Output Summary": "📤 Output Summary"
}

# Session state for navigation
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Raw Data"

# --- Custom CSS ---
st.markdown("""
<style>
/* Sidebar background */
section[data-testid="stSidebar"] {
    background: #1a1a2f;
    padding-top: 2rem;
}

/* Sidebar buttons as tabs */
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

# --- Sidebar Tabs ---
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

# ----------------- VIEWS ------------------------

if st.session_state.active_tab == "Raw Data":
    st.title("🗂️ Raw Market Data")
    st.dataframe(features_df[["time", "Close", "High", "Low", "Open", "Volume"]].head(50))

elif st.session_state.active_tab == "Processed Features":
    st.title("🧹 Processed Data Summary")
    st.dataframe(features_df.describe())
    st.markdown("**Price Return Distribution:**")
    st.bar_chart(features_df["price_return"])

elif st.session_state.active_tab == "Anomaly Graph":
    st.title("📈 Anomaly Detection Output")
    fig, ax = plt.subplots(figsize=(12, 6))
    normal = anomaly_df[anomaly_df["anomaly"] == 1]
    outliers = anomaly_df[anomaly_df["anomaly"] == -1]

    ax.plot(anomaly_df["time"], anomaly_df["Close"], label="Close Price", color="gray", alpha=0.5)
    ax.scatter(outliers["time"], outliers["Close"], color="red", label="Anomalies")

    ax.set_title("Anomaly Detection on GME")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")
    ax.legend()
    st.pyplot(fig)

elif st.session_state.active_tab == "Model Details":
    st.title("🧠 Trained Model Insights")
    st.markdown("- Model: **Isolation Forest**")
    st.markdown(f"- Detected **{sum(anomaly_df['anomaly'] == -1)}** anomalies out of **{len(anomaly_df)}** rows.")
    st.bar_chart(anomaly_df["anomaly"].value_counts())

elif st.session_state.active_tab == "Output Summary":
    st.title("📤 Final Output: Anomaly CSV")
    st.dataframe(anomaly_df.tail(20))
    st.download_button("📥 Download CSV", anomaly_df.to_csv(index=False), file_name="GME_anomalies.csv")
