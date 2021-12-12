from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leruamerlen import settings
from leruamerlen.spiders.LeroyMerlin import LeroymerlinSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroymerlinSpider, search='ламинат')

    process.start()
