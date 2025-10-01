"""Copied mycareer helper into scraper_csv package."""
from ..csv.sources import mycareer_nj as _mc  # type: ignore

search_mycareer = _mc.search_mycareer
