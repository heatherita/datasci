"""Example source file for news sites. Export a list of SOURCE dicts or a single SOURCE dict.
"""
SOURCE = [
    {
        'site_name': "ny times",
        'site_url': "https://www.nytimes.com/section/us",
        'headline_xpath': "//html/body//main/section//div/section[contains(@id, 'stream-panel')]/div/ol//li",
        'headline_url_xpath': "",
        'headline_title_xpath': "//a/h3/text()",
        'headline_date_xpath': "//div/span[@data-testid = 'todays-date']/text()",
        'byline_xpath': "//article/p[2]/span/text()",
        'use_sel': True
    },
    {
        'site_name': 'just the news',
        'site_url': 'https://justthenews.com/nation',
        'headline_xpath': "//html/body//article",
        'headline_url_xpath': "//div[contains(@class, 'node__text')]/h3/a/@href",
        'headline_title_xpath': "//div[contains(@class, 'node__text')]/h3/a/text()",
        'headline_date_xpath': "//html/body//div/main//article//div[contains(@class, 'node__meta')]/div[contains(@class, 'node__dates')]//text()",
        'byline_xpath': "//html/body//div/main//article//div[contains(@class, 'node__meta')]/div[contains(@class, 'node__byline')]//text()",
        'use_sel': False
    }
]
