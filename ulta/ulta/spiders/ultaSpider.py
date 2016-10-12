# -*- coding: utf-8 -*-
import scrapy
#from ulta.items import BItem
#from scrapy.selector import Selector
from scrapy_splash import SplashRequest


class UltaspiderSpider(scrapy.Spider):
    name = "ultaSpider"
    allowed_domains = ["reviews.sephora.com"]
    start_urls = (
        'http://www.reviews.sepohra.com/',
    )

#    start_urls = ["http://www.dmoz.org/"]
#    allowed_domains = ["localhost"]
#    start_urls = ["http://www.dmoz.org"]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse,
                                endpoint='render.html',
                                args={'wait': 0.5,
                                      'har': 1,
                                      'html': 1,
                                     }
                                )

    def parse(self, response):
#        print(response.xpath('//body'))
#        print(response.css("title").extract())
#        print(response.data["har"])
#        print(response.data["har"]["log"]["pages"])
        print(response.xpath('//p[@class="price"]/text()').extract_first())
        print("PARSED", response.url)

#    def start_requests(self):
#        start_urls = (
##            'http://www.ulta.com/',
#            'http://www.ulta.com/fabulous-foaming-face-wash?productId=xlsImpprod6200623',
#        )
#        for url in start_urls:
#            yield SplashRequest(
#                url,
#                self.parse,
#                endpoint='render.json',
#                args={'har': 1, 'html': 1, }
#            )
#
#    def parse(self, response):
#        print(response.xpath('//h1[@itemprop="name"]/text()').extract_first())
#        hxs = Selector(response)
#        items = hxs.xpath('//body')
#
#        new_items = []
#        for item in items:
#            new_item = BItem()
#            new_item['name'] = item.xpath(
#                '//h1[@itemprop="name"]/text()'
#            ).extract_first()
#            new_item['brand'] = item.xpath(
#                '//h2[@itemprop="brand"]//a/text()'
#            ).extract_first()
#            new_items.append(new_item)
#        return new_items
