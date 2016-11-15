import re
#import time
#from DermaStore.items import DermaStoreItem
#from DermaStore.items import DermaStoreLoader

from scrapy import Spider
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
#from selenium import webdriver
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By


class DermaStoreSpider(Spider):
    name = "DermaStoreSpider"
    allowed_domains = ["DermaStore.com"]
    # start_urls = [base_url + "/hydra-mat-emulsion-P393524?skuId=1694819&icid2=products"]
    start_urls = (

    )

    def parse(self, response):
        yield SplashRequest(response.url, self.parse_link, endpoint='render.html',
                            args={'wait': 2,
                                  'har': 1,
                                  'html': 1})

    def parse_link(self, response):
        #driver = webdriver.PhantomJS()
        #driver.get(response.url)
        #time.sleep(3)
        #hxs = Selector(text=driver.page_source)

        print response.url
        """
        hxs = Selector(response)
        sku = re.search(r"P\d{6}", str(response.url))
        sku = sku.group(0)

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
        five_star_reviews_l = ('.//div[starts-with(@class, "BVRRHistogramBarRow '
                               'BVRRHistogramBarRow5")]//span[@class='
                               '"BVRRHistAbsLabel"]/text()')
        four_star_reviews_l = ('.//div[starts-with(@class, "BVRRHistogramBarRow '
                               'BVRRHistogramBarRow4")]//span[@class='
                               '"BVRRHistAbsLabel"]/text()')
        three_star_reviews_l = ('.//div[starts-with(@class, "BVRRHistogramBarRow '
                                'BVRRHistogramBarRow3")]//span[@class='
                                '"BVRRHistAbsLabel"]/text()')
        two_star_reviews_l = ('.//div[starts-with(@class, "BVRRHistogramBarRow '
                              'BVRRHistogramBarRow2")]//span[@class='
                              '"BVRRHistAbsLabel"]/text()')
        one_star_reviews_l = ('.//div[starts-with(@class, "BVRRHistogramBarRow '
                              'BVRRHistogramBarRow1")]//span[@class='
                              '"BVRRHistAbsLabel"]/text()')
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
        ingredient = [i for i in ingredient]
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
        new_item.add_xpath('one_star_reviews', one_star_reviews_l)
        new_item.add_xpath('two_star_reviews', two_star_reviews_l)
        new_item.add_xpath('three_star_reviews', three_star_reviews_l)
        new_item.add_xpath('four_star_reviews', four_star_reviews_l)
        new_item.add_xpath('five_star_reviews', five_star_reviews_l)
        new_item.add_xpath('price', price_link)
        new_item.add_xpath('size', size_link)
        new_item.add_value('ingredient', ingredient)
        for r in reviews:
            new_item.add_value('reviews', self.Review(r))
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

            print "REVIEWS: ", len(reviews)
            try:
                wait = WebDriverWait(driver, 10)
                next_link = ('.//span[@class="BV_Tracking'
                             'Tag_Review_Display_NextPage"]')
                nextr_ele = EC.presence_of_element_located((By.XPATH,
                                                            next_link))
                nextr = wait.until(nextr_ele)
                nextr.click()
                time.sleep(3)
                reviews = Selector(text=driver.page_source)
                reviews = reviews.xpath('//html[@lang="en"]//body')
                reviews = reviews.xpath('.//div[@class='
                                        '"BVRRDisplayContentBody"]'
                                        '//div[starts-with(@class, '
                                        '"BVRRContentReview '
                                        'BVRRDisplayContentReview")]')
            except TimeoutException:
                break

            for r in reviews:
                new_item.add_value('reviews', self.Review(r))
        """
        #driver.close()
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
