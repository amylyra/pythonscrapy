# -*- coding: utf-8 -*-
import re
import time
from Bscrapy.items import BItem
from Bscrapy.items import BItemLoader

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy.selector import Selector


class ultaSerumSpider(CrawlSpider):
    name = "ultaSerumSpider"
    allowed_domains = ["ulta.com"]
    start_urls = (
        #"http://www.ulta.com/",
        "http://www.ulta.com/skin-care-treatment-serums?N=27cs",
        "http://www.ulta.com/skin-care-treatment-serums?N=27cs&No=48&Nrpp=48",
        "http://www.ulta.com/skin-care-treatment-serums?N=27cs&No=96&Nrpp=48",
        "http://www.ulta.com/skin-care-treatment-serums?N=27cs&No=144&Nrpp=48",
        "http://www.ulta.com/skin-care-treatment-serums?N=27cs&No=192&Nrpp=48",
        "http://www.ulta.com/skin-care-treatment-serums?N=27cs&No=240&Nrpp=48",
        "http://www.ulta.com/skin-care-treatment-serums?N=27cs&No=288&Nrpp=48",
        "http://www.ulta.com/skin-care-treatment-serums?N=27cs&No=336&Nrpp=48",
        "http://www.ulta.com/skin-care-treatment-serums?N=27cs&No=384&Nrpp=48",
        "http://www.ulta.com/skin-care-treatment-serums?N=27cs&No=432&Nrpp=48",
        "http://www.ulta.com/skin-care-treatment-serums?N=27cs&No=480&Nrpp=48",
        "http://www.ulta.com/skin-care-treatment-serums?N=27cs&No=528&Nrpp=48",
        "http://www.ulta.com/skin-care-treatment-serums?N=27cs&No=576&Nrpp=48",
        "http://www.ulta.com/skin-care-treatment-serums?N=27cs&No=624&Nrpp=48",
        "http://www.ulta.com/skin-care-treatment-serums?N=27cs&No=672&Nrpp=48",
        "http://www.ulta.com/skin-care-treatment-serums?N=27cs&No=720&Nrpp=48",
    )

    rules = (
        Rule(LinkExtractor(allow=('.*?\/.*\?productId\=.*'),
                           restrict_xpaths='//a'),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=('.*?\?productId\=.*'),
                           restrict_xpaths='//a'),
             callback='parse_item', follow=False),
        #Rule(LinkExtractor(allow=(), restrict_xpaths='//a'),
        #     follow=False),
    )

    def __init__(self):
        super(ultaSerumSpider, self).__init__()
        self.driver = webdriver.PhantomJS()

    def parse_item(self, response):
        driver = webdriver.PhantomJS()
        #driver = self.driver
        driver.get(response.url)
        time.sleep(.5)
        item = Selector(response).xpath('//html[@lang="en"]')
        sku = item.xpath(' \
                    //span[@id="itemNumber"]/text()').extract_first()
        sku = re.search(r"\d{7}", str(sku))
        if sku:
            sku = sku.group(0)
        else:
            driver.close()
            yield None

        name_link = '//h1[@itemprop="name"]/text()'
        brand_link = '//meta[@property="og:brand"]/@content'
        number_reviews_link = '//meta[@id="meta_reviewCount"]/@content'
        review_rating_link = '//meta[@id="meta_rating"]/@content'
        price_link = '//meta[@property="product:price:amount"]/@content'
        category_link = ('//div[@class="makeup-breadcrumb"]//ul//li//a/text()')
        size = item.xpath(
                    '//span[@id="itemSize"]/text()').extract_first()
        if not size:
            size = item.xpath('//span[@id="skuDisplayName"]/text()') \
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
        percent_recommend_link = (('//p[@class="pr-snapshot-consensus-value pr-rounded"]'
                                   '//text()'))
        pros_link = (('//div[@class="pr-attribute-group pr-rounded pr-attribute-pros"]'
                 '//ul[@class="pr-attribute-value-list pr-snapshot-attribute-value-list"]'
                 '//li/text()'))
        cons_link = (('//div[@class="pr-attribute-group pr-rounded pr-attribute-cons"]'
                 '//ul[@class="pr-attribute-value-list pr-snapshot-attribute-value-list"]'
                 '//li/text()'))
        best_uses_link = (('//div[@class="pr-attribute-group pr-rounded pr-attribute-bestuses pr-last"]'
                     '//ul[@class="pr-attribute-value-list pr-snapshot-attribute-value-list"]'
                     '//li/text()'))
        reviews = item.xpath('//div[@class="pr-review-wrap"]')

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
        new_item.add_xpath('percent_recommend', percent_recommend_link)
        new_item.add_xpath('pros', pros_link)
        new_item.add_xpath('cons', cons_link)
        new_item.add_xpath('best_uses', best_uses_link)
        for r in reviews:
            new_item.add_value('reviews', self.Review(r))

        while True:
            try:
                wait = WebDriverWait(driver, 1)
                next_link = ('//span[@class="pr-page-next"]'
                             '//a[@data-pr-event="header-page-next-link"]')
                nextr_ele = EC.presence_of_element_located((By.XPATH, next_link))
                nextr = wait.until(nextr_ele)
                nextr.click()
                time.sleep(1)
                reviews = Selector(text=driver.page_source)
                reviews = reviews.xpath('//div[@class="pr-review-wrap"]')
            except:
                break

            for r in reviews:
                new_item.add_value('reviews', self.Review(r))

        driver.close()
        yield new_item.load_item()

    def Review(self, response):
        review = {}
        rating_base = './/div[@class="pr-review-rating-wrapper"]'
        author_base = ('.//div[@class="pr-review-author"]'
                       '//div[@class="pr-review-author-info-wrapper"]')
        main_base = './/div[@class="pr-review-main-wrapper"]'
        main_base_points = main_base + ('//div[@class="pr-review-points"]'
                                        '//div[@class="pr-review-points-attr-wrapper"]')
        main_base_text = main_base + '//div[@class="pr-review-text"]'
        main_base_footer = main_base + ('//div[@class="pr-review-footer"]'
                                        '//div[@class="pr-review-bottom-line-wrapper"]')

        date_link = rating_base + \
            '//div[@class="pr-review-author-date pr-rounded"]/text()'
        rating_title_link = rating_base + '//div[@class="pr-review-rating"]' + \
            '//p[@class="pr-review-rating-headline"]/text()'
        rating_score_link = rating_base + '//div[@class="pr-review-rating"]' + \
            '//span[@class="pr-rating pr-rounded"]/text()'
        author_name_link = author_base + \
            '//p[@class="pr-review-author-name"]//span/text()'
        author_type_link = author_base + \
            ('//div[@class="pr-review-author-affinity-wrapper"]'
             '//p[@class="pr-review-author-affinities"]//span/text()')
        author_location_link = author_base + \
            '//p[@class="pr-review-author-location"]//span/text()'
        review_pros_link = main_base_points + \
            ('//div[@class="pr-attribute-group pr-rounded pr-attribute-pros"]'
             '//div[@class="pr-attribute-value"]//ul//li/text()')
        review_cons_link = main_base_points + \
            ('//div[@class="pr-attribute-group pr-rounded pr-attribute-cons"]'
             '//div[@class="pr-attribute-value"]//ul//li/text()')
        review_bestuses_link = main_base_points + \
            ('//div[@class="pr-attribute-group pr-rounded pr-attribute-bestuses pr-last"]'
             '//div[@class="pr-attribute-value"]//ul//li/text()')
        review_text_link = main_base_text + '//p[@class="pr-comments"]/text()'
        review_recommend_link = main_base_footer + '//p/text()'
        review['date'] = response.xpath(date_link).extract()
        review['rating_title'] = response.xpath(rating_title_link).extract()
        review['rating_score'] = response.xpath(rating_score_link).extract()
        review['author_name'] = response.xpath(author_name_link).extract()
        review['author_type'] = response.xpath(author_type_link).extract()
        review['author_location'] = response.xpath(author_location_link).extract()
        review['review_cons'] = response.xpath(review_cons_link).extract()
        review['review_pros'] = response.xpath(review_pros_link).extract()
        review['review_bestuses'] = response.xpath(review_bestuses_link).extract()
        review['review_text'] = response.xpath(review_text_link).extract()
        review['review_recommend'] = response.xpath(review_recommend_link).extract()
        return review

