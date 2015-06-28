# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.contrib.exporter import JsonItemExporter
import codecs
import json
import settings
import os.path
from scrapy import log
from pprint import pprint
from downloadfile import WeipanSpiderUtil
class WeipanSpiderPipeline(object):
    def process_item(self, item, spider):
        return item

class DownloadFilePipeline(object):
    def __init__(self):
        self.download_log = codecs.open('downloadlog.json', 'w', encoding='utf-8')
        self.util = WeipanSpiderUtil()
        self.fingerprints = dict()

    def is_ebook(self,item):
        if int(item['size']) < 100*1024*1024 and \
                (str(item['mime_type']).lower().find('pdf')>0 or\
                             str(item['mime_type']).lower().find('epub')>0 or\
                             str(item['mime_type']).lower().find('doc')>0):
            return True
        log.msg('invalid ebook '+item['title'],level=log.WARNING)
        return False

    def process_item(self, item, spider):
        if item['md5'] not in self.fingerprints:
            localfilename = settings.DOWNLOAD_DIR + item['title']
            if (not os.path.isfile(localfilename)) and self.is_ebook(item):
                self.util.download_file(item['url'],filename=localfilename)
            self.fingerprints[item['md5']] = item['title']
        else:
            item['copy_ref'] = self.fingerprints[item['md5']]
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.download_log.write(line)
        return item
