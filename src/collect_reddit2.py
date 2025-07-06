import praw
import datetime
import json
import os
from dotenv import load_dotenv

# 🔐 Load credentials from .env
load_dotenv()

CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = os.getenv("REDDIT_USER_AGENT")

if not all([CLIENT_ID, CLIENT_SECRET, USER_AGENT]):
    raise ValueError("❌ Missing Reddit credentials in .env")

# 🤖 Authenticate
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

# --- Parameters ---
ticker = "GME"
target_date = datetime.date(2025, 7, 4)

start_ts = int(datetime.datetime(target_date.year, target_date.month, target_date.day).timestamp())
end_ts = int(datetime.datetime(target_date.year, target_date.month, target_date.day + 1).timestamp())

results = []

# 🔍 Fetch posts
for submission in reddit.subreddit("all").search(ticker, sort="new", limit=200):
    created_ts = int(submission.created_utc)
    if start_ts <= created_ts < end_ts:
        results.append({
            "id": submission.id,
            "time": datetime.datetime.utcfromtimestamp(created_ts).isoformat(),
            "title": submission.title,
            "text": submission.selftext,
            "score": submission.score,
            "num_comments": submission.num_comments,
            "author": str(submission.author)
        })

print(f"✅ Fetched {len(results)} posts for {ticker} on {target_date}")

# 💾 Save to file
output_dir = "../data/social"
os.makedirs(output_dir, exist_ok=True)
file_path = os.path.join(output_dir, f"reddit_{ticker}.json")

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

print(f"📁 Saved to {file_path}")
