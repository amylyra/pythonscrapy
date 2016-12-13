# -*- coding: utf-8 -*-
import re
import time
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector


class SephoraReviewSpider(CrawlSpider):
    name = "SephoraReview"
    allowed_domains = ["sephora.com"]
    #start_urls = (
    #    'http://reviews.sephora.com/8723abredes/P248407/reviews.htm?format=embedded',
    #)
    start_urls = []
    with open("./sephora_cream_links.txt") as f:
        start_urls_list = f.readlines()

    for url in start_urls_list:
        start_urls.append('http://reviews.sephora.com'
                          '/8723abredes/{0}/reviews.htm'
                          '?format=embedded'.format(url.split(':')[-1].strip()))
        b = re.search(r"page=\d+", a)

    rules = (
        Rule(LinkExtractor(allow=('.*?format=embedded&page=\d.*scrollToTop.*')),
                                  #'.*?format=embedded&page=\d.&scrollToTop=true'
             callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        time.sleep(1)
        print "LINK: ", response.url
        hxs = Selector()
