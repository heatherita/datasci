#!/usr/bin/env python3
"""Consolidated exporter for CSV scraping.

This module merges functionality from the previous `scrapeme*` modules.
It exposes a `main(output_base)` entrypoint which writes per-source CSVs
based on `SOURCES` provided by `src/csv/sources/sources_config.py` or
other source modules that import this module.
"""
import datetime as dt
import re
import pandas as pd
import requests
from lxml import etree, html
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from pathlib import Path
from typing import Optional

from src.scraper_csv.sources import SOURCES  # type: ignore
from src.scraper_csv.cleancsv import clean_file  # type: ignore


def get_url_selenium(url: str, wait: float = 5.0):
    """Fetch a page using Selenium (Firefox) and return an lxml tree."""
    driver = webdriver.Firefox()
    try:
        driver.get(url)
        import time
        time.sleep(wait)
        page_source = driver.page_source
    finally:
        driver.quit()
    return html.fromstring(page_source)


def get_url_classic(url: str, timeout: int = 15):
    """Fetch a page using requests and return an lxml tree."""
    headers = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})
    r = requests.get(url, headers=headers, timeout=timeout)
    return html.fromstring(r.content)


def clean_elem(elem_str: str) -> str:
    elem_str = elem_str.strip('[ \t\n\r]+')
    elem_str = re.sub(r'\s+', ' ', elem_str)
    return elem_str


def clean_list(elem_list):
    if elem_list:
        elem_list_str = ' '.join(elem_list)
        return clean_elem(elem_list_str)
    return ''


def get_byline(article_tree, author_xpaths):
    for author_xpath in author_xpaths:
        headline_byline = article_tree.xpath(author_xpath)
        if headline_byline:
            return clean_list(headline_byline)
    return ''


def get_timestamp(article_tree, timestamp_xpaths):
    for timestamp_xpath in timestamp_xpaths:
        headline_timestamp = article_tree.xpath(timestamp_xpath)
        if headline_timestamp:
            return clean_list(headline_timestamp)
    return ''


def create_headlines_list(xpath_list):
    headlines_out = []
    for xpath_dict in xpath_list:
        site_name = xpath_dict.get('site_name')
        site_url = xpath_dict.get('site_url') or xpath_dict.get('url')
        if not site_url:
            continue
        domain_tokens = site_url.split('/')
        domain = '/'.join(domain_tokens[:3])
        headline_xpath = xpath_dict.get('headline_xpath')
        headline_title_xpath = xpath_dict.get('headline_title_xpath')
        headline_url_xpath = xpath_dict.get('headline_url_xpath')
        date_xpaths = [xpath_dict.get('headline_date_xpath'), "//html//body//*[starts-with(text(),'Updated: ')]//text()", "//html//body//*[starts-with(text(),'Published: ')]//text()"]
        author_xpaths = [xpath_dict.get('byline_xpath'), "//html//body//*[contains(@class,'byline')]//a//text()", "//html//body//*[contains(@class,'author')]//a//text()"]
        use_selenium = xpath_dict.get('use_sel') or xpath_dict.get('use_selenium')

        try:
            if use_selenium:
                tree = get_url_selenium(site_url)
            else:
                tree = get_url_classic(site_url)
        except Exception as e:
            print('fetch failed for', site_url, e)
            continue

        if not headline_xpath:
            # nothing to do for this site config
            continue

        headlines = tree.xpath(headline_xpath)

        for headline_block in headlines:
            headline_data = {'site_name': site_name,
                             'headline_byline': '',
                             'headline_date': '',
                             'headline_title': '',
                             'timestamp': dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S')}
            list_page_tree = etree.ElementTree(headline_block)
            headline_titles = list_page_tree.xpath(headline_title_xpath) if headline_title_xpath else []
            headline_data['headline_title'] = clean_list(headline_titles)
            if headline_url_xpath:
                headline_urls = list_page_tree.xpath(headline_url_xpath)
                for headline_url in headline_urls:
                    if headline_url:
                        if not headline_url[:4] == 'http':
                            headline_url = domain + '/' + headline_url
                        article_page_tree = get_url_classic(headline_url)
                        headline_data['headline_byline'] = get_byline(article_page_tree, author_xpaths)
                        headline_data['headline_date'] = get_timestamp(article_page_tree, date_xpaths)
            else:
                headline_data['headline_byline'] = get_byline(list_page_tree, author_xpaths)
                headline_data['headline_date'] = get_timestamp(list_page_tree, date_xpaths)
            headlines_out.append(headline_data)
    return headlines_out


def write_csv_for_source(source_dict, out_dir: Path):
    name = source_dict.get('site_name', 'unknown').replace(' ', '_')
    raw_path = out_dir / f"{name}-raw.csv"
    clean_path = out_dir / f"{name}-clean.csv"

    rows = create_headlines_list([source_dict])
    if not rows:
        print(f"No rows found for {name}")
        return
    df = pd.DataFrame(rows)
    out_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(raw_path, header=True, sep=';', mode='w', encoding='utf-8', index=False)

    # Attempt to clean using cleancsv; the cleaner expects a dict-based CSV layout
    try:
        clean_file(str(raw_path), str(clean_path))
    except Exception as e:
        print('clean_file failed:', e)


def main(output_base: Optional[str] = None):
    output_base = Path(output_base or Path.home() / 'data' / 'scraper')
    for source in SOURCES:
        # SOURCES may expose a list of dicts or a single dict
        if isinstance(source, list):
            for s in source:
                write_csv_for_source(s, output_base)
        else:
            write_csv_for_source(source, output_base)


if __name__ == '__main__':
    import sys
    outdir = sys.argv[1] if len(sys.argv) > 1 else None
    main(outdir)
