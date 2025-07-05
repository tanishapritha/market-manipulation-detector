import os
import json
import praw
from datetime import datetime

# ----------- SETUP PRAW -----------
reddit = praw.Reddit(
    client_id="wFn4u-HKw_1Jw3uIBsvsQg",
    client_secret="JDRJXBfHMUEa9QriYGi0K1WueM2T5g",
    user_agent="MarketManipDetector"
)

# ----------- COLLECT POSTS -----------

def collect_reddit(ticker="GME"):
    subreddits = [
        "wallstreetbets", "stocks", "investing",
        "StockMarket", "options", "pennystocks"
    ]
    query = f"${ticker}"
    all_posts = []

    for sub in subreddits:
        subreddit = reddit.subreddit(sub)
        posts = subreddit.search(query, limit=200, sort="new")

        for post in posts:
            if not post.stickied and (post.selftext or post.title):
                all_posts.append({
                    "id": post.id,
                    "time": datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%dT%H:%M:%S'),
                    "author": str(post.author),
                    "title": post.title,
                    "text": post.selftext,
                    "score": post.score,
                    "num_comments": post.num_comments
                })

    # Save to JSON
    output_dir = "../data/social"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"reddit_{ticker}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(all_posts, f, indent=4)

    print(f"[+] Collected {len(all_posts)} posts → {file_path}")


# ----------- RUN -------------
if __name__ == "__main__":
    collect_reddit(ticker="GME")
