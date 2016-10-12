# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector


class TestspiderSpider(CrawlSpider):
    name = "testSpider"
    allowed_domains = ["reviews.sephora.com"]
    start_urls = (
        'http://reviews.sephora.com/',
    )

    rules = (
        Rule(LinkExtractor(allow=[r'8723abredes.+']),
             callback='parse_item',
             follow=True),
    )

    def parse_item(self, response):
        print response.url
        pass
