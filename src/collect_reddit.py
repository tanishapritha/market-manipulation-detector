import praw
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)


# ----------- SCRAPE POSTS ------------------------
def scrape_reddit(ticker="GME", limit=100):
    posts = []
    subreddit = reddit.subreddit("wallstreetbets")

    for post in subreddit.search(ticker, limit=limit):
        posts.append({
            "id": post.id,
            "time": datetime.utcfromtimestamp(post.created_utc).isoformat(),
            "title": post.title,
            "text": post.selftext,
            "score": post.score,
            "num_comments": post.num_comments,
            "author": str(post.author)
        })

    return posts

# ----------- SAVE AS JSON ------------------------

def save_as_json(data, ticker):
    dir_path = "data/social"
    os.makedirs(dir_path, exist_ok=True)  # Create dir if not exists
    file_path = os.path.join(dir_path, f"reddit_{ticker}.json")

    with open(file_path, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    print(f"[+] Saved {len(data)} posts to {file_path}")


# ----------- RUN THIS SCRIPT ---------------------

if __name__ == "__main__":
    ticker = "GME"
    data = scrape_reddit(ticker)
    save_as_json(data, ticker)
