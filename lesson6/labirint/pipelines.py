# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class LabirintPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.labirint_db

    def process_item(self, item, spider):
        item['author'] = ', '.join(item['author'])
        item['title'] = item['title'].split(':')[-1].strip()
        item['price'] = int(item['price'])
        if item['discount_price']:
            item['discount_price'] = int(item['discount_price'])
        item['book_rate'] = float(item['book_rate'])
        collection = self.db[spider.name]
        try:
            collection.insert_one(item)
        except DuplicateKeyError:
            pass
        return item
