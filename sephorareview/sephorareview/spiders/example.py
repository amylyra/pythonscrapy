# -*- coding: utf-8 -*-
from sephorareview.items import SephorareviewItem
from sephorareview.items import SephoraReviewLoader

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector


class ExampleSpider(CrawlSpider):
    name = "example"
    allowed_domains = ["reviews.sephora.com"]
    start_urls = (
        'http://reviews.sepohra.com/',
        #'http://reviews.sephora.com/8723abredes/P409968/reviews.htm?format=embedded&page=1&scrollToTop=true',
    )

    rules = (
        Rule(LinkExtractor(allow=[r'8723abreades/\w+']), callback='parse_item', follow=True),
#        Rule(LinkExtractor(),
#             callback='parse_item',
#             follow=False
#             ),
#        Rule(LinkExtractor(allow=('\/8723abredes\/P\d+\/reviews\.htm\?format\=.*')),
#             callback='parse_item',
#             ),
#        Rule(LinkExtractor(allow=('\/8723abredes\/P\d+\/reviews\.htm\?format\=embedded&page=\d&scrollToTop\=true')),
#             callback='parse_item',
#             ),
    )

    def parse_item(self, response):
        print "response.url: ", response.url
        sku = response.url.split('/')[4]
        hxs = Selector(response)
        reviews = hxs.xpath('//div[starts-with(@class, \
                            "BVRRContentReview BVRRDisplayContentReview")]')

        user_link = './/span[@class="BVRRNickname"]/text()'
        skintype_link = './/span[@class="BVRRValue BVRRContextDataValue \
                            BVRRContextDataValuesk\
                            inType"]/text()'
        age_link = './/span[@class="BVRRValue BVRRContextDataValue \
                    BVRRContextDataValueage"]/text()'
        location_link = './/span[@class="BVRRValue BVRRUserLocation"]/text()'
        date_link = './/span[@class="BVRRValue BVRRReviewDate"]/text()'
        rating_link = './/span[@class="BVRRNumber BVRRRatingNumber"]/text()'
        title_link = './/span[@class="BVRRValue BVRRReviewTitle"]/text()'
        comment_link = './/span[@class="BVRRReviewText"]/text()'

        for review in reviews:
            new_review = SephoraReviewLoader(SephorareviewItem(),
                                             review)
            new_review.add_value('sku', sku)
            new_review.add_xpath('user', user_link)
            new_review.add_xpath('skintype', skintype_link)
            new_review.add_xpath('age', age_link)
            new_review.add_xpath('location', location_link)
            new_review.add_xpath('date', date_link)
            new_review.add_xpath('rating', rating_link)
            new_review.add_xpath('title', title_link)
            new_review.add_xpath('comment', comment_link)
            yield new_review.load_item()
