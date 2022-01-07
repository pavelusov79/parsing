from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from scrapper import settings
from scrapper.spiders.nashdom import NashdomSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(NashdomSpider)

    process.start()
