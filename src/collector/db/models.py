from enum import UNIQUE

from sqlalchemy import Column, Integer, Float, String, Text, DateTime, Boolean, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
# from database import Base
import enum
from collector.db.database import Base


class RedditSubmission(Base):
    __tablename__ = "reddit_submission"

    id = Column(Integer, primary_key=True, index=True)
    reddit_id = Column(Text,unique=True)
    subreddit = Column(Text)
    title = Column(Text)
    selftext = Column(Text)
    score = Column(Integer)
    num_comments = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    fetched_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    submission_sentiment = relationship("RedditSubmissionSentiment", back_populates="reddit_submission")

class RedditSubmissionSentiment(Base):
    __tablename__ = "reddit_submission_sentiment"

    id = Column(Integer, primary_key=True, index=True)
    reddit_id = Column(Text,unique=True)
    sentiment_score = Column(Float)
    polarity = Column(Integer)
    submission_id = Column(Integer, ForeignKey("reddit_submission.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    reddit_submission = relationship("RedditSubmission", back_populates="submission_sentiment")


