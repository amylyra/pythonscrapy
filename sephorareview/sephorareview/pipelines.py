# -*- coding: utf-8 -*-

from scrapy.exceptions import DropItem
import hashlib
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DuplicateSephorareviewPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        base = "%s%s" % (''.join(item['sku']).encode('utf-8'),
                         ''.join(item['user']).encode('utf-8'))

        hash_id = hashlib.md5(base).hexdigest()

        if hash_id in self.ids_seen:
            raise DropItem("Duplicate name/url: %s" % base)

        else:
            self.ids_seen.add(hash_id)
            return item
