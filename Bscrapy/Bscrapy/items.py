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
    sku_out = MapCompose(strip_html, decoding, trim_whitespace)
    category_out = MapCompose(strip_html, decoding, trim_whitespace)
    brand_out = MapCompose(strip_html, decoding, trim_whitespace)
    name_out = MapCompose(strip_html, decoding, trim_whitespace)
    number_reviews_out = MapCompose(strip_html, decoding, trim_whitespace)
    review_rating_out = MapCompose(strip_html, decoding, trim_whitespace)
    price_out = MapCompose(strip_html, decoding, trim_whitespace)
    size_out = MapCompose(strip_html, decoding, trim_whitespace)
    ingredient_out = MapCompose(strip_html, decoding, trim_whitespace)
    percent_recommend = MapCompose(strip_html, decoding, trim_whitespace)
    pros = MapCompose(strip_html, decoding, trim_whitespace)
    cons = MapCompose(strip_html, decoding, trim_whitespace)
    best_uses = MapCompose(strip_html, decoding, trim_whitespace)
    reviews_out = MapCompose(strip_html, decoding, trim_whitespace)
    description_out = MapCompose(strip_html, decoding, trim_whitespace)
    details_out = MapCompose(strip_html, decoding, trim_whitespace)
    regimen_out = MapCompose(strip_html, decoding, trim_whitespace)


class BItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sku = Field(output_processor=TakeFirst())
    category = Field()
    brand = Field(output_processor=TakeFirst())
    name = Field(output_processor=TakeFirst())
    number_reviews = Field(output_processor=TakeFirst())
    percent_recommend = Field(output_processor=TakeFirst())
    pros = Field()
    cons = Field()
    best_uses = Field()
    review_rating = Field(output_processor=TakeFirst())
    price = Field(output_processor=TakeFirst())
    size = Field()
    ingredient = Field(output_processor=TakeFirst())
    reviews = Field()
    description = Field(output_processor=TakeFirst())
    details = Field(output_processor=TakeFirst())
    regimen = Field(output_processor=TakeFirst())
