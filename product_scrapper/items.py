# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductScrapperItem(scrapy.Item):
    # define the fields for your item here like:
    product_id = scrapy.Field()
    name = scrapy.Field()
    product_desc = scrapy.Field()
    url = scrapy.Field()
    colors = scrapy.Field()
    image_urls = scrapy.Field()
    product_price = scrapy.Field()
    product_care = scrapy.Field()
