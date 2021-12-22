import json
import re
import scrapy
from scrapy.http import HtmlResponse


class InstagramSpiderSpider(scrapy.Spider):
    name = 'instagram_spider'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    inst_login_link = '	https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'paul.usov'
    inst_pwd = '#PWD_INSTAGRAM_BROWSER:10:1640136177:AZZQAOlu9HKfXc1HNzQwHrE+z5rtOmYfFAnv39Bj2AsnoJcC4EiRE+A0BA2/n/sbO8R6skLA+WZnFvjZ6R0leLO7FhpkC9fopZW3f5jmAuDKMIvYvj078lv8PALUvnl3n2Tu23wExoyThg=='
    users = ['fresh_fakt', 'factstop_']

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.inst_login_link,
                                 method='POST',
                                 callback=self.login,
                                 formdata={'username': self.inst_login, 'enc_password': self.inst_pwd},
                                 headers={'X-CSRFToken': csrf}
                                 )

    def login(self, response: HtmlResponse):
        print()

    def fetch_csrf_token(self, text):
        ''' Get csrf-token for auth '''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')