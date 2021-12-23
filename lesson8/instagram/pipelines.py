# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class InstagramPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.instagram_db

    def process_item(self, item, spider):
        try:
            if item['subscriber_photo']:
                item['subscriber_photo'] = item['subscriber_photo'][0]['path']
        except:
            if item['following_photo']:
                item['following_photo'] = item['following_photo'][0]['path']
        collection = self.db[spider.name]
        try:
            collection.insert_one(item)
        except DuplicateKeyError:
            pass
        return item


class InstagramPhotoPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        try:
            if item['subscriber_photo_url']:
                yield scrapy.Request(item['subscriber_photo_url'])

        except:
            if item['following_photo_url']:
                yield scrapy.Request(item['following_photo_url'])

    def item_completed(self, results, item, info):
        try:
            if item['subscriber_photo_url']:
                item['subscriber_photo'] = [itm[1] for itm in results if itm[0]]
                return item
        except:
            if item['following_photo_url']:
                item['following_photo'] = [itm[1] for itm in results if itm[0]]
                return item

    def file_path(self, request, response=None, info=None, *, item=None):
        try:
            if item["subscriber_photo_url"]:
                return f'{item["username"]}/subscribers/{item["subscriber_username"]}.jpg'
        except:
            if item["following_photo_url"]:
                return f'{item["username"]}/following/{item["following_username"]}.jpg'
