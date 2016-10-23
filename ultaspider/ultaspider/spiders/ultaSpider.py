# -*- coding: utf-8 -*-
import scrapy
import time
from selenium import webdriver

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.xlib.pydispatch import dispather

class UltaspiderSpider(CrawlSpider):
    name = "ultaSpider"
    allowed_domains = ["ulta.com"]
    #allowed_domains = ["sephora.com"]
    start_urls = (
        'http://www.ulta.com/skin-care?N=2707',
        #'http://www.sephora.com/',
    )

    def __init__(self):
        super(UltaspiderSpider, self).__init__()
        self.driver = webdriver.PhantomJS()

    rules = (
        #Rule(LinkExtractor(allow=()), follow=True, callback='parse_item'),
        Rule(LinkExtractor(allow=('.*?\/.*\?productId\=.*'),
                           restrict_xpaths='//a'),
             callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=('.*?\?productId\=.*'),
                           restrict_xpaths='//a'),
             callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=(), restrict_xpaths='//a'),
             follow=True),
    )


    def parse_item(self, response):
        #driver = webdriver.PhantomJS()
        time.sleep(0.5)
        print "LINK: ", response.url
        self.driver.get(response.url)
        #print "Xpath: ", response.xpath('//li[@class="cat-sub-nav"]//a/@href').extract()
        self.driver.close()
        pass

