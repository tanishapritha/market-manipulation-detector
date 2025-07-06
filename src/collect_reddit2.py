import praw
import datetime
import json
import os

# --- Use your credentials here ---
reddit = praw.Reddit(
    client_id='a7Np-eNbiFgRV97N-CuoRA',
    client_secret='XvQBjdMPI2XATCrH3CggN2vJz5UsgQ',
    user_agent='marketmani script by u/gsharpminoronly'
)

# --- Parameters ---
ticker = "GME"
target_date = datetime.date(2025, 7, 4)

start_ts = int(datetime.datetime(target_date.year, target_date.month, target_date.day).timestamp())
end_ts = int(datetime.datetime(target_date.year, target_date.month, target_date.day + 1).timestamp())

results = []

# Search subreddit "all" for posts containing the ticker
for submission in reddit.subreddit("all").search(ticker, sort="new", limit=200):
    created_ts = int(submission.created_utc)
    if start_ts <= created_ts < end_ts:
        results.append({
            "id": submission.id,
            "time": datetime.datetime.utcfromtimestamp(submission.created_utc).isoformat(),
            "title": submission.title,
            "text": submission.selftext,
            "score": submission.score,
            "num_comments": submission.num_comments,
            "author": str(submission.author)
        })

print(f"✅ Fetched {len(results)} posts for {ticker} on {target_date}")

# Save JSON file
output_dir = "../data/social"
os.makedirs(output_dir, exist_ok=True)
file_path = os.path.join(output_dir, f"reddit_{ticker}.json")

with open(file_path, "w") as f:
    json.dump(results, f, indent=4)

print(f"📁 Saved to {file_path}")
