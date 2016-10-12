# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item
from scrapy.item import Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose
from util import strip_html, trim_whitespace
#from sephorareview.util import strip_html, trim_whitespace


class SephoraReviewLoader(ItemLoader):
    sku = Compose(strip_html, trim_whitespace)
    user = Compose(strip_html, trim_whitespace)
    skintype = Compose(strip_html, trim_whitespace)
    age = Compose(strip_html, trim_whitespace)
    location = Compose(strip_html, trim_whitespace)
    date = Compose(strip_html, trim_whitespace)
    rating = Compose(strip_html, trim_whitespace)
    title = Compose(strip_html, trim_whitespace)
    comment = Compose(strip_html, trim_whitespace)


class SephorareviewItem(Item):
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

    sku = Field()
    user = Field()
    skintype = Field()
    age = Field()
    location = Field()
    date = Field()
    rating = Field()
    title = Field()
    comment = Field()
