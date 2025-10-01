import sys
from pathlib import Path

# make src importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from src.scraper_jsonl.sources.mycareer_nj import OUTPUT_PATH, URLS  # type: ignore
import jsonl_exporter as _je  # module in src/jsonl_exporter.py


def run():
    out = OUTPUT_PATH
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    _je.main_for_urls(URLS, out)


if __name__ == '__main__':
    run()
