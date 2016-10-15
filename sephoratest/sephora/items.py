# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item
from scrapy.item import Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from util import strip_html, trim_whitespace, decoding


class SephoraLoader(ItemLoader):
    sku = MapCompose(strip_html, decoding, trim_whitespace)
    category = MapCompose(strip_html, decoding, trim_whitespace)
    brand = MapCompose(strip_html, decoding, trim_whitespace)
    name = MapCompose(strip_html, decoding, trim_whitespace)
    lastpage = MapCompose(strip_html, decoding, trim_whitespace)
    number_reviews = MapCompose(strip_html, decoding, trim_whitespace)
    review_rating = MapCompose(strip_html, decoding, trim_whitespace)
    number_loves = MapCompose(strip_html, decoding, trim_whitespace)
    price = MapCompose(strip_html, decoding, trim_whitespace)
    size = MapCompose(strip_html, decoding, trim_whitespace)
    ingredient = MapCompose(strip_html, decoding, trim_whitespace)


class SephoraItem(Item):
    @classmethod
    def from_dict(kls, d):
        il = SephoraLoader(item=kls())
        for name, value in d.iteritems():
            try:
                il.add_value(name, value)
            except KeyError:
                pass
        return il.load_item()

    sku = Field()
    category = Field()
    brand = Field()
    name = Field()
    lastpage = Field()
    number_reviews = Field()
    review_rating = Field()
    number_loves = Field()
    price = Field()
    size = Field()
    ingredient = Field()
