# -*- coding: utf-8 -*-
from Bscrapy.items import BItem

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector


class ultaSpider(CrawlSpider):
    name = "ultaSpider"
    allowed_domains = ["ulta.com"]
    #allowed_domains = ["skinstore.com"]
    #allowed_domains = ["sephora.com"]

    start_urls = (
        "http://www.ulta.com",
        #"http://www.sephora.com/",
        #"http://www.skinstore.com",
    )

    rules = (
#        Rule(LinkExtractor(allow=('\/.*?\/.*\?productId\=.*')),
#             callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=(), canonicalize=True), follow=True),
    )

    def parse_item(self, response):
        hxs = Selector(response)
        items = hxs.xpath('//body')

        for item in items:
            new_item = BItem()
            new_item['name'] = item.xpath(
                '//h1[@itemprop="name"]/text()'
            ).extract_first()
            new_item['brand'] = item.xpath(
                '//h2[@itemprop="brand"]//a/text()'
            ).extract_first()
            new_item['ingredient'] = item.xpath(
                '//div[@class="product-catalog-content current-ingredients"]/text()'
            ).extract_first()

            yield new_item
#        return new_items
