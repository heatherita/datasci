"""Copied config to new scraper_csv package to avoid name clash."""
OUTPUT_DIR = '/home/heather/data/scraper/csv'

SOURCES = [
    {
        'site_name': 'mycareer_nj_search_example',
        'urls': [
            'https://mycareer.nj.gov/training/search?q=lascomp+%2Bcomptia'
        ],
    }
]
