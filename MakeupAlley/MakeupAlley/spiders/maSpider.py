# -*- coding: utf-8 -*-
import json
import time
import scrapy
#from MakeupAlley.loginform import fill_login_form
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
       
        category = ('//a[@class="track_BreadCrumbs_Category"]/@href')
        brand = ('//a[@class="track_BreadCrumbs_Brand"]//span/text()')
        product = ('.//a[@class="track_BreadCrumbs_Brand"]//span/text()')
        
        print "LINK: ", response.url
    
        return
