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
from ..items import Book #this is the way to import code from parent directory
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
        try:
            html_txt = response.body.decode("utf-8","ignore")
            url = response.url
            hxs = Selector(text=html_txt)
        except Exception,e:
            raise