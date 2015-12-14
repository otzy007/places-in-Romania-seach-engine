# -*- coding: utf-8 -*-

# Scrapy settings for places_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

from scrapy import log

ITEM_PIPELINES = [
    'scrapyelasticsearch.scrapyelasticsearch.ElasticSearchPipeline',
]

DOWNLOAD_DELAY = 1

BOT_NAME = 'places_crawler'

SPIDER_MODULES = ['places_crawler.spiders']
NEWSPIDER_MODULE = 'places_crawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'places_crawler (+http://www.yourdomain.com)'

ELASTICSEARCH_SERVER = '192.168.0.103'
ELASTICSEARCH_PORT = 9200
ELASTICSEARCH_INDEX = 'places'
ELASTICSEARCH_TYPE = 'place'
ELASTICSEARCH_UNIQ_KEY = 'name'
ELASTICSEARCH_LOG_LEVEL= log.DEBUG
