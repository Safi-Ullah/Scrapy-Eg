# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class ProductScrapperPipeline(object):
    def open_spider(self, spider):
        self.file = open('products.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, products, spider):
        line = json.dumps(dict(products)) + "\n"
        self.file.write(line)

        return products
