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


class BItemLoader(ItemLoader):
    sku_out = MapCompose(strip_html, trim_whitespace)
    #category_out = MapCompose(strip_html, trim_whitespace)
    brand_out = MapCompose(strip_html, trim_whitespace)
    name_out = MapCompose(strip_html, trim_whitespace)
    number_reviews_out = MapCompose(strip_html, trim_whitespace)
    review_rating_out = MapCompose(strip_html, trim_whitespace)
    price_out = MapCompose(strip_html, trim_whitespace)
    size_out = MapCompose(strip_html, trim_whitespace)
    ingredient_out = MapCompose(strip_html, trim_whitespace)
    reviews_out = MapCompose(strip_html, decoding, trim_whitespace)
    description_out = MapCompose(strip_html, trim_whitespace)
    details_out = MapCompose(strip_html, trim_whitespace)
    regimen_out = MapCompose(strip_html, trim_whitespace)
    benefit_link = MapCompose(strip_html, trim_whitespace)


class BItem(Item):
    # define the fields for your item here like:
    sku = Field(output_processor=TakeFirst())
    #category = Field()
    brand = Field(output_processor=TakeFirst())
    name = Field(output_processor=TakeFirst())
    number_reviews = Field(output_processor=TakeFirst())
    review_rating = Field(output_processor=TakeFirst())
    price = Field(output_processor=TakeFirst())
    size = Field()
    ingredient = Field()
    reviews = Field()
    description = Field()
    details = Field()
    regimen = Field()
    benefit = Field()
