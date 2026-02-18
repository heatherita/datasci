#!/usr/bin/env python3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collector.db.database import SessionLocal
from collector.db.models import RedditSubmission, RedditSubmissionSentiment

db = SessionLocal()
analyzer = SentimentIntensityAnalyzer()

HEADERS = {"User-Agent": "job-sentiment-study/0.1 by heather"}



def score_sentiment():
    try:
        posts = db.query(RedditSubmission).all()

        for post in posts:

            text = (post.title or "") + " " + (post.selftext or "")
            scores = analyzer.polarity_scores(text)

            compound = scores["compound"]

            if compound > 0.05:
                polarity = 1
            elif compound < -0.05:
                polarity = -1
            else:
                polarity = 0

            row = RedditSubmissionSentiment(
                reddit_id=post.reddit_id,
                sentiment_score=compound,
                polarity=polarity,
                submission_id=post.id
            )
            db.add(row)

        db.commit()
    finally:
        db.close()


def score_reddit_main(args) -> None:
    print(f"in score_reddit_main")
    score_sentiment()

