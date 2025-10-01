"""Scraper for https://mycareer.nj.gov used as a CSV source module.

Expose either a function `search_mycareer(params, username, password)` or a
`SOURCE` dict/structure that the CSV exporter can use.
"""
import os
import requests
from lxml import html


def search_mycareer(params: dict, username: str | None = None, password: str | None = None):
    session = requests.Session()
    username = username or os.environ.get('MYCAREER_USER')
    password = password or os.environ.get('MYCAREER_PASS')

    login_url = 'https://mycareer.nj.gov/Account/Login'
    if username and password:
        r = session.get(login_url)
        tree = html.fromstring(r.content)
        payload = {'Username': username, 'Password': password}
        session.post(login_url, data=payload)

    search_url = 'https://mycareer.nj.gov/training/search'
    resp = session.get(search_url, params=params)
    tree = html.fromstring(resp.content)

    job_rows = tree.xpath("//div[contains(@class,'training-result')]")
    results = []
    for job in job_rows:
        title = job.xpath(".//h3//text()")
        provider = job.xpath(".//div[contains(@class,'provider')]//text()")
        location = job.xpath(".//span[contains(@class,'location')]//text()")
        results.append([
            ' '.join([t.strip() for t in title if t.strip()]),
            ' '.join([p.strip() for p in provider if p.strip()]),
            ' '.join([l.strip() for l in location if l.strip()]),
        ])
    return results
