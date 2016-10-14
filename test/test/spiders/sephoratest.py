# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor



class SephoratestSpider(CrawlSpider):
    name = "sephoratest"
    allowed_domains = ["sephora.com"]
    start_urls = (
        'http://www.sephora.com/',
        #'http://www.sephora.com/skincare/',
        #'http://www.sephora.com/skincare',
    )

    rules = (
        Rule(LinkExtractor(allow=(".+P\d{6}\D*")), callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=()), follow=True),
    )

    def parse_item(self, response):
        yield response.url
