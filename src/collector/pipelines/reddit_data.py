#!/usr/bin/env python3
import shutil
import subprocess
import sys
import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
from pathlib import Path
from typing import List, Tuple

from collector.db.database import SessionLocal

db = SessionLocal()


def _fail(msg: str, code: int = 2) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)

def collect_reddit_posts_json():

    headers = {"User-Agent": "job-sentiment-study/0.1"}

    url = "https://www.reddit.com/r/jobsearchhacks/new.json?limit=100"
    r = requests.get(url, headers=headers)

    data = r.json()
    print(f"reddit data is {data}")



def collect_reddit_posts_api():
    reddit = praw.Reddit(
        client_id="YOUR_ID",
        client_secret="YOUR_SECRET",
        user_agent="job-sentiment-study"
    )

    analyzer = SentimentIntensityAnalyzer()

    subreddit = reddit.subreddit("jobsearchhacks")

    for post in subreddit.new(limit=500):
        text = (post.title or "") + " " + (post.selftext or "")
        scores = analyzer.polarity_scores(text)

        compound = scores["compound"]

        if compound > 0.05:
            polarity = 1
        elif compound < -0.05:
            polarity = -1
        else:
            polarity = 0



def insert_db():
    try:
        # do inserts, queries, etc.
        db.commit()
    finally:
        db.close()

def collect_reddit_main(args) -> None:
    print(f"in collect_reddit_main")
    # collect_reddit_posts()
    # insert_db()

