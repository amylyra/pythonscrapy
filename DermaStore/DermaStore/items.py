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


class DermaStoreLoader(ItemLoader):
    sku_out = MapCompose(strip_html, trim_whitespace)
    category_out = MapCompose(strip_html, trim_whitespace)
    brand_out = MapCompose(strip_html, trim_whitespace)
    name_out = MapCompose(strip_html, trim_whitespace)
    lastpage_out = MapCompose(strip_html, trim_whitespace)
    number_reviews_out = MapCompose(strip_html, trim_whitespace)
    review_rating_out = MapCompose(strip_html, trim_whitespace)
    number_loves_out = MapCompose(strip_html, trim_whitespace)
    price_out = MapCompose(strip_html,  trim_whitespace)
    size_out = MapCompose(strip_html, trim_whitespace)
    ingredient_out = MapCompose(strip_html, trim_whitespace)
    reviews_out = MapCompose(strip_html, trim_whitespace)
    five_star_reviews_out = MapCompose(strip_html, trim_whitespace)
    four_star_reviews_out = MapCompose(strip_html, trim_whitespace)
    three_star_reviews_out = MapCompose(strip_html, trim_whitespace)
    two_star_reviews_out = MapCompose(strip_html, trim_whitespace)
    one_star_reviews_out = MapCompose(strip_html, trim_whitespace)


class DermaStoreItem(Item):
    @classmethod
    def from_dict(kls, d):
        il = DermaStoreLoader(item=kls())
        for name, value in d.iteritems():
            try:
                il.add_value(name, value)
            except KeyError:
                pass
        return il.load_item()

    sku = Field(output_processor=TakeFirst())
    category = Field()
    brand = Field(output_processor=TakeFirst())
    name = Field(output_processor=TakeFirst())
    lastpage = Field(output_processor=TakeFirst())
    number_reviews = Field(output_processor=TakeFirst())
    review_rating = Field(output_processor=TakeFirst())
    number_loves = Field(output_processor=TakeFirst())
    price = Field(output_processor=TakeFirst())
    size = Field(output_processor=TakeFirst())
    ingredient = Field()
    reviews = Field()
    five_star_reviews = Field(output_processor=TakeFirst())
    four_star_reviews = Field(output_processor=TakeFirst())
    three_star_reviews = Field(output_processor=TakeFirst())
    two_star_reviews = Field(output_processor=TakeFirst())
    one_star_reviews = Field(output_processor=TakeFirst())

