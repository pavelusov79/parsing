import scrapy
from scrapy.http import HtmlResponse
from labirint.items import LabirintItem


class LabirintSpiderSpider(scrapy.Spider):
    name = 'labirint_spider'
    allowed_domains = ['labirint.ru']

    def __init__(self, mark, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://www.labirint.ru/search/{mark}/?stype=0']

    def parse(self, response: HtmlResponse):
        pages = response.xpath('//a[@class="pagination-number__text"]/text()').getall()
        if pages:
            for page in range(1, int(pages[-1]) + 1):
                url = self.start_urls[0] + f'&page={page}'
                yield response.follow(url, callback=self.parse)

        links = response.xpath('//a[@class="product-title-link"]/@href').getall()
        for link in links:
            yield response.follow('https://www.labirint.ru' + link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        title = response.xpath('//div[@id="product-title"]/h1/text()').get()
        link = response.url
        author = response.xpath('//a[@data-event-label="author"]/text()').getall()
        price = response.xpath('//span[@class="buying-price-val-number"]/text() | //span[@class="buying-priceold-val-number"]/text()').get()
        discount_price = response.xpath('//span[@class="buying-pricenew-val-number"]/text()').get()
        book_rate = response.xpath('//div[@id="rate"]/text()').get()
        item = LabirintItem(title=title, link=link, author=author, price=price, discount_price=discount_price, book_rate=book_rate)
        yield item
