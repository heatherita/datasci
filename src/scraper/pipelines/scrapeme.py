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
    #make optional
    driver.find_element(By.LINK_TEXT, "No thanks").click()
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #list_items = soup.find_all(("a", class_="pencraft pc-reset"))
    headlines = soup.find_all(attrs={"data-testid": "post-preview-title"})
    headlines_list = []
    for item in headlines:
        print(item.text)
        headlines_list.append(item.text)
    return headlines_list

def get_headlines(site_name, url, site_xpath):
    HEADERS = ({'User-Agent':
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})

    webpage = requests.get(url, headers=HEADERS)
    tree = html.fromstring(webpage.content)
    headlines=tree.xpath(site_xpath)
    #print('sitename: ', site_name, 'headlines: ', headlines)
    return headlines

def mucho_array(journal_list, journal_name):
    #nlist = []
    for headline in journal_list:
        if re.search('[a-zA-Z0-9]+',headline):
            #print('headline, before clean: ', headline, len(headline))
            headline = headline.strip(' \t\n\r')
            #print('headline, after clean: ', headline, len(headline))
            tlist = [headline,journal_name,dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S')]
            headlines_list.append(tlist)


nyt_url = "https://www.nytimes.com/section/us"
nyt_xpath = "//html//article//a/text()"
jtn_url = "https://justthenews.com/nation"
jtn_xpath = "//html/body//article[contains(@class, 'node--article')]//div[contains(@class, 'node__text')]/h3/a/text()"
nypost_url = "https://nypost.com/news/"
nypost_xpath = "//html//h3[contains(@class, 'story__headline')]/a//text()"
#cnn_url = "https://www.cnn.com/us"
#cnn_xpath = "//html//section//div//span[1][not(contains(@class, 'container_lead-plus-headlines__text-label'))]/text()"

cnn_url = "https://www.cnn.com"
cnn_xpath = "//html//section//div//span[contains(@class, 'container__headline-text')]/text()"

axios_url = "https://www.axios.com/"
axios_xpath = "//html/body/div/div[1]/div[2]/main/div[2]/div[2]/div[2]//h2/a/span/text()"
foxnews_url = "https://www.foxnews.com/us"
foxnews_xpath = "//html//section[contains(@class, 'collection-article-list')]/div/article[contains(@class, 'article')]/div/header/h4/a/text()"
dwnews_url = "https://www.dailywire.com/topic/readers-pass"
dwnews_xpath = ("//html/body//article[contains(@class, 'css')]//h3//text()")
rcknews_url = "https://www.racket.news"
rcknews_xpath = ("//html/body//a[contains(@data-testid,'post-preview-title')]//text()")

nyt_headlines = get_headlines('ny times',nyt_url,nyt_xpath)
jtn_headlines = get_headlines('just the news', jtn_url,jtn_xpath)
nypost_headlines = get_headlines('ny post', nypost_url,nypost_xpath)
#after 2024-11-05 9:31 pm I use cnn.com and not cnn.com/us
cnn_headlines = get_headlines('cnn', cnn_url,cnn_xpath)
axios_headlines = get_headlines('axios', axios_url,axios_xpath)
foxnews_headlines = get_headlines('foxnews', foxnews_url,foxnews_xpath)
dwnews_headlines = get_headlines('dwnews', dwnews_url,dwnews_xpath)
rcknews_headlines = get_headlines_racket('rcknews', rcknews_url,rcknews_xpath)




#columns = ['headline','journal','date']

headlines_list = []
mucho_array(nyt_headlines, 'NY Times')
mucho_array(jtn_headlines, 'Just the News')
mucho_array(nypost_headlines, 'NY Post')
mucho_array(cnn_headlines, 'CNN')
mucho_array(axios_headlines, 'Axios')
mucho_array(foxnews_headlines, 'Fox News')
mucho_array(dwnews_headlines, 'Daily Wire')
mucho_array(rcknews_headlines, 'Racket News')

df_ = pd.DataFrame(headlines_list,None)
#print(list(nyt_data))
df_.to_csv('~/data/scraper/cleaned/headlines-new.csv', header=None, sep=';',mode='a',encoding='utf-8', index=False)







