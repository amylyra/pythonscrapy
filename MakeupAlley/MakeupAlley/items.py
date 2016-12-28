# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item
from scrapy.item import Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.loader.processors import TakeFirst
from util import strip_html, trim_whitespace, decoding


class MakeupalleyLoader(ItemLoader): 
    sku_out = MapCompose(strip_html, trim_whitespace) 
    url_out = MapCompose(strip_html, trim_whitespace) 
    page_out = MapCompose(strip_html, trim_whitespace) 
    category_out = MapCompose(strip_html, trim_whitespace) 
    brand_out = MapCompose(strip_html, trim_whitespace) 
    review_rating_out = MapCompose(strip_html, trim_whitespace) 
    number_review_out = MapCompose(strip_html, trim_whitespace)
    repurchase_out = MapCompose(strip_html, trim_whitespace) 
    package_qual_out = MapCompose(strip_html, trim_whitespace) 
    reviews_out = MapCompose(strip_html, trim_whitespace) 


class MakeupalleyItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sku = Field(output_processor=TakeFirst())
    url = Field(output_processor=TakeFirst())
    page = Field(output_processor=TakeFirst())
    category = Field(output_processor=TakeFirst())
    brand = Field(output_processor=TakeFirst())
    review_rating = Field(output_processor=TakeFirst())
    number_review = Field(output_processor=TakeFirst())
    repurchase = Field(output_processor=TakeFirst())
    package_qual = Field(output_processor=TakeFirst())
    reviews = Field()
