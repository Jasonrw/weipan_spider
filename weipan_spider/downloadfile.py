# -*- coding: utf-8 -*-
#chekc in
__author__ = 'Min'
import urllib2
from scrapy.selector import Selector
from scrapy.http import Request
from pprint import pprint
from keepalive import HTTPHandler
import codecs
import json
from Weipan_Book import WeipanBook
from StringIO import StringIO
import gzip
from datetime import datetime, time
from scrapy import log
from resource_mgr import resource_mgr
import requests

class WeipanSpiderUtil:
    query_prefix='http://vdisk.weibo.com/search/?type=public&keyword='
    def get_utc_seconds(self):
        utcnow = datetime.utcnow()
        ep_time = datetime.strptime('19700101', "%Y%m%d")
        delta = utcnow - ep_time
        return int(delta.total_seconds())


    def make_basic_request(self,url):
        keepalive_handler = HTTPHandler()
        opener = urllib2.build_opener(keepalive_handler)
        urllib2.install_opener(opener)
        request = Request(url)
        request.add_header('Host', 'vdisk.weibo.com')
        request.add_header('Connection', 'keep-alive')
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36')
        request.add_header('Accept-Encoding','gzip, deflate, sdch')
        request.add_header('Accept-Language','en-US,en;q=0.8,zh-CN;q=0.6')
        return request

    def make_scrapy_basic_request(self,url):
        keepalive_handler = HTTPHandler()
        opener = urllib2.build_opener(keepalive_handler)
        urllib2.install_opener(opener)

        request = Request(url)
        request.add_header('Host', 'vdisk.weibo.com')
        request.add_header('Connection', 'keep-alive')
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36')
        request.add_header('Accept-Encoding','gzip, deflate, sdch')
        request.add_header('Accept-Language','en-US,en;q=0.8,zh-CN;q=0.6')
        return request

    def make_query_request(self,title):
        url = self.query_prefix+title
        request = self.make_basic_request(url)
        request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        return request

    def make_download_request(self,resource_id):
        #url = string.
        url='http://vdisk.weibo.com/api/weipan/fileopsStatCount?link='\
            +str(resource_id)+'&ops=download&_='+str(self.get_utc_seconds())
        print url
        request = self.make_basic_request(url)
        request.add_header('x-response-version', '2')
        request.add_header('X-Requested-With','XMLHttpRequest')
        request.add_header('Referer','http://vdisk.weibo.com/search/?type=public&keyword=%E8%AE%A1%E7%AE%97%E5%87%A0%E4%BD%95')
        request.add_header('Cookie','saeut=128.199.199.160.1423838665227899; SINAGLOBAL=611836786847.5616.1423838696977; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW6VS44SKDOE03F.DpSS6my5JpX5KMt; SUHB=0WGMgclYKdPFCr; UOR=www.thunderex.com,widget.weibo.com,login.sina.com.cn; CNZZDATA3212592=cnzz_eid%3D1230030116-1423837401-null%26ntime%3D1427547320; _s_tentry=-; Apache=2748549464158.714.1427550861344; ULV=1427550861361:9:7:4:2748549464158.714.1427550861344:1427513633822; __utmt=1; __utma=18712062.314646581.1423838697.1427513634.1427550862.10; __utmb=18712062.1.10.1427550862; __utmc=18712062; __utmz=18712062.1427513634.9.3.utmcsr=login.sina.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/crossdomain2.php')
        return request
        #time.
    def make_request(self,url):
        #keepalive_handler = HTTPHandler()
        #opener = urllib2.build_opener(keepalive_handler)
        #urllib2.install_opener(opener)
        #url='http://vdisk.weibo.com/api/weipan/fileopsStatCount?link=s-WAggO9Rbafb&ops=download&_=1427550931372'
        request = urllib2.Request(url)
        request.add_header('Host', 'vdisk.weibo.com')
        request.add_header('Connection', 'keep-alive')
        request.add_header('Accept','application/json, text/javascript, */*; q=0.01')
        request.add_header('x-response-version', '2')
        request.add_header('X-Requested-With','XMLHttpRequest')
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36')
        #request.add_header('Referer','http://vdisk.weibo.com/search/?type=public&keyword=%E8%AE%A1%E7%AE%97%E5%87%A0%E4%BD%95')
        request.add_header('Accept-Encoding','gzip, deflate, sdch')
        request.add_header('Accept-Language','en-US,en;q=0.8,zh-CN;q=0.6')
        cookie_str = resource_mgr.cookie_jar.get_cookie_str()
        request.add_header('Cookie',cookie_str)
        #request.add_header('Cookie','saeut=128.199.199.160.1423838665227899; SINAGLOBAL=611836786847.5616.1423838696977; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW6VS44SKDOE03F.DpSS6my5JpX5KMt; SUHB=0WGMgclYKdPFCr; UOR=www.thunderex.com,widget.weibo.com,login.sina.com.cn; CNZZDATA3212592=cnzz_eid%3D1230030116-1423837401-null%26ntime%3D1427547320; _s_tentry=-; Apache=2748549464158.714.1427550861344; ULV=1427550861361:9:7:4:2748549464158.714.1427550861344:1427513633822; __utmt=1; __utma=18712062.314646581.1423838697.1427513634.1427550862.10; __utmb=18712062.1.10.1427550862; __utmc=18712062; __utmz=18712062.1427513634.9.3.utmcsr=login.sina.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/crossdomain2.php')
        return request

    def get_file_download_url(self,resource_id):
        request = self.make_download_request(resource_id)
        response_content = self.get_response(request)
        content = json.loads(response_content,encoding='utf-8')
        if content:
            download_url=content['download_list'][1]
            return download_url
        return ''

    def download_file(self,url,filename=''):
        log.msg('Start to download '+filename+' url: '+url)
        r = requests.get(url, stream=True)
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        return filename

    def download_file_v1(self,url,filename=''):
        log.msg('Start to download '+filename+' url: '+url)
        download_request = self.make_request(url)
        #download_request.add_header()

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        #response = opener.open('http://www.bad.org.uk')
        #response = urllib2.urlopen(download_request)
        response = opener.open(download_request)
        start_time = datetime.now()
        filesize = 0
        if response:
            localfile = open(filename,'wb')
            while True:
                data = response.read()
                if not data:
                    break
                localfile.write(data)
                filesize += len(data)
            response.close()
            localfile.close()
        end_time = datetime.now()
        elapsed_secs = end_time - start_time
        summary = ' Size: '+str(filesize)+' time cost: '+str(elapsed_secs)
        log.msg('Complete download task: '+filename+summary+' url: '+url)

    def get_response(self, request):
        response = urllib2.urlopen(request)
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
            return data
        else:
            return response.read()

    def parse_search_list(self,htmltxt):
        htmltxt = htmltxt.decode('utf-8','ignore')
        hxs = Selector(text=htmltxt)
        items = hxs.xpath("//table[@id='search_table']/tbody/tr")

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

    def download_book(self,title):
        title = urllib2.quote(title.encode(encoding='utf-8'))
        request = self.make_query_request(title)
        htmlpage = self.get_response(request)
        self.parse_search_list(htmlpage)

    def test(self):
        print 'Hello World'

if __name__ == "__main__":
    print 'start test'
    spider = WeipanSpiderUtil()
    spider.download_book(u'计算几何')
    #spider.download_book('test')


    #print content
    #print content['download_list'][1]
    #print data
    #print data.decode('utf-8')
    #pprint(data)

'''
encoder = json.JSONEncoder(ensure_ascii=False)
data_encoded = encoder.encode(data)
decoder = json.JSONDecoder(encoding='utf-8')
data_decoded = decoder.decode(data)
pprint(data_encoded)
pprint(data_decoded)
'''

'''
        response = urllib2.urlopen(request)
#data = handler.read()
keepalive_handler.close_all()
if response.info().get('Content-Encoding') == 'gzip':
    print 'start to decoded gzipped content'
    buf = StringIO( response.read())
    f = gzip.GzipFile(fileobj=buf)
    data = f.read()
    content = json.loads(data,encoding='utf-8')
    download_url=content['download_list'][1]
    urllib.urlretrieve(download_url,'test.pdf')
'''

'''
query example:
GET http://vdisk.weibo.com/search/?type=public&keyword=%E8%AE%A1%E7%AE%97%E5%87%A0%E4%BD%95 HTTP/1.1
Host: vdisk.weibo.com
Connection: keep-alive
Cache-Control: max-age=0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36
Accept-Encoding: gzip, deflate, sdch
Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6
Cookie: feedNumTime5538783344=1427468165; saeut=128.199.199.160.1423838665227899; SINAGLOBAL=611836786847.5616.1423838696977; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW6VS44SKDOE03F.DpSS6my5JpX5KMt; SUHB=0WGMgclYKdPFCr; _s_tentry=h8.haval.cn; Apache=4544272106140.852.1427601211574; ULV=1427601211626:11:9:2:4544272106140.852.1427601211574:1427593985729; UOR=www.thunderex.com,widget.weibo.com,h8.haval.com.cn; CNZZDATA3212592=cnzz_eid%3D1230030116-1423837401-null%26ntime%3D1427601344; __utmt=1; __utma=18712062.314646581.1423838697.1427593986.1427602597.12; __utmb=18712062.1.10.1427602597; __utmc=18712062; __utmz=18712062.1427513634.9.3.utmcsr=login.sina.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/crossdomain2.php
'''