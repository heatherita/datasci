import argparse

from collector.db.database import Base, SessionLocal, engine
from collector.pipelines.reddit_data import collect_reddit_main
from collector.pipelines.reddit_clean import clean_reddit_main
from collector.pipelines.reddit_score import score_reddit_main
from collector.db import models  # IMPORTANT: ensures models are registered

def run(args):
    print(f"Running collector for {args.source}")

def build_parser() -> argparse.ArgumentParser:

    p = argparse.ArgumentParser(prog="collector")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("collect-reddit")
    s.set_defaults(func=collect_reddit_main)

    s = sub.add_parser("clean-reddit")
    s.set_defaults(func=clean_reddit_main)

    s = sub.add_parser("score-reddit")
    s.set_defaults(func=score_reddit_main)

    run_parser = sub.add_parser("run")
    run_parser.add_argument("--source", required=True)
    run_parser.add_argument("--days", type=int, default=1)
    run_parser.set_defaults(func=run)

    return p


def main() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        args = build_parser().parse_args()
        args.func(args)
    finally:
        db.close()

if __name__ == "__main__":
    main()
