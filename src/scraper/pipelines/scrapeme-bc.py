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



rcknews_url = "https://www.racket.news"
rcknews_xpath = ("//html/body//a[contains(@data-testid,'post-preview-title')]//text()")


rcknews_headlines = get_headlines_racket('rcknews', rcknews_url,rcknews_xpath)




#columns = ['headline','journal','date']

headlines_list = []

mucho_array(rcknews_headlines, 'Racket News')

df_ = pd.DataFrame(headlines_list,None)
#print(list(nyt_data))
df_.to_csv('~/Documents/help/answerbank/resources/docs/beachcomber/headlines-bc.csv', header=None, sep=';',mode='a',encoding='utf-8', index=False)







