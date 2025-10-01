# scraper
scraper: Scraping Headlines from 6 US news channels and saving them in a local file to accumulate a database of headlines.

#### Run

```Simply load project in PyCharm and run. Change the path to headlines.csv if desired.```

#### JSONL

```python jsonl-exporter.py /home/heather/data/scraper/jobs-nj/jobs.json \
https://mycareer.nj.gov/training/search?q=lascomp+%2Bcomptia \
https://mycareer.nj.gov/training/search?q=lascomp++pmp \
https://mycareer.nj.gov/training/search?q=lascomp++entrepreneur https://mycareer.nj.gov/training/search?q=kaizen+pmp \
https://mycareer.nj.gov/training/search?q=kaizen+data https://nj.gov/labor/myunemployment/jobseekers/training/
