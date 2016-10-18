# -*- coding: utf-8 -*-
import re
from sephora.items import SephoraItem
from sephora.items import SephoraLoader
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy_splash import SplashRequest


class SephoraspiderSpider(Spider):
    name = "sephoraSpider"
    allowed_domains = ["sephora.com", "reviews.sephora.com"]
    prefix = 'http://www.sephora.com/P'
    start_urls = ["%s%s" % (prefix, str(i).rjust(6, '0'))
                  #for i in xrange(250, 999999)]
                  #for i in xrange(309307, 309311)]
                  for i in xrange(300000, 350000)]

    def parse(self, response):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse_link, endpoint='render.html',
                                args={'wait': 0.5,
                                      'har': 1,
                                      'html': 1})

    def parse_link(self, response):
        hxs = Selector(response)
        #test = hxs.xpath('//div[@class="u-bb u-bw3"]//a/@src')
        #if test == "/images/404.jpg":
        #    yield None
        print response.url
        sku = re.search(r"P\d{6}", str(response.url))
        if sku:
            sku = sku.group(0)
        else:
            yield None

        items = hxs.xpath('//body')
        category_link = '//li[@class= \
                            "Breadcrumb-item Breadcrumb-item--current" \
                        ]//a[@class="Breadcrumb-link"]/text()'
        brand_link = '//a[@class="u-h2 u-db u-linkComplex OneLinkNoTx"] \
                      //span[@class="u-linkComplexTarget"]/text()'
        name_link = '//h1[@class="u-fwb u-h3 u-mt0 u-mb1"]/text()'
        lastpage_link = '//span[@class="BVRRPageLink BVRRPageNumber"]//a/text()'
        number_reviews_link = '//div[@class="u-flex u-h6 u-ls1 u-lh1 u-fwb u-ttu"] \
                                //span[@class="u-linkComplexTarget"]/text()'
        review_rating_link = '//div[@class="u-mr1 StarRating u-relative u-oh"]/@seph-stars'
        number_loves_link = '//div[@class="u-flex u-h6 u-ls1 u-lh1 u-fwb u-ttu"] \
                        //span[@class="ng-binding"]/text()'
        price_link = '//div[@class="u-fwb u-h3 u-lhh"]//span[@class="ng-binding"]/text()'
        size_link = '//div[@class="Swatch-txt ng-binding"]/text()'
        ingredient_link = '//div[@id="ingredients"]//p/text()'

        for item in items:
            try:
                lastpage = item.xpath(lastpage_link).extract()[-1]
            except IndexError:
                lastpage = item.xpath(lastpage_link).extract()

            ingredient = item.xpath(ingredient_link).extract()
            ingredient = [i.decode() for i in ingredient]
            if ingredient:
                ingredient = ingredient[-1]
            else:
                ingredient = ingredient

            new_item = SephoraLoader(SephoraItem(), item)
            new_item.add_value('sku', sku)
            new_item.add_xpath('category', category_link)
            new_item.add_xpath('brand', brand_link)
            new_item.add_xpath('name', name_link)
            new_item.add_value('lastpage', lastpage)
            new_item.add_xpath('number_reviews', number_reviews_link)
            new_item.add_xpath('review_rating', review_rating_link)
            new_item.add_xpath('number_loves', number_loves_link)
            new_item.add_xpath('price', price_link)
            new_item.add_xpath('size', size_link)
            new_item.add_value('ingredient', ingredient)

            yield new_item.load_item()
