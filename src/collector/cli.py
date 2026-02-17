import argparse
from collector.pipelines.reddit_data import collect_reddit_main

def run(args):
    print(f"Running collector for {args.source}")

def build_parser() -> argparse.ArgumentParser:

    # parser = argparse.ArgumentParser()
    # sub = parser.add_subparsers(dest="command")

    p = argparse.ArgumentParser(prog="collector")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("collect-reddit")
    # s.add_argument("url")
    # s.add_argument("--out", default="out/urls.txt")
    s.set_defaults(func=collect_reddit_main)

    run_parser = sub.add_parser("run")
    run_parser.add_argument("--source", required=True)
    run_parser.add_argument("--days", type=int, default=1)
    run_parser.set_defaults(func=run)

    return p
    # args = parser.parse_args()
    # if hasattr(args, "func"):
    #     args.func(args)

def main() -> None:
    args = build_parser().parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
