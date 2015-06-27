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
from ..Weipan_Book import WeipanBook
from ..downloadfile import WeipanSpiderUtil
from ..items import DownloadItem
import json
import urllib2
import os
#set default encoding
import sys
import time
import codecs
import re
from pprint import pprint
from ..resource_mgr import resource_mgr
INPUT_TASK_FILE='./task/task.txt'

class WeipanSpider(scrapy.Spider):
    name = "weipanspider"
    allowed_domains = ["weibo.com"]
    start_urls = []
    spider_util = WeipanSpiderUtil()

    def __init__(self):
        log.msg('Start to initialize input task: '+INPUT_TASK_FILE)
        taskfile=codecs.open(INPUT_TASK_FILE,mode='r',encoding='utf-8')
        #taskfile=codecs.open(INPUT_TASK_FILE)
        query_list=taskfile.readlines()
        #query_list = [u'计算几何',u'算法导论']
        for query in query_list:
            query=query.strip('\n\r\s\t').encode('utf-8')
            title = urllib2.quote(query)
            query_url='http://vdisk.weibo.com/search/?type=public&keyword='+title
            self.start_urls.append(query_url)
        taskfile.close()

    def parse_cookie(self,headers):
        cookie_list = headers.getlist('Set-Cookie')
        for cookie_str in cookie_list:
            resource_mgr.cookie_jar.add_cookie_str(cookie_str)

    def parse(self,response):
        try:
            html_txt = response.body.decode("utf-8","ignore")
            sign = re.search("var SIGN = \'(.+)\';",html_txt).group(1)
            #print sign
            url = response.url
            self.parse_cookie(response.headers)
            hxs = Selector(text=html_txt)
            items = hxs.xpath('//table[@id="search_table"]/tbody/tr')
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
                    book['local_file'] = resource_id
                    #file_url = self.get_file_download_url(resource_id)
                    #book['download_url'] = file_url
                    #pprint(book)
                    request = self.make_resourceid_request(resource_id,sign)
                    yield request
        except Exception,e:
            raise

    def make_resourceid_request(self,resource_id, sign):
        url='http://vdisk.weibo.com/api/weipan/fileopsStatCount?link='\
            +str(resource_id)+'&ops=download&wpSign='+sign+'&_='+str(self.spider_util.get_utc_seconds())
        req_header = {'Host':'vdisk.weibo.com',
                   'Connection':'keep-alive',
                   'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
                   'Accept-Encoding':'gzip, deflate, sdch',
                   'Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6',
                   'x-response-version': '2',
                   'X-Requested-With':'XMLHttpRequest',
                   'Referer':'http://vdisk.weibo.com/search/?type=public&keyword=%E8%AE%A1%E7%AE%97%E5%87%A0%E4%BD%95',
                   }
        #return Request(url,callback=self.get_file_download_url,headers=req_header,cookies=resource_mgr.cookie_jar.cookies)
        print 'Send Request: '+url
        return Request(url,callback=self.get_file_download_url,headers=req_header)

    def get_file_download_url(self,response):
        content = json.loads(response.body,encoding='utf-8')
        self.parse_cookie(response.headers)

        if content and 'download_list' in content and len(content['download_list'])>1:
            download_url=content['download_list'][1]
            print 'Download Url: '+download_url
            item = DownloadItem()
            item['url'] = download_url
            item['title']=content['title']
            item['type']=content['type']
            item['size']=content['bytes']
            item['mime_type']=content['mime_type']
            item['modified']=content['modified']
            item['md5']=content['md5']
            item['count_download']=content['count_download']
            item['copy_ref']=content['copy_ref']
            yield item
            #return download_url
            #print 'Download url: ',download_url
            #print 'Filename: ',item['title']
        #return ''

    def parse_file_download_url(self,response):
        content = json.loads(response.body, encoding='utf-8')
        if content:
            download_url=content['download_list'][1]
            print download_url