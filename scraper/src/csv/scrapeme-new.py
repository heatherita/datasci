#!/usr/bin/env python3
"""Refactored scraper entrypoint.

Loads site source configs from `src/sources` and writes per-source CSVs.
"""
import datetime as dt
import re
import pandas as pd
import requests
from lxml import etree, html
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
from pathlib import Path
from typing import Optional

from sources import SOURCES
from cleancsv import clean_file


def get_headlines_racket(site_name, url, site_xpath):
    driver = webdriver.Firefox()
    driver.implicitly_wait(0.5)
    driver.maximize_window()
    driver.get(url)
    # make optional
    try:
        driver.find_element(By.LINK_TEXT, "No thanks").click()
    except Exception:
        pass
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    headlines = soup.find_all(attrs={"data-testid": "post-preview-title"})
    headlines_list = []
    for item in headlines:
        headlines_list.append(item.text)
    return headlines_list


def get_url_selenium(url):
    print("selenium method: ", url)
    driver = webdriver.Firefox()
    driver.get(url)
    #!/usr/bin/env python3
    """Refactored scraper entrypoint.

    Loads site source configs from `src/sources` and writes per-source CSVs.
    """
    import datetime as dt
    import re
    import pandas as pd
    import requests
    from lxml import etree, html
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from bs4 import BeautifulSoup
    import os
    from pathlib import Path
    from typing import Optional

    from sources import SOURCES
    from cleancsv import clean_file


    def get_headlines_racket(site_name, url, site_xpath):
        driver = webdriver.Firefox()
        driver.implicitly_wait(0.5)
        driver.maximize_window()
        driver.get(url)
        # make optional
        try:
            driver.find_element(By.LINK_TEXT, "No thanks").click()
        except Exception:
            pass
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        headlines = soup.find_all(attrs={"data-testid": "post-preview-title"})
        headlines_list = []
        for item in headlines:
            headlines_list.append(item.text)
        return headlines_list


    def get_url_selenium(url):
        print("selenium method: ", url)
        driver = webdriver.Firefox()
        driver.get(url)
        # Wait for dynamic content to load (adjust sleep time as needed)
        import time
        time.sleep(5)
        page_source = driver.page_source
        driver.quit()
        tree = html.fromstring(page_source)
        return tree


    def get_url_classic(url):
        print("classic method: ", url)
        headers = ({'User-Agent':
                        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                        '(KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                    'Accept-Language': 'en-US, en;q=0.5'})

        webpage = requests.get(url, headers=headers)
        tree = html.fromstring(webpage.content)
        return tree


    def clean_list(elem_list):
        if elem_list:
            elem_list_str = ' '.join(elem_list)
            return clean_elem(elem_list_str)
        return ''


    def clean_elem(elem_str):
        elem_str = elem_str.strip('[ \t\n\r]+')
        elem_str = re.sub('\\s+', ' ', elem_str)
        return elem_str


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
            site_url = xpath_dict.get('site_url')
            domain_tokens = site_url.split('/')
            domain = '/'.join(domain_tokens[:3])
            headline_xpath = xpath_dict.get('headline_xpath')
            headline_title_xpath = xpath_dict.get('headline_title_xpath')
            headline_url_xpath = xpath_dict.get('headline_url_xpath')
            date_xpaths = [xpath_dict.get('headline_date_xpath'), "//html//body//*[starts-with(text(),'Updated: ')]//text()", "//html//body//*[starts-with(text(),'Published: ')]//text()"]
            author_xpaths = [xpath_dict.get('byline_xpath'), "//html//body//*[contains(@class,'byline')]//a//text()", "//html//body//*[contains(@class,'author')]//a//text()"]
            use_selenium = xpath_dict.get('use_sel')

            if use_selenium:
                tree = get_url_selenium(site_url)
            else:
                tree = get_url_classic(site_url)

            headlines = tree.xpath(headline_xpath)

            for headline_block in headlines:
                headline_data = {'site_name': site_name,
                                 'headline_byline': '',
                                 'headline_date': '',
                                 'headline_title': '',
                                 'timestamp': dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S')}
                list_page_tree = etree.ElementTree(headline_block)
                headline_titles = list_page_tree.xpath(headline_title_xpath)
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
    import pandas as pd
    import requests
    from lxml import etree, html
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from bs4 import BeautifulSoup
    import os
    from pathlib import Path

    from sources import SOURCES
    from cleancsv import clean_file


    def get_headlines_racket(site_name, url, site_xpath):
        driver = webdriver.Firefox()
        driver.implicitly_wait(0.5)
        driver.maximize_window()
        driver.get(url)
        # make optional
        try:
            driver.find_element(By.LINK_TEXT, "No thanks").click()
        except Exception:
            pass
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        headlines = soup.find_all(attrs={"data-testid": "post-preview-title"})
        headlines_list = []
        for item in headlines:
            headlines_list.append(item.text)
        return headlines_list


    def get_url_selenium(url):
        print("selenium method: ", url)
        driver = webdriver.Firefox()
        driver.get(url)
        # Wait for dynamic content to load (adjust sleep time as needed)
        import time
        time.sleep(5)
        page_source = driver.page_source
        driver.quit()
        tree = html.fromstring(page_source)
        return tree


    def get_url_classic(url):
        print("classic method: ", url)
        headers = ({'User-Agent':
                        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                        '(KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                    'Accept-Language': 'en-US, en;q=0.5'})

        webpage = requests.get(url, headers=headers)
        tree = html.fromstring(webpage.content)
        return tree


    def clean_list(elem_list):
        if elem_list:
            elem_list_str = ' '.join(elem_list)
            return clean_elem(elem_list_str)


    def clean_elem(elem_str):
        elem_str = elem_str.strip('[ \t\n\r]+')
        elem_str = re.sub('\s+', ' ', elem_str)
        return elem_str


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
            site_url = xpath_dict.get('site_url')
            domain_tokens = site_url.split('/')
            domain = '/'.join(domain_tokens[:3])
            headline_xpath = xpath_dict.get('headline_xpath')
            headline_title_xpath = xpath_dict.get('headline_title_xpath')
            headline_url_xpath = xpath_dict.get('headline_url_xpath')
            date_xpaths = [xpath_dict.get('headline_date_xpath'), "//html//body//*[starts-with(text(),'Updated: ')]//text()", "//html//body//*[starts-with(text(),'Published: ')]//text()"]
            author_xpaths = [xpath_dict.get('byline_xpath'), "//html//body//*[contains(@class,'byline')]//a//text()", "//html//body//*[contains(@class,'author')]//a//text()"]
            use_selenium = xpath_dict.get('use_sel')

            if use_selenium:
                tree = get_url_selenium(site_url)
            else:
                tree = get_url_classic(site_url)

            headlines = tree.xpath(headline_xpath)

            for headline_block in headlines:
                headline_data = {'site_name': site_name,
                                 'headline_byline': '',
                                 'headline_date': '',
                                 'headline_title': '',
                                 'timestamp': dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S')}
                list_page_tree = etree.ElementTree(headline_block)
                headline_titles = list_page_tree.xpath(headline_title_xpath)
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


    def main(output_base: str | None = None):
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
