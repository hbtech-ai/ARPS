# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class HefeiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    time = scrapy.Field()
    address = scrapy.Field()
    major_character = scrapy.Field()
    organization = scrapy.Field()
    host = scrapy.Field()
    person_abstract = scrapy.Field()
    content = scrapy.Field()
    link = scrapy.Field()