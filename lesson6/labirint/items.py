# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LabirintItem(scrapy.Item):
    _id = scrapy.Field()
    link = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    price = scrapy.Field()
    discount_price = scrapy.Field()
    book_rate = scrapy.Field()

