import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class LeruamerlenPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.leroymerlin_db

    def process_item(self, item, spider):
        item['description'] = self.process_description(item)
        del item['desc_keys']
        del item['desc_values']
        item['images'] = [el['path'] for el in item['images']]
        collection = self.db[spider.name]
        try:
            collection.insert_one(item)
        except DuplicateKeyError:
            collection.update_one({'_id': item["_id"]}, {'$set': {'price': item['price']}})
        return item

    def process_description(self, item):
        return dict(zip(item['desc_keys'], item['desc_values']))


class LeruamerlenPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['images']:
            for img in item['images']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['images'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        return f'{item["_id"]}/{request.url.split("/")[-1]}'
