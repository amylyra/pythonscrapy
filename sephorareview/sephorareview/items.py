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
from util import strip_html, trim_whitespace


class SephoraReviewLoader(ItemLoader):
    sku_out = MapCompose(strip_html, trim_whitespace)
    url_out = MapCompose(strip_html, trim_whitespace)
    ratings_out = MapCompose(strip_html, trim_whitespace)
    number_review_out = MapCompose(strip_html, trim_whitespace)
    page_out = MapCompose(strip_html, trim_whitespace)
    reviews_out = MapCompose(strip_html, trim_whitespace)


class SephoraReviewItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    @classmethod
    def from_dict(kls, d):
        il = SephoraReviewLoader(item=kls())
        for name, value in d.iteritems():
            try:
                il.add_value(name, value)
            except KeyError:
                pass
        return il.load_item()

    sku = Field(output_processor=TakeFirst())
    url = Field(output_processor=TakeFirst())
    ratings = Field()
    number_review = Field(output_processor=TakeFirst())
    page = Field(output_processor=TakeFirst)
    reviews = Field()
