import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class ScrapperPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.nashdom_vl_db

    def process_item(self, item, spider):
        return item


class ScrapperPhotoPipeline(ImagesPipeline):
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
        pass
        # return f'{item["_id"]}/{request.url.split("/")[-1]}'
