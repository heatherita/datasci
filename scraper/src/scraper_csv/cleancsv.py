"""Thin passthrough to existing cleancsv implementation in src/csv/cleancsv.py
This file exists to keep import locations stable after renaming packages.
"""
from ..csv.cleancsv import clean_file  # type: ignore
