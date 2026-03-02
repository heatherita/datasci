#!/usr/bin/env python3
import time
from datetime import datetime, timezone

#import praw
#from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
from collector.db import models
from collector.db.database import SessionLocal
from collector.db.models import RedditSubmission

db = SessionLocal()


HEADERS = {"User-Agent": "job-sentiment-study/0.1 by heather"}

def fetch_new(after: str | None = None, limit: int = 100):
    url = f"https://www.reddit.com/r/jobsearchhacks/new.json?limit={limit}"
    if after:
        url += f"&after={after}"
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json()



def ingest(pages: int = 5, sleep_s: float = 1.2):
    # db = SessionLocal()
    try:
        after = None
        for _ in range(pages):
            data = fetch_new(after=after)
            children = data["data"]["children"]
            if not children:
                break

            for c in children:
                p = c["data"]
                reddit_id = p["name"]          # e.g. t3_xxxxx (good unique key)
                created = datetime.fromtimestamp(p["created_utc"], tz=timezone.utc)

                exists = db.query(models.RedditSubmission).filter_by(reddit_id=reddit_id).first()
                if exists:
                    continue

                row = RedditSubmission(
                    reddit_id=reddit_id,
                    subreddit="jobsearchhacks",
                    created_at=created,
                    title=p.get("title").strip() or "",
                    selftext=p.get("selftext").strip() or "",
                    score=int(p.get("score") or 0),
                    num_comments=int(p.get("num_comments") or 0),
                )
                db.add(row)

            db.commit()
            after = data["data"].get("after")
            if not after:
                break
            time.sleep(sleep_s)
    finally:
        db.close()



def insert_db():
    try:
        # do inserts, queries, etc.
        db.commit()
    finally:
        db.close()

def collect_reddit_main(args) -> None:
    print(f"in collect_reddit_main")
    ingest(pages=10)
    # insert_db()

