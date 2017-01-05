# -*- coding: utf-8 -*-
import re import time from SkinStore.items import BItem from SkinStore.items import BItemLoader from SkinStore.util import trim_whitespace

from scrapy.spiders import CrawlSpider from scrapy.spiders import Rule from scrapy.linkextractors import LinkExtractor from selenium import webdriver from 
selenium.webdriver.support.ui import WebDriverWait from selenium.webdriver.support import expected_conditions as EC from selenium.webdriver.common.by import By from 
scrapy.selector import Selector


class ultaSpider(CrawlSpider):
    name = "SkinStoreSpider"
    allowed_domains = ["skinstore.com"]
    start_urls = (
        #"http://www.skinstore.com/",
        "http://www.skinstore.com/skin-care/lotions.list?pageNumber=1",
        "http://www.skinstore.com/skin-care/lotions.list?pageNumber=2",
        "http://www.skinstore.com/skin-care/moisturizers.list?pageNumber=1",
        "http://www.skinstore.com/skin-care/moisturizers.list?pageNumber=2",
        "http://www.skinstore.com/skin-care/moisturizers.list?pageNumber=3",
        "http://www.skinstore.com/skin-care/moisturizers.list?pageNumber=4",
        "http://www.skinstore.com/skin-care/moisturizers.list?pageNumber=5",
        "http://www.skinstore.com/skin-care/moisturizers.list?pageNumber=6",
        "http://www.skinstore.com/skin-care/moisturizers.list?pageNumber=7",
        "http://www.skinstore.com/skin-care/moisturizers.list?pageNumber=8",
        "http://www.skinstore.com/skin-care/moisturizers.list?pageNumber=9",
        "http://www.skinstore.com/skin-care/moisturizers.list?pageNumber=10",
        "http://www.skinstore.com/skin-care/moisturizers.list?pageNumber=11",
        "http://www.skinstore.com/skin-care/moisturizers.list?pageNumber=12",
        "http://www.skinstore.com/skin-care/moisturizers.list?pageNumber=13",
        "http://www.skinstore.com/skin-care/moisturizers.list?pageNumber=14",
        "http://www.skinstore.com/skin-care/moisturizers.list?pageNumber=15",
        "http://www.skinstore.com/skin-care/moisturizers.list?pageNumber=16",
        "http://www.skinstore.com/skin-care/balms.list",
        "http://www.skinstore.com/skin-care/oils.list?pageNumber=1",
        "http://www.skinstore.com/skin-care/oils.list?pageNumber=2",
    )

    rules = (
        Rule(LinkExtractor(allow=('.*\/\d{8}.*')),
             callback='parse_item', follow=False),
        #Rule(LinkExtractor(allow=(), deny_domains=["m"]),
        #     follow=True),
    )

#    def __init__(self):
#        super(ultaSpider, self).__init__() self.driver = webdriver.PhantomJS()

    def parse_item(self, response):
        with open('try.txt', 'a') as f:
            f.write(response.url + '\n')
        item = Selector(response).xpath('//html[@lang="en-us"]//body')
        sku = item.xpath(' \
                    //div[@class="product-title-wrap"]/@rel').extract_first()
        sku = re.search(r"\d{8}", str(sku))
        if sku:
            sku = sku.group(0)
        else:
            yield None

        name_link = '//h1[@class="product-title font-alpha"]/text()'
        brand_link = ('//div[@class="content"]//tr'
                      '[contains(.//th/text(), "Brand:")]//td')
        number_reviews_link = '//p[@class="reviews-number"]/text()'
        review_rating_link = '//p[@class="score"]/text()'
        price_link = '//span[@class="price"]/text()'
        #category_link = ('//div[@class="makeup-breadcrumb"]//ul//li//a/text()')
        ingredient_link = ('//div[@class="content"]//tr'
                           '[contains(.//th/text(), "Ingredients:")]//td')
        description_link = ('//div[@itemprop="description"]//p/text()')
        regimen_link = ('//div[@class="content"]//tr'
                        '[contains(.//th/text(), "Directions:")]//td')
        benefit_link = ('//div[@itemprop="description"]//ul//li/text()')
        size_link = ('//div[@class="content"]//tr'
                     '[contains(.//th/text(), "Volume:"]//li/text()')
        reviews = item.xpath('//div[@class="review-block"]')

        new_item = BItemLoader(BItem(), item)
        new_item.add_value('sku', sku)
        new_item.add_xpath('name', name_link)
        new_item.add_xpath('brand', brand_link)
        new_item.add_xpath('number_reviews', number_reviews_link)
        new_item.add_xpath('review_rating', review_rating_link)
        new_item.add_xpath('price', price_link)
        #new_item.add_xpath('category', category_link)
        try:
            new_item.add_xpath('size', size_link)
        except:
            pass
        new_item.add_xpath('ingredient', ingredient_link)
        new_item.add_xpath('description', description_link)
        new_item.add_xpath('regimen', regimen_link)
        new_item.add_xpath('benefit', benefit_link)
        for r in reviews:
            try:
                new_item.add_value('reviews', self.Review(r))
            except:
                break
        driver = webdriver.PhantomJS()
        driver.get(response.url)
        time.sleep(1)
        while True:
            try:
                wait = WebDriverWait(driver, 20)
                next_link = ('//a[@id="next-button"]//div[@class="active"]')
                nextr_ele = EC.presence_of_element_located((By.XPATH, next_link))
                nextr = wait.until(nextr_ele)
                nextr.click()
                time.sleep(2)
                reviews = Selector(text=driver.page_source)
                reviews = reviews.xpath('//html[@lang="en-us"]//body')
                reviews = reviews.xpath('//div[@class="review-block"]')
            except:
                break

            for r in reviews:
                new_item.add_value('reviews', self.Review(r))

        driver.close()
        yield new_item.load_item()
        #pass

    def Review(self, response):
        review = {}
        rating_title_link = './/h3[@class="product-review-title cf"]/text()'
        author_name_link = './/span[@class="product-review-author"]//span/text()'
        date_link = './/meta[@itemprop="datePublished"]/@content'
        rating_score_link = './/span[@class="rating-stars"]/@style'
        review_text_link = './/p[@itemprop="description"]/text()'
        date = response.xpath(date_link).extract_first()
        rating_title = response.xpath(rating_title_link).extract_first()
        rating_score = response.xpath(rating_score_link).extract_first().split(':')[-1]
        author_name = response.xpath(author_name_link).extract_first()
        review_text = response.xpath(review_text_link).extract_first()
        review['date'] = trim_whitespace(date)
        review['author_name'] = trim_whitespace(author_name)
        review['rating_title'] = trim_whitespace(rating_title)
        if rating_score:
            review['rating_score'] = trim_whitespace(rating_score)
        if review_text:
            review['review_text'] = trim_whitespace(review_text)
        return review

