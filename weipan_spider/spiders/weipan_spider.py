#coding=UTF-8
__author__ = 'Administrator'
import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
import string
import re
import math
import urllib
from scrapy import log
#from ..items import Book #this is the way to import code from parent directory
from ..Weipan_Book import WeipanBook
import json
import urllib2
import os
#set default encoding
import sys
import time
#import pprint
from pprint import pprint

class WeipanSpider(scrapy.spider):
    name = "weipanspider"
    allowed_domains = ["weibo.com"]
    def parse(self,response):
        title=u'计算几何'
        title = urllib2.quote(title.encode(encoding='utf-8'))
        query_url='http://vdisk.weibo.com/search/?type=public&keyword='+title
        yield Request(url=query_url,callback=self.parse_search_results)

    def parse_search_results(self,response):
        try:
            html_txt = response.body.decode("utf-8","ignore")
            url = response.url
            hxs = Selector(text=html_txt)
            items = hxs.xpath('//table[@id="search_table"]/tbody/tr/')
            if items:
                for item in items:
                    book_title = item.xpath(".//div[@class='sort_name_detail']/a/@title")
                    book_url = item.xpath(".//div[@class='sort_name_detail']/a/@href")
                    book_size = item.xpath(".//td[@class='sort_size_m']/text()")
                    book_downloads = item.xpath(".//td[@class='sort_downnum_m']/text()")
                    book = WeipanBook()
                    book['title'] = book_title.extract()[0]
                    book['refer_url'] = book_url.extract()[0]
                    book['file_size'] = book_size.extract()[0]
                    book['downloads'] = book_downloads.extract()[0]
                    prefix_len =  'http://vdisk.weibo.com/s/'.__len__()
                    resource_id = book['refer_url'][prefix_len:]
                    file_url = self.get_file_download_url(resource_id)
                    book['local_file'] = resource_id
                    book['download_url'] = file_url
                    pprint(book)

        except Exception,e:
            raise

    def parse_file_download_url(self,response):
        content = json.loads(response.body, encoding='utf-8')
        if content:
            download_url=content['download_list'][1]
            print download_url