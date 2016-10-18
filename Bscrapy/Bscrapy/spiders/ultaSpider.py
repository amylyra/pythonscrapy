# -*- coding: utf-8 -*-
from Bscrapy.items import BItem

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
#from scrapy.selector import Selector
from selenium import webdriver


class ultaSpider(CrawlSpider):
    name = "ultaSpider"
    allowed_domains = ["ulta.com"]
    start_urls = (
        #"http://www.ulta.com",
        "http://www.ulta.com/microdelivery-exfoliating-wash?productId=xlsImpprod1490142",
    )

    rules = (
        Rule(LinkExtractor(allow=('.*?\/.*\?productId\=.*')),
             callback='parse_item', follow=True),
#        Rule(LinkExtractor(allow=()),
#             callback='parse_item', follow=False),
    )

    def __init__(self):
        super(ultaSpider, self).__init__()
        self.driver = webdriver.PhantomJS()

    def parse_item(self, response):
#        driver = webdriver.Chrome()
        driver = self.driver
        driver.get(response.url)
        while True:
            next = driver.find_element_by_xpath(
                '//span[@class="pr-page-next"]//a')
                #'//a[@data-pr-event="header-page-next-link"]')
            try:
                next.click()
                print("nextpage")
            except:
                break

        driver.close()
        return

#    def parse_link(self, response):
#        hxs = Selector(response)
#        items = hxs.xpath('//body')
#
#        for item in items:
#            new_item = BItem()
#            new_item['name'] = item.xpath(
#                '//h1[@itemprop="name"]/text()'
#            ).extract_first()
#            new_item['brand'] = item.xpath(
#                '//h2[@itemprop="brand"]//a/text()'
#            ).extract_first()
#            new_item['ingredient'] = item.xpath(
#                '//div[@class="product-catalog-content current-ingredients"]/text()'
#            ).extract_first()
##            new_item['price'] =
##            new_items.append(new_item)
#
#            yield new_item
#        return new_items
