"""CSV source configs for the CSV exporter.

Place SOURCE dicts here. The CSV exporter will import `SOURCES` and call
the existing scraper functions to write CSVs.
"""

from .sources_config import SOURCES, OUTPUT_DIR  # noqa: F401
