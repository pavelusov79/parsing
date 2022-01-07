import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from scrapper.items import ScrapperItem
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class NashdomSpider(scrapy.Spider):
    name = 'nashdom'
    allowed_domains = ['наш.дом.рф']
    start_urls = ['https://наш.дом.рф/сервисы/каталог-новостроек/список-объектов/список?objStatus=0&residentialBuildings=1&place=0-26&page=0&limit=100']

    def parse(self, response: HtmlResponse):
        next_link = response.xpath('//a[@class="pagination-item-next"]/@href').get()
        if next_link:
            yield response.follow(f'https://наш.дом.рф{next_link}', callback=self.parse)
        links = response.xpath('//a[contains(@class, "styles__Address-sc-")]')
        print(len(links))
        for link in links:
            yield response.follow(link, callback=self.parse_item)

    def parse_item(self, response: HtmlResponse):
        dom_id = response.xpath('//p[contains(@class, "styles__Id-sc-")]/text()').get().split(':')[-1]
        print()
