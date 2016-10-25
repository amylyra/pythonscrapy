import re
import time
from sephora.items import SephoraItem
from sephora.items import SephoraLoader
from sephora.util import trim_whitespace

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class sephoraSpider(CrawlSpider):
    name = "sephoraSpider"
    allowed_domains = ["sephora.com", "reviews.sephora.com"]
    start_urls = (
        'http://www.sephora.com/',
        #'http://www.sephora.com/skincare/',
        #'http://www.sephora.com/black-tea-age-delay-cream-P217512',
    )

    rules = (
        Rule(LinkExtractor(allow=(".+P\d{6}\D*")), callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=(),
                           deny=("t5\/.+",
                                 "profile.+",
                                 "gallery.+",
                                 "stores.+",
                                 "storelist.+",
                                 "search.+"),
                           deny_domains=["jobs", "community"]),
             follow=True),
    )

    def parse_item(self, response):
        driver = webdriver.PhantomJS()
        driver.get(response.url)
        time.sleep(1)
        hxs = Selector(text=driver.page_source)
        sku = re.search(r"P\d{6}", str(response.url))
        if sku:
            sku = sku.group(0)
        else:
            driver.close()
            yield None
        item = hxs.xpath('//html[@lang="en"]//body')
        category_link = ('.//li['
                         '@class="Breadcrumb-item Breadcrumb-item--current"]'
                         '//a[@class="Breadcrumb-link"]/text()')
        brand_link = ('.//a[@class="u-h2 u-db u-linkComplex OneLinkNoTx"]'
                      '//span[@class="u-linkComplexTarget"]/text()')
        name_link = ('.//h1[@class="u-fwb u-h3 u-mt0 u-mb1"]/text()')
        lastpage_link = ('.//span[@class="BVRRPageLink BVRRPageNumber"]'
                         '//a/text()')
        number_reviews_link = ('.//div[@class='
                               '"u-flex u-h6 u-ls1 u-lh1 u-fwb u-ttu"]'
                               '//span[@class="u-linkComplexTarget"]'
                               '/text()')
        review_rating_link = ('.//div'
                              '[@class="u-mr1 StarRating u-relative u-oh"]'
                              '/@seph-stars')
        number_loves_link = ('.//div'
                             '[@class="u-flex u-h6 u-ls1 u-lh1 u-fwb u-ttu"]'
                             '//span[@class="ng-binding"]/text()')
        price_link = ('.//div'
                      '[@class="u-fwb u-h3 u-lhh"]'
                      '//span[@class="ng-binding"]/text()')
        size_link = ('.//div[@class="Swatch-txt ng-binding"]/text()')
        ingredient_link = ('.//div[@id="ingredients"]//p/text()')
        reviews = item.xpath('.//div[@class='
                             '"BVRRDisplayContentBody"]'
                             '//div[starts-with(@class, '
                             '"BVRRContentReview '
                             'BVRRDisplayContentReview")]')
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
        #counter = 0
        for r in reviews:
        #    counter += 1
            new_item.add_value('reviews', self.Review(r))
        #    print "COUNTER: ", counter

        """
        while True:
            wait = WebDriverWait(driver, 20)
            next_link = ('.//span[@class="BV_Tracking'
                         'Tag_Review_Display_NextPage"]')
            nextr_ele = EC.presence_of_element_located((By.XPATH,
                                                        next_link))
            nextr = wait.until(nextr_ele)
            nextr.click()
            time.sleep(5)
            reviews = Selector(text=driver.page_source)
            reviews = reviews.xpath('//html[@lang="en"]//body')
            reviews = reviews.xpath('.//div[@class='
                                    '"BVRRDisplayContentBody"]'
                                    '//div[starts-with(@class, '
                                    '"BVRRContentReview '
                                    'BVRRDisplayContentReview")]')
            try:
                wait = WebDriverWait(driver, 1)
                next_link = ('.//span[@class="BV_Tracking'
                             'Tag_Review_Display_NextPage"]')
                nextr_ele = EC.presence_of_element_located((By.XPATH,
                                                            next_link))
                nextr = wait.until(nextr_ele)
                nextr.click()
                time.sleep(1)
                reviews = Selector(text=driver.page_source)
                reviews = reviews.xpath('//html[@lang="en"]//body')
                reviews = reviews.xpath('.//div[@class='
                                        '"BVRRDisplayContentBody"]'
                                        '//div[starts-with(@class, '
                                        '"BVRRContentReview '
                                        'BVRRDisplayContentReview")]')
            except:
                break
            print "REVIEWS: ", len(reviews)
            for r in reviews:
                counter += 0
                print "COUNTER: ", counter
                new_item.add_value('reviews', self.Review(r))
        """
        driver.close()
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
        return review
