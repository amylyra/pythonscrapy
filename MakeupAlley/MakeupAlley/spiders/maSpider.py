# -*- coding: utf-8 -*-
import json
import time
import scrapy
#from MakeupAlley.loginform import fill_login_form
from MakeupAlley.items import MakeupalleyLoader
from MakeupAlley.items import MakeupalleyItem

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector


class MaspiderSpider(CrawlSpider):
    name = "maSpider"
    allowed_domains = ["makeupalley.com"]
    login_url = 'https://www.makeupalley.com/account/login.asp'
    start_urls = ('https://www.makeupalley.com/product/searching.asp/page=2/pagesize=15/CategoryId=7/SD=/SC=/',
                 )

    rules = (
        Rule(LinkExtractor(allow=('.*ItemId=\d.*')), 
             callback='parse_item', follow=True),
    )

    def start_requests(self):
        yield scrapy.Request(
                url=self.login_url, 
                callback=self.login_parse
                )

    def login_parse(self, response):
        # args, url, method = fill_login_form(response.url, reponse.body,
        #                                    self.login_user, self.login_pass)
        return scrapy.FormRequest.from_response(
            response, 
            formdata={'UserName': 'zaozaoyuan', 
                      'Password': 'provenaf'}, 
            callback=self.after_login
        )

    def after_login(self, response):
        if "you entered is invalid" in response.body: 
            self.log("RESPONSE FAILED!")
            return
        else:  
            self.log("SUCCESSFULLY LOGGED IN. START CRAWLING!")
            for url in self.start_urls:
                yield scrapy.Request(url, callback=self.parse)

    def parse_item(self, response):
        hxs = response.xpath('//main')
        url = reponse.url
       
        itemID = hxs.xpath('.//div[@id="ItemId"]/text()')
        itemID = re.search(r"\d{6}", str(itemID))
        if itemID: 
            itemID = itemID.group(0)
        else:
            yield None 

        category = response.xpath('//a[@class="track_BreadCrumbs_Category"]//span/text()').extract_first()
        brand = response.xpath('//a[@class="track_BreadCrumbs_Brand"]//span/text()').extract_first()

        product = hxs.xpath('.//div[@id="ProductName"]/text()').extract_first()
        review_rating = hxs.xpath('.//div[@class="product-review-stats tablet-divider"]//h3/text()').extract_first()
        number_review = hxs.xpath('.//div[@class="product-review-stats tablet-divider"]//p//span/text()').extract_first()
        #repurchase = ('//div[@class="product-review-stats tablet-divider"]//p/text()')#.extract()[2]
        #package_qual = ('//div[@class="product-review-stats tablet-divider"]//p/text()')#.extract()[4]
        repurchase = hxs.xpath('.//p[@class="pack-xs"]/text()').extract_first()
        package_qual = hxs.xpath('.//p[@class="price-xs"]/text()').extract_first()

        new_item = MakeupAlleyLoader(MakeupAlleyItem(), item)
        new_item.add_value('url', url)
        new_item.add_value('sku', itemID)
        new_item.add_value('category', category)
        new_item.add_value('brand', brand)
        new_item.add_value('review_rating', review_rating)
        new_item.add_value('number_review', number_review)
        new_item.add_value('repurchase', repurchase)
        new_item.add_value('package_qual', package_qual)

        print "LINK: ", response.url
        reviews = hxs.xpath('.//div[id="reviews-wrapper"]//div[@class="comments"]')
        for r in reviews:
            new_item.add_value('reviews', self.Review(r))

        yield new_item.load_item()
        

    def Review(self, response):
        review = {}
        author_name = response.xpath('.//div[@class="user-reviews"]//p//a//span/text()').extract_first()
        author_char = .response.xpath('.//div[@class="important"]//p/text()').extract()
        date = response.xpath('.//div[@class="date"]//p/text()').extract_first()
        review_rating = response.xpath('.//div[@class="lipies"]//span/@class').extract_first()
        review_rating = re.search(r"l-\d-\d", str(review_rating)).group(0)
        review_text = response.xpath('.//div[@class="break-word"]/text').extract_first()
        """
        skintype = ["Other", "Very Dry", "Dry", "Normal", "Combination", "Acne-prone", "Oily", "Very Oily", "Sensitive"] 
        skintone = ["Other", "Fair", "Fair-Medium", "Medium", "Olive", "Tan", "Medium Brown", "Dark", "Deep Dark"]
        skinundertone = ["Cool", "Neutral", "Not Sure", "Warm"]
        hairtype = ["Other", "Straight", "Wavy", "Curly", "Kinky", "Relaxed"]
        hairtexture = ["Other", "Fine", "Medium", "Coarse"]
        haircolor = ["Other", "Blond", "Brunette", "Black", "Brown", "Red", "Silver", "Grey"]
        eyecolor = ["Other", "Blue", "Brown", "Black", "Hazel", "Violet", "Green", "Gray"]
        """
        age = author_char[0]
        skintype = author_char[1].split(',')[0]
        skintone = author_char[1].split(',')[1]
        skinundertone = author_char[1].split(',')[2]
        hairtype = author_char[2].split(',')[0]
        hairtexture = author_char[2].split(',')[1]
        haircolor = author_char[2].split(',')[2]
        review['author'] = authoer_name
        review['date'] = date
        review['age'] = age
        review['skintype'] = skintype
        review['skintone'] = skintone
        review['skinundertone'] = skinundertone
        review['hairtype'] = hairtype
        review['hairtexture'] = hairtexture
        review['haircolor'] = haircolor
        review['eyecolor'] = eyecolor
        review['review_rating'] = review_rating
        review['review_text'] = review_text
        return json.dumps(review, ensure_ascii=False)
    
        return
