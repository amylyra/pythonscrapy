# -*- coding: utf-8 -*-
import json
import time
import re
from sephorareview.items import SephoraReviewItem
from sephorareview.items import SephoraReviewLoader

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector


class SephoraReview(CrawlSpider):
    name = "SephoraReview"
    allowed_domains = ["sephora.com"]
    start_urls = (
        'http://reviews.sephora.com/8723abredes/P248407/reviews.htm?format=embedded',
    )
    """
    start_urls = []
    with open("./sephora_cream_links.txt") as f:
        start_urls_list = f.readlines()

    for url in start_urls_list:
        start_urls.append('http://reviews.sephora.com'
                          '/8723abredes/{0}/reviews.htm'
                          '?format=embedded'.format(url.split(':')[-1].strip()))
    """
    rules = (
        Rule(LinkExtractor(allow=('.*?format=embedded&page=\d.*scrollToTop.*')),
                                  #'.*?format=embedded&page=\d.&scrollToTop=true'
             callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        time.sleep(1)
        hxs = Selector(response)
        url = response.url
        item = hxs.xpath('//html[@lang="en-US"]//body')
        review_rating_link = ('.//span[@itemprop="ratingValue"]/text()')
        number_reviews_link = ('.//span[@class="BVRRNumber"]/text()')
        review_link = ('.//div[starts-with(@class, '
                       '"BVRRContentReview BVRRDisplayContentReview")]')

        sku = re.search(r"P\d{6}", str(response.url)).group(0)
        page = re.search(r"page=\d+", url).group(0)

        new_item = SephoraReviewLoader(SephoraReviewItem(), item)
        reviews = item.xpath(review_link)
        new_item.add_value('sku', sku)
        new_item.add_value('url', url)
        new_item.add_xpath('ratings', review_rating_link)
        new_item.add_xpath('number_review', number_reviews_link)
        new_item.add_value('page', page)
        for r in reviews:
            new_item.add_value('reviews', self.Review(r))
        yield new_item.load_item()

    def Review(self, response):
        review = {}
        author_name_link = './/span[@itemprop="author"]/text()'
        location_link = './/span[@class="BVRRValue BVRRUserLocation"]/text()'
        skin_type_link = ('.//span[@class="BVRRValue '
                          'BVRRContextDataValue '
                          'BVRRContextDataValueskinType"]/text()')
        age_link = ('.//span[@class="BVRRValue '
                    'BVRRContextDataValue BVRRContextDataValueage"]/text()')
        rating_score_link = './/span[@itemprop="ratingValue"]/text()'
        title_link = './/span[@class="BVRRValue BVRRReviewTitle"]/text()'
        date_link = './/meta[@itemprop="datePublished"]/@content'
        text_link = './/span[@class="BVRRReviewText"]'
        review['author'] = response.xpath(author_name_link).extract_first()
        review['location'] = response.xpath(location_link).extract_first()
        review['skin_type_link'] = response.xpath(skin_type_link) \
            .extract_first()
        review['age_link'] = response.xpath(age_link).extract_first()
        review['rating_score'] = response.xpath(rating_score_link) \
            .extract_first()
        review['title'] = response.xpath(title_link).extract_first()
        review['date'] = response.xpath(date_link).extract()
        review['text'] = response.xpath(text_link).extract()
        return json.dumps(review, ensure_ascii=False)
