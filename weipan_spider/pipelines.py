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

    def process_item(self, item, spider):
        if item['md5'] not in self.fingerprints:
            localfilename = settings.DOWNLOAD_DIR + item['copy_ref']
            if not os.path.isfile(localfilename):
                self.util.download_file(item['url'],filename=localfilename)
            self.fingerprints[item['md5']] = item['copy_ref']
        else:
            item['copy_ref'] = self.fingerprints[item['md5']]
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.download_log.write(line)
        return item
