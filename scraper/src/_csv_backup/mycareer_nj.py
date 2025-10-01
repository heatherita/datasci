"""Backup copy of mycareer_nj scaffold."""
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
        payload = {
            'Username': username,
            'Password': password,
        }
        session.post(login_url, data=payload)

    search_url = 'https://mycareer.nj.gov/jobs/search'
    resp = session.get(search_url, params=params)
    tree = html.fromstring(resp.content)

    job_rows = tree.xpath("//div[contains(@class,'job-result')]")
    results = []
    for job in job_rows:
        title = job.xpath(".//h3//text()")
        location = job.xpath(".//span[contains(@class,'location')]//text()")
        posted = job.xpath(".//span[contains(@class,'posted-date')]//text()")
        results.append([
            ' '.join([t.strip() for t in title if t.strip()]),
            ' '.join([l.strip() for l in location if l.strip()]),
            ' '.join([p.strip() for p in posted if p.strip()]),
        ])

    return results
