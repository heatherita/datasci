"""Export scraped pages as JSONL for RAG ingestion.

This module implements simple heuristics to extract article/training details
from the NJ sites you specified. It's tolerant to minor HTML differences but
may require tweaks for exact fields.
"""
import hashlib
import json
import re
from datetime import datetime
from typing import Dict, Iterable, List
from urllib.parse import urljoin, urlparse

import requests
from lxml import html


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Safari/537.36',
}


def fetch_tree(url: str, timeout: int = 15):
    r = requests.get(url, headers=HEADERS, timeout=timeout)
    r.raise_for_status()
    return html.fromstring(r.content)


def clean_text(text: str) -> str:
    if not text:
        return ''
    # collapse whitespace and trim
    return re.sub(r'\s+', ' ', text).strip()


# NOTE: chunking and explicit metadata cleaning were previously added.
# The user requested plain JSON output with no chunking/cleaning, so we
# intentionally keep extraction minimal below and write a single JSON array
# when the output path ends with '.json'.


def make_id(url: str) -> str:
    return hashlib.sha1(url.encode('utf-8')).hexdigest()


def extract_mycareer_detail(tree: html.HtmlElement, url: str) -> Dict:
    # Heuristics for fields
    title = tree.xpath('//h1/text()') or tree.xpath('//title/text()')
    title = clean_text(title[0]) if title else ''

    # description: join paragraphs in main/article
    paragraphs = tree.xpath('//main//p//text() | //article//p//text()')
    if not paragraphs:
        paragraphs = tree.xpath('//div[contains(@class, "summary") or contains(@class, "description")]//text()')
    description = clean_text(' '.join(paragraphs))

    # metadata heuristics: look for labels and values
    metadata = {}
    # find provider/organization labels
    provider = tree.xpath("//text()[contains(., 'Provider')]/following::text()[1]")
    if provider:
        metadata['provider'] = clean_text(provider[0])

    # try to capture contact/location/delivery type
    rows = tree.xpath("//dt/text() | //th/text() | //div[contains(@class,'meta')]//text()")
    # minimal attempt: add any short 'key: value' text fragments
    text_nodes = tree.xpath('//text()')
    for n in text_nodes:
        if ':' in n and len(n.split(':', 1)[0]) < 30:
            k, v = n.split(':', 1)
            k = clean_text(k)
            v = clean_text(v)
            if k and v and len(v) < 200:
                metadata[k.lower()] = v

    return {
        'id': make_id(url),
        'source': 'mycareer.nj.gov',
        'url': url,
        'title': title,
        'description': description,
        'metadata': metadata,
        'scraped_at': datetime.utcnow().isoformat() + 'Z',
    }


def extract_njgov_training(tree: html.HtmlElement, url: str) -> Dict:
    title = tree.xpath('//h1/text()') or tree.xpath('//title/text()')
    title = clean_text(title[0]) if title else ''
    paragraphs = tree.xpath('//main//p//text() | //div[contains(@class, "content")]//p//text()')
    description = clean_text(' '.join(paragraphs))
    return {
        'id': make_id(url),
        'source': 'nj.gov',
        'url': url,
        'title': title,
        'description': description,
        'metadata': {},
        'scraped_at': datetime.utcnow().isoformat() + 'Z',
    }


def find_mycareer_detail_urls(search_url: str) -> List[str]:
    tree = fetch_tree(search_url)
    # links that contain '/training/' followed by digits
    hrefs = tree.xpath("//a[contains(@href,'/training/')]/@href")
    detail_urls = []
    for h in hrefs:
        # normalize
        joined = urljoin(search_url, h)
        path = urlparse(joined).path
        if re.search(r'/training/\d+$', path):
            if joined not in detail_urls:
                detail_urls.append(joined)
    return detail_urls


def export_mycareer_search(search_url: str, out_fh):
    detail_urls = find_mycareer_detail_urls(search_url)
    for u in detail_urls:
        try:
            tree = fetch_tree(u)
            doc = extract_mycareer_detail(tree, u)
            out_fh.write(json.dumps(doc, ensure_ascii=False) + '\n')
        except Exception as e:
            print('Failed to fetch', u, 'error:', e)


def export_njgov_training(listing_url: str, out_fh):
    tree = fetch_tree(listing_url)
    # find links under the page that go to training details
    hrefs = tree.xpath("//a[contains(@href,'/training/')]/@href | //a[contains(@href,'/training')]/@href")
    seen = set()
    for h in hrefs:
        u = urljoin(listing_url, h)
        if u in seen:
            continue
        seen.add(u)
        try:
            t = fetch_tree(u)
            doc = extract_njgov_training(t, u)
            out_fh.write(json.dumps(doc, ensure_ascii=False) + '\n')
        except Exception as e:
            print('Failed to fetch', u, 'error:', e)


def main_for_urls(urls: Iterable[str], out_path: str = 'output.jsonl'):
    Path = __import__('pathlib').Path
    outp = Path(out_path)
    outp.parent.mkdir(parents=True, exist_ok=True)
    # If out_path ends with .json, write a single JSON array. Otherwise write
    # newline-delimited JSON (JSONL) as before.
    as_array = str(outp).lower().endswith('.json')
    docs = []
    for url in urls:
        parsed = urlparse(url)
        if 'mycareer.nj.gov' in parsed.netloc:
            if re.search(r'/training/search', parsed.path) or parsed.query:
                # export_mycareer_search writes to a filehandle; collect docs
                # by calling find_mycareer_detail_urls + extract
                detail_urls = find_mycareer_detail_urls(url)
                for u in detail_urls:
                    try:
                        tree = fetch_tree(u)
                        doc = extract_mycareer_detail(tree, u)
                        docs.append(doc)
                    except Exception as e:
                        print('Failed to fetch detail', u, 'error:', e)
            elif re.search(r'/training/\d+$', parsed.path):
                try:
                    tree = fetch_tree(url)
                    doc = extract_mycareer_detail(tree, url)
                    docs.append(doc)
                except Exception as e:
                    print('Failed detail fetch', url, e)
        elif 'nj.gov' in parsed.netloc:
            # listing page -> collect detail links similarly
            hrefs = fetch_tree(url).xpath("//a[contains(@href,'/training/')]/@href | //a[contains(@href,'/training')]/@href")
            seen = set()
            for h in hrefs:
                u = urljoin(url, h)
                if u in seen:
                    continue
                seen.add(u)
                try:
                    t = fetch_tree(u)
                    doc = extract_njgov_training(t, u)
                    docs.append(doc)
                except Exception as e:
                    print('Failed to fetch', u, 'error:', e)
        else:
            # generic fallback: fetch and extract paragraphs
            try:
                tree = fetch_tree(url)
                title = tree.xpath('//h1/text()') or tree.xpath('//title/text()')
                desc = tree.xpath('//p//text()')
                doc = {
                    'id': make_id(url),
                    'source': parsed.netloc,
                    'url': url,
                    'title': clean_text(title[0]) if title else '',
                    'description': clean_text(' '.join(desc)),
                    'metadata': {},
                    'scraped_at': datetime.utcnow().isoformat() + 'Z',
                }
                docs.append(doc)
            except Exception as e:
                print('Failed generic fetch', url, e)

    if as_array:
        with open(outp, 'w', encoding='utf-8') as fh:
            json.dump(docs, fh, ensure_ascii=False, indent=2)
    else:
        with open(outp, 'w', encoding='utf-8') as fh:
            for d in docs:
                fh.write(json.dumps(d, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    import sys
    # sample usage: python jsonl_exporter.py output.jsonl url1 url2 ...
    if len(sys.argv) < 3:
        print('Usage: python jsonl_exporter.py <output.jsonl> <url1> [<url2> ...]')
        sys.exit(1)
    out = sys.argv[1]
    urls = sys.argv[2:]
    main_for_urls(urls, out)