# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import  Item,Field
class WeipanSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    filename = Field()
    upload_time = Field()
    owner = Field()
    filesize = Field()
    downloads = Field()
    pass
