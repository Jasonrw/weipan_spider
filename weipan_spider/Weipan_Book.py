# -*- coding: utf-8 -*-
#check in
__author__ = 'Min'
import scrapy
from scrapy.item import  Item,Field

class WeipanBook(scrapy.Item):
    title = Field()
    refer_url = Field()
    download_url = Field()
    local_file = Field()
    file_size = Field()
    downloads = Field()
