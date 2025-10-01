"""Scraper for https://mycareer.nj.gov.

This module exposes a function `search_mycareer(params, username, password)` which
should return an iterable of rows (lists or tuples) ready to be written to CSV.

Important: the implementation below is a scaffold. Website login and search
flows change over time; adapt the selectors and form fields after inspecting
the current site with your browser's dev tools.
"""
import os
import requests
from lxml import html


def search_mycareer(params: dict, username: str | None = None, password: str | None = None):
    """Login (if credentials provided) and perform a search using `params`.

    Args:
        params: mapping of search parameters (job title, location, etc). Keys are site-specific.
        username: optional username for login. If None, will try from env var MYCAREER_USER.
        password: optional password for login. If None, will try from env var MYCAREER_PASS.

    Returns:
        Iterable of rows (list/tuple) where each row represents a job result.
    """
    session = requests.Session()
    username = username or os.environ.get('MYCAREER_USER')
    password = password or os.environ.get('MYCAREER_PASS')

    # Example login flow placeholder (inspect site to get actual form fields)
    login_url = 'https://mycareer.nj.gov/Account/Login'
    if username and password:
        # Fetch login page to get anti-forgery tokens if present
        r = session.get(login_url)
        tree = html.fromstring(r.content)
        # Example: token = tree.xpath("//input[@name='__RequestVerificationToken']/@value")
        payload = {
            'Username': username,
            'Password': password,
            # Include token here if required
        }
        # Post credentials - adjust URL and payload keys as needed
        session.post(login_url, data=payload)

    # Perform search - adjust endpoint and params as required
    search_url = 'https://mycareer.nj.gov/jobs/search'  # likely needs update
    resp = session.get(search_url, params=params)
    tree = html.fromstring(resp.content)

    # Example xpath for job rows - update according to site
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
