import sys
from pathlib import Path
import csv

# make src importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from exporter import main as run_scraper  # noqa: E402
from src.scraper_csv.sources.sources_config import SOURCES, OUTPUT_DIR  # type: ignore


def write_csv_for_sources():
    outdir = Path(OUTPUT_DIR)
    outdir.mkdir(parents=True, exist_ok=True)
    # For now simply call the existing runner which writes to default location
    # Advanced: iterate SOURCES and call write_csv_for_source per config.
    run_scraper(str(outdir))


if __name__ == '__main__':
    write_csv_for_sources()
