# -*- coding: utf-8 -*-
import re
from Bscrapy.items import BItem
from Bscrapy.items import BItemLoader

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from selenium import webdriver
from scrapy.selector import Selector


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
        self.driver.get(response.url)
        items = Selector(response).xpath('//html')
        sku = items.xpath(' \
                    //span[@id="itemNumber"]/text()').extract_first()
        sku = re.search(r"\d{7}", str(sku))
        print "SKU: ", sku
        if sku:
            sku = sku.group(0)
        else:
            yield None

        name_link = '//h1[@itemprop="name"]/text()'
        brand_link = '//meta[@property="og:brand"]/@content'
        number_reviews_link = '//meta[@id="meta_reviewCount"]/@content'
        review_rating_link = '//meta[@id="meta_rating"]/@content'
        price_link = '//meta[@property="product:price:amount"]/@content'
        category_link = ('//div[@class="makeup-breadcrumb"]//ul//li//a/text()')
        size = items.xpath(
                    '//span[@id="itemSize"]/text()').extract_first()
        if not size:
            size = items.xpath('//span[@id="skuDisplayName"]/text()') \
                        .extract_first()
        if size:
            size = size.strip()

        ingredient_link = ('//div[@class="product-catalog-content '
                           'current-ingredients"]/text()')
        description_link = '//meta[@property="og:description"]/@content'
        details_link = ('//div[@class="product-catalog-content '
                        'current-longDescription"]/text()')
        regimen_link = ('//div[@class="product-catalog-content '
                        'current-directions"]/text()')
        reviews_link = '//div[@class="pr-review-wrap"]'

        for item in items:
            new_item = BItemLoader(BItem(), item)
            new_item.add_value('sku', sku)
            new_item.add_xpath('name', name_link)
            new_item.add_xpath('brand', brand_link)
            new_item.add_xpath('number_reviews', number_reviews_link)
            new_item.add_xpath('review_rating', review_rating_link)
            new_item.add_xpath('price', price_link)
            new_item.add_xpath('category', category_link)
            new_item.add_value('size', size)
            new_item.add_xpath('ingredient', ingredient_link)
            new_item.add_xpath('description', description_link)
            new_item.add_xpath('details', details_link)
            new_item.add_xpath('regimen', regimen_link)
            #new_item.add_xpath('reviews', reviews_link)

            #while True:
            #    next = self.driver.find_element_by_xpath(
            #        '//a[@data-pr-event="header-page-next-link"]')
            #    try:
            #        next.click()
            #    except:
            #        break
            #    new_item.add_xpath('reviews', reviews_link)
            yield new_item.load_item()
        self.driver.close()


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
