import datetime as dt
import re
import pandas as pd
import requests
from lxml import etree, html
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def get_headlines_racket(site_name, url, site_xpath):
    driver = webdriver.Firefox()
    driver.implicitly_wait(0.5)
    driver.maximize_window()
    driver.get(url)
    # make optional
    driver.find_element(By.LINK_TEXT, "No thanks").click()
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # list_items = soup.find_all(("a", class_="pencraft pc-reset"))
    driver.quit()
    headlines = soup.find_all(attrs={"data-testid": "post-preview-title"})
    headlines_list = []
    for item in headlines:
        print(item.text)
        headlines_list.append(item.text)
    return headlines_list

def get_url_selenium(url):
    print("selenium method: ", url)
    driver = webdriver.Firefox()
    driver.get(url)
    # Wait for dynamic content to load (adjust sleep time as needed)
    import time
    time.sleep(5)  # Or use WebDriverWait for better reliability
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
        print('clean_list, after clean: ', elem_list_str)
        return clean_elem(elem_list_str)


def clean_elem(elem_str):
    #if re.search('[a-zA-Z0-9]+', elem_str):
    elem_str = elem_str.strip('[ \t\n\r]+')
    #re.sub('\\r+', '', elem_str)
    #re.sub('\\t+', '', elem_str)
    #re.sub('\\n+', '', elem_str)
    elem_str = re.sub('\\s+', ' ', elem_str)
    # elem_str = elem_str.strip('[By|Updated|Published| .|:]+')
    print('elem, after clean: ', elem_str, len(elem_str))
    return elem_str


def get_byline(article_tree, author_xpaths):
    byline_found = False

    for author_xpath in author_xpaths:
        if not byline_found:
            headline_byline = article_tree.xpath(author_xpath)
            if headline_byline:
                byline_found = True
    if headline_byline:
        print('from article page byline: ', headline_byline[0])
        return clean_list(headline_byline)


def get_timestamp(article_tree, timestamp_xpaths):
    timestamp_found = False

    for timestamp_xpath in timestamp_xpaths:
        if not timestamp_found:
            headline_timestamp = article_tree.xpath(timestamp_xpath)
            if headline_timestamp:
                timestamp_found = True
    if headline_timestamp:
        print('from article page timestamp: ', headline_timestamp[0])
        return clean_list(headline_timestamp)


def create_headlines_list(xpath_list):
    for xpath_dict in xpath_list:
        site_name = xpath_dict.get('site_name')
        site_url = xpath_dict.get('site_url')
        domain_tokens = site_url.split('/')
        domain = '/'.join(domain_tokens[:3])
        print('domain: ', domain)
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

        # news_blurb = tree.xpath("//html/body//main/section//div/section[contains(@id, 'stream-panel')]//ol")[1]
        # print("news_blurb:", etree.tostring(news_blurb, pretty_print=True).decode())

        headlines = tree.xpath(headline_xpath)

        # get child xpaths
        for headline_block in headlines:
            headline_data = {'site_name': site_name,
                             'headline_byline': '',
                             'headline_date': '',
                             'headline_title': '',
                             'timestamp': dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S')}
            list_page_tree = etree.ElementTree(headline_block)
            # print("list page tree:", etree.tostring(list_page_tree, pretty_print=True).decode())
            headline_titles = list_page_tree.xpath(headline_title_xpath)
            headline_data['headline_title'] = clean_list(headline_titles)
            if headline_url_xpath:
                headline_urls = list_page_tree.xpath(headline_url_xpath)
                for headline_url in headline_urls:
                    if headline_url:
                        # print('headline_url: ', headline_url)
                        # print("headline_url tree:", etree.tostring(headline_url, pretty_print=True).decode())
                        if not headline_url[:4] == 'http':
                            headline_url = domain + '/' + headline_url
                        print('headline_url: ', headline_url)
                        article_page_tree = get_url_classic(headline_url)
                        headline_data['headline_byline'] = get_byline(article_page_tree, author_xpaths)
                        headline_data['headline_date'] = get_timestamp(article_page_tree,date_xpaths)
            else:
                headline_data['headline_byline'] = get_byline(list_page_tree, author_xpaths)
                headline_data['headline_date'] = get_timestamp(list_page_tree, date_xpaths)
            headlines_list.append(headline_data)
    return headlines_list


xpaths = []
headlines_list = []

nytimes_xpaths = {
    'site_name': "ny times",
    'site_url': "https://www.nytimes.com/section/us",
    'headline_xpath': "//html/body//main/section//div/section[contains(@id, 'stream-panel')]/div/ol//li",
    'headline_url_xpath': "",
    'headline_title_xpath': "//a/h3/text()",
    'headline_date_xpath': "//div/span[@data-testid = 'todays-date']/text()",
    'byline_xpath': "//article/p[2]/span/text()",
    'use_sel': True
}
#xpaths.append(nytimes_xpaths)

jtn_xpaths = {
    'site_name': 'just the news',
    'site_url': 'https://justthenews.com/nation',
    'headline_xpath': "//html/body//article",
    'headline_url_xpath': "//div[contains(@class, 'node__text')]/h3/a/@href",
    'headline_title_xpath': "//div[contains(@class, 'node__text')]/h3/a/text()",
    'headline_date_xpath': "//html/body//div/main//article//div[contains(@class, 'node__meta')]/div[contains(@class, 'node__dates')]//text()",
    'byline_xpath': "//html/body//div/main//article//div[contains(@class, 'node__meta')]/div[contains(@class, 'node__byline')]//text()",
    'use_sel': False
}
#xpaths.append(jtn_xpaths)

nypost_xpaths = {
    'site_name': 'ny post',
    'site_url': "https://nypost.com/us-news",
    'headline_xpath': "//html/body//div/main//div[contains(@class, 'the-latest__story')]",
    'headline_url_xpath': "//h3[contains(@class, 'story__headline')]/a/@href",
    'headline_title_xpath': "//h3[contains(@class, 'story__headline')]/a/text()",
    'headline_date_xpath': "//div[contains(@class, 'meta--byline')]//span[contains(@class, 'updated-date')]/text()",
    'byline_xpath': "//div[contains(@class, 'meta--byline')]//div[contains(@class, 'byline__author')]//a/text()",
    'use_sel': False
}
#xpaths.append(nypost_xpaths)

cnn_xpaths = {
    'site_name': 'cnn',
    'site_url': "https://www.cnn.com/us",
    'headline_xpath': "//html/body//section//div[contains(@class,'container_lead-plus-headlines__item--type-section')]",
    'headline_url_xpath': "//a[contains(@class,'container_lead-plus-headlines')][1]/@href",
    'headline_title_xpath': "//a[contains(@class,'container_lead-plus-headlines')]//span[contains(@class, 'container__headline-text')]/text()",
    'headline_date_xpath': "//html//body//div//section//div[contains(@class,'headline__byline-sub-text')]//div[contains(@class,'timestamp')]/text()",
    'byline_xpath': "//html//body//div//section//div[contains(@class,'byline')]//div[contains(@class,'byline__names')]//span/text()",
    'use_sel': True
}
xpaths.append(cnn_xpaths)

# extra_xpaths = {
#     'site_name': '#update',
#     'site_url': '#update',
#     'headline_xpath': "#update",
#     'headline_url_xpath': "#update",
#     'headline_title_xpath': "#update",
#     'headline_date_xpath': "#update",
#     'byline_xpath': "#update",
#     'use_sel': False
# }

# axios_url = "https://www.axios.com/"
# axios_xpath = "//html/body/div/div[1]/div[2]/main/div[2]/div[2]/div[2]//h2/a/span/text()"
# foxnews_url = "https://www.foxnews.com/us"
# foxnews_xpath = "//html//section[contains(@class, 'collection-article-list')]/div/article[contains(@class, 'article')]/div/header/h4/a/text()"
# dwnews_url = "https://www.dailywire.com/topic/readers-pass"
# dwnews_xpath = ("//html/body//article[contains(@class, 'css')]//h3//text()")
# rcknews_url = "https://www.racket.news"
# rcknews_xpath = ("//html/body//a[contains(@data-testid,'post-preview-title')]//text()")

create_headlines_list(xpaths)

# nyt_headlines = get_headlines('ny times',nyt_url,nyt_xpath)
# jtn_headlines = get_headlines('just the news', jtn_url,jtn_xpath)
# nypost_headlines = get_headlines('ny post', nypost_url,nypost_xpath)
# after 2024-11-05 9:31 pm I use cnn.com and not cnn.com/us
# cnn_headlines = get_headlines('cnn', cnn_url,cnn_xpath)
# axios_headlines = get_headlines('axios', axios_url,axios_xpath)
# foxnews_headlines = get_headlines('foxnews', foxnews_url,foxnews_xpath)
# dwnews_headlines = get_headlines('dwnews', dwnews_url,dwnews_xpath)
# rcknews_headlines = get_headlines_racket('rcknews', rcknews_url,rcknews_xpath)


df_ = pd.DataFrame(headlines_list, None)
df_.to_csv('~/data/scraper/authors/headlines-cnn.csv', header=None, sep=';', mode='a', encoding='utf-8', index=False)
