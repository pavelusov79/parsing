import scrapy
from scrapy.http import HtmlResponse
from leruamerlen.items import LeruamerlenItem
from scrapy.loader import ItemLoader


class LeroymerlinSpider(scrapy.Spider):
    name = 'LeroyMerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        next_link = response.xpath('//a[@data-qa-pagination-item="right"]/@href').get()
        if next_link:
            yield response.follow(f'https://leroymerlin.ru{next_link}', callback=self.parse)
        links = response.xpath('//a[@data-qa="product-name"]')
        for link in links:
            yield response.follow(link, callback=self.parse_item)

    def parse_item(self, response: HtmlResponse):
        loader = ItemLoader(item=LeruamerlenItem(), response=response)
        loader.add_xpath('_id', '//span[@itemprop="sku"]/@content')
        loader.add_xpath('item_name', '//h1/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('price', '//uc-pdp-price-view//span[@slot]/text()')
        loader.add_xpath('images', '//img[@slot="thumbs"]/@src')
        loader.add_xpath('desc_keys', '//dt[@class="def-list__term"]/text()')
        loader.add_xpath('desc_values', '//dd[@class="def-list__definition"]/text()')
        yield loader.load_item()

        # item_id = response.xpath('//span[@itemprop="sku"]/@content').get()
        # item_name = response.xpath('//h1/text()').get()
        # url = response.url
        # price = response.xpath('//uc-pdp-price-view//span[@slot]/text()').getall()
        # images = response.xpath('//img[@slot="thumbs"]/@src').getall()
        # desc_keys = response.xpath('//dt[@class="def-list__term"]/text()').getall()
        # desc_values = response.xpath('//dd[@class="def-list__definition"]/text()').getall()
        # item = LeruamerlenItem(_id=item_id, item_name=item_name, url=url, price=price, images=images, desc_keys=desc_keys, desc_values=desc_values)
        # yield item


