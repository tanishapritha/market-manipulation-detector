import praw
import datetime
import json
import os
from dotenv import load_dotenv
import time

load_dotenv()

CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = os.getenv("REDDIT_USER_AGENT")

if not all([CLIENT_ID, CLIENT_SECRET, USER_AGENT]):
    raise ValueError("❌ Missing Reddit credentials in .env")

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

# Parameters
ticker = "GME"
start_date = datetime.date(2025, 6, 30)
end_date = datetime.date(2025, 7, 11)

start_ts = int(datetime.datetime.combine(start_date, datetime.time.min).timestamp())
end_ts = int(datetime.datetime.combine(end_date, datetime.time.min).timestamp())

results = []
seen_ids = set()

# Paginate through results using 'before' timestamps
search_window_ts = end_ts
print(f"🔍 Searching backwards from {datetime.datetime.utcfromtimestamp(search_window_ts)}")

while True:
    count_before = len(results)
    for submission in reddit.subreddit("all").search(
        query=ticker,
        sort="new",
        syntax="lucene",
        params={"before": search_window_ts},
        time_filter="all"
    ):
        created_ts = int(submission.created_utc)
        if created_ts < start_ts:
            break  # Done

        if created_ts < search_window_ts:
            search_window_ts = created_ts  # Move window back

        if submission.id in seen_ids:
            continue
        seen_ids.add(submission.id)

        results.append({
            "id": submission.id,
            "time": datetime.datetime.utcfromtimestamp(created_ts).isoformat(),
            "title": submission.title,
            "text": submission.selftext,
            "score": submission.score,
            "num_comments": submission.num_comments,
            "author": str(submission.author)
        })

    if len(results) == count_before:
        break  # No new results, stop

    time.sleep(2)  # Be polite to Reddit

print(f"✅ Fetched {len(results)} posts for {ticker} between {start_date} and {end_date}")

# Save to file
output_dir = "../data/social"
os.makedirs(output_dir, exist_ok=True)
file_path = os.path.join(output_dir, f"reddit_{ticker}.json")

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

print(f"📁 Saved to {file_path}")
