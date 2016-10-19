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
    sku = MapCompose(TakeFirst, strip_html, decoding, trim_whitespace)
    category = MapCompose(strip_html, decoding, trim_whitespace)
    brand = MapCompose(TakeFirst, strip_html, decoding, trim_whitespace)
    name = MapCompose(TakeFirst, strip_html, decoding, trim_whitespace)
    number_reviews = MapCompose(TakeFirst, strip_html, decoding, trim_whitespace)
    review_rating = MapCompose(TakeFirst, strip_html, decoding, trim_whitespace)
    price = MapCompose(TakeFirst, strip_html, decoding, trim_whitespace)
    size = MapCompose(TakeFirst, strip_html, decoding, trim_whitespace)
    ingredient = MapCompose(TakeFirst, strip_html, decoding, trim_whitespace)
    reviews = MapCompose(strip_html, decoding, trim_whitespace)
    description = MapCompose(TakeFirst, strip_html, decoding, trim_whitespace)
    details = MapCompose(TakeFirst, strip_html, decoding, trim_whitespace)
    regimen = MapCompose(TakeFirst, strip_html, decoding, trim_whitespace)


class BItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sku = Field()
    category = Field()
    brand = Field()
    name = Field()
    number_reviews = Field()
    review_rating = Field()
    price = Field()
    size = Field()
    ingredient = Field()
    reviews = Field()
    description = Field()
    details = Field()
    regimen = Field()


