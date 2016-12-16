# -*- coding: utf-8 -*-
import scrapy
import requests
from MakeupAlley.loginform import fill_login_form
from MakeupAlley.items import MakeupalleyItem

class MaspiderSpider(scrapy.Spider):
    name = "maSpider"
    allowed_domains = ["makeupalley.com"]
    start_urls = ['http://makeupalley.com/']

    def parse(self, response):
        pass
