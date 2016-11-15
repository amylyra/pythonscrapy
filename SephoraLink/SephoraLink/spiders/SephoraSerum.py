# -*- coding: utf-8 -*-
import time
import scrapy
from scrapy.selector import Selector
from selenium import webdriver


class SephoraSerumSpider(scrapy.Spider):
    name = "SephoraSerum"
    allowed_domains = ["sephora.com"]
    start_urls = (
        "http://www.sephora.com/facial-treatments?pageSize=-1",
        "http://www.sephora.com/facial-treatments?pageSize=-1&currentPage=2",
    )

    def parse(self, response):
        driver = webdriver.PhantomJS()
        driver.get(response.url)
        time.sleep(1)
        hxs = Selector(text=driver.page_source)
        links = hxs.xpath('//div[@class="SkuGrid"]//a/@href').extract()
        driver.close()
        with open("sephora_links.txt", 'ab') as f:
            for i in links:
                f.write(i + "\n")
