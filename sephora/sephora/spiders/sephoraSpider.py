# -*- coding: utf-8 -*-
from sephora.items import SephoraItem
from sephora.items import SephoraLoader

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy_splash import SplashRequest


class SephoraspiderSpider(CrawlSpider):
    name = "sephoraSpider"
    allowed_domains = ["sephora.com", "reviews.sephora.com"]
    start_urls = (
        #'http://www.sephora.com/',
        'http://www.sephora.com/skincare/',
        #'http://www.sephora.com/black-tea-age-delay-cream-P217512',
    )

    rules = (
#        Rule(LinkExtractor(allow=(".+P\d{6}\D*", )),
        Rule(LinkExtractor(allow=(".+P\d{6}\D*")), callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=()), follow=True),
    )

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse_item, endpoint='render.html',
                                args={'wait': 0.5,
                                      'har': 1,
                                      'html': 1})

    def parse_item(self, response):
        print response.url
#        sku = response.url.split('-')[-1][:7]
#        hxs = Selector(response)
#        items = hxs.xpath('//body')
#        category_link = '//li[@class= \
#                            "Breadcrumb-item Breadcrumb-item--current" \
#                        ]//a[@class="Breadcrumb-link"]/text()'
#        brand_link = '//a[@class="u-h2 u-db u-linkComplex OneLinkNoTx"] \
#                      //span[@class="u-linkComplexTarget"]/text()'
#        name_link = '//h1[@class="u-fwb u-h3 u-mt0 u-mb1"]/text()'
#        lastpage_link = '//span[@class="BVRRPageLink BVRRPageNumber"]//a/text()'
#        number_reviews_link = '//div[@class="u-flex u-h6 u-ls1 u-lh1 u-fwb u-ttu"] \
#                                //span[@class="u-linkComplexTarget"]/text()'
#        review_rating_link = '//div[@class="u-mr1 StarRating u-relative u-oh"]/@seph-stars'
#        number_loves_link = '//div[@class="u-flex u-h6 u-ls1 u-lh1 u-fwb u-ttu"] \
#                        //span[@class="ng-binding"]/text()'
#        price_link = '//div[@class="u-fwb u-h3 u-lhh"]//span[@class="ng-binding"]/text()'
#        size_link = '//div[@class="Swatch-txt ng-binding"]/text()'
#        ingredient_link = '//div[@id="ingredients"]//p/text()'
#
#        for item in items:
#            try:
#                lastpage = item.xpath(lastpage_link).extract()[-1]
#            except IndexError:
#                lastpage = item.xpath(lastpage_link).extract()
#
#            ingredient = item.xpath(ingredient_link).extract()
#            ingredient = [i.decode() for i in ingredient]
#            if ingredient:
#                ingredient = ingredient[-1]
#            else:
#                ingredient = ingredient
#
#            new_item = SephoraLoader(SephoraItem(), item)
#            new_item.add_value('sku', sku)
#            new_item.add_xpath('category', category_link)
#            new_item.add_xpath('brand', brand_link)
#            new_item.add_xpath('name', name_link)
#            new_item.add_value('lastpage', lastpage)
#            new_item.add_xpath('number_reviews', number_reviews_link)
#            new_item.add_xpath('review_rating', review_rating_link)
#            new_item.add_xpath('number_loves', number_loves_link)
#            new_item.add_xpath('price', price_link)
#            new_item.add_xpath('size', size_link)
#            new_item.add_value('ingredient', ingredient)
#
#            yield new_item.load_item()
