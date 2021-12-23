# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagramItem(scrapy.Item):
    _id = scrapy.Field()
    user_id = scrapy.Field()
    username = scrapy.Field()
    subscriber_user_id = scrapy.Field()
    following_user_id = scrapy.Field()
    subscriber_username = scrapy.Field()
    following_username = scrapy.Field()
    subscriber_photo = scrapy.Field()
    following_photo = scrapy.Field()
    subscriber_photo_url = scrapy.Field()
    following_photo_url = scrapy.Field()
