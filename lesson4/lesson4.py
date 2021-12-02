import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from lxml import html
import requests
import datetime
from pprint import pprint

def parse_from_email():
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    url = 'https://news.mail.ru/'
    res = requests.get(url)
    dom = html.fromstring(res.text)
    news_links = dom.xpath('//a[@class="list__text"]/@href | //a[contains(@class, "js-topnews__item")]/@href')
    # parsed_news = []
    client = MongoClient('127.0.0.1', 27017)
    db = client['mail_news_db']
    main_news_collection = db['main_news']
    for link_url in news_links:
        response = requests.get(link_url)
        if response.status_code == 200:
            news_item = {}
            news_dom = html.fromstring(response.text)
            news_date_string = news_dom.xpath('//span[contains(@class, "note__text")]/@datetime')[0]
            news_date = datetime.datetime.strptime(news_date_string, '%Y-%m-%dT%H:%M:%S+03:00').strftime('%d.%m.%Y %H:%M')
            news_origin = news_dom.xpath('//a[@class="link color_gray breadcrumbs__link"]/span[@class="link__text"]/text()')[0]
            news_title = news_dom.xpath('//h1[@class="hdr__inner"]/text()')[0]
            news_item["_id"] = int(link_url.split('/')[-2])
            news_item["date"] = news_date
            news_item["origin"] = news_origin
            news_item["title"] = news_title
            news_item["news_link"] = link_url
            # parsed_news.append(news_item)
            try:
                main_news_collection.insert_one(news_item)
            except DuplicateKeyError:
                # main_news_collection.update_one({'_id': news_item["_id"]}, {'$set': {'news_link': link_url}})
                pass
    # pprint(parsed_news, sort_dicts=False)
    for news in main_news_collection.find({}):
        pprint(news)


parse_from_email()

