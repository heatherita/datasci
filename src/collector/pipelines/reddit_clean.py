import re
from collector.db.database import SessionLocal
from collector.db.models import RedditSubmission

db = SessionLocal()

def clean_text(text: str) -> str:
    if not text:
        return ""

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove zero-width spaces
    text = re.sub(r"\u200b", "", text)

    # Collapse multiple spaces/tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Collapse 3+ newlines into 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()

def clean_whitespace():
    try:
        posts = db.query(RedditSubmission).all()

        for post in posts:
            post.title = clean_text(post.title)
            post.selftext = clean_text(post.selftext)

        db.commit()
    finally:
        db.close()

def clean_reddit_main(args) -> None:
    print(f"in collect_reddit_main")
    clean_whitespace()