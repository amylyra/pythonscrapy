# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import hashlib


class SkinStorePipeline(object):
    def process_item(self, item, spider):
        return item


class DuplicateSkinStorePipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        try:
            base = item['sku'][0]
        except:
            return
        hash_id = hashlib.md5(base).hexdigest()
        if hash_id in self.ids_seen:
            raise DropItem("Duplicate item: %s" % base)
        else:
            self.ids_seen.add(hash_id)
            return item
