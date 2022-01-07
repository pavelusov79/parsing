# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapperItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    pr_declaration = scrapy.Field()
    pr_declaration_link = scrapy.Field()
    contractor = scrapy.Field()
    buildiner = scrapy.Field()
    main_photos = scrapy.Field()
    common_info = scrapy.Field()
    price = scrapy.Field()
    finish_term = scrapy.Field()
