# -*- coding: utf-8 -*-

# Scrapy settings for weipan_spider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#


BOT_NAME = 'weipan_spider'

SPIDER_MODULES = ['weipan_spider.spiders']
NEWSPIDER_MODULE = 'weipan_spider.spiders'
ITEM_PIPELINES = ['weipan_spider.pipelines.DownloadFilePipeline']

#dir to store downloaded ebooks
DOWNLOAD_DIR='./data/'

#input task file
INPUT_TASK_FILE='./task/task.txt'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'weipan_spider (+http://www.yourdomain.com)'
