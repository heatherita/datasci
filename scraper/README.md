# scraper
Scrapes headlines from configured sites and writes CSV output.

Usage (refactored)

- Site definitions live under `src/sources/` (one module per source).
- Main entrypoint: `src/scrapeme-new.py` (also importable as `src/scrapeme_new.py`).

CSV output

- Raw CSVs are written to ~/data/scraper/ by default, one pair per source:
  `{site_name}-raw.csv` and `{site_name}-clean.csv`.

mycareer.nj.gov

- `src/sources/mycareer_nj.py` is a scaffold that includes `search_mycareer(params,username,password)`.
- Provide credentials via environment variables MYCAREER_USER and MYCAREER_PASS, or pass them directly to the function.
- The login/search flow will need customizing to match the live site's form fields and endpoints.

Run examples

```bash
# write CSVs to default location (~/data/scraper)
PYTHONPATH=src python3 src/scrapeme-new.py

# or import programmatically
PYTHONPATH=src python3 -c "import scrapeme_new; scrapeme_new.main()"
```

Dependencies

- Install required packages into your Python environment:

```bash
python3 -m pip install requests lxml pandas selenium beautifulsoup4
```

Notes

- The project expects a Firefox WebDriver for selenium (geckodriver) to be available on PATH if selenium-based sources are used.
- I did not install dependencies here; run the pip command above in your environment before executing the scripts.
# scraper
scraper: Scraping Headlines from 6 US news channels and saving them in a local file to accumulate a database of headlines.

#### Run

```Simply load project in PyCharm and run. Change the path to headlines.csv if desired.```

