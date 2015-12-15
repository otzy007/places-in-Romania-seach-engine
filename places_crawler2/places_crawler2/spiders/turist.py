# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import scrapy
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from places_crawler2.items import PlacesCrawler2Item
import urlparse

class CartaroSpider(scrapy.Spider):
    name = "turist"
    allowed_domains = ["turistderomania.ro"]
    start_urls = []
    for page in xrange(1,14):
        start_urls += [
            u'http://www.turistderomania.ro/cele-mai-frumoase-1000-locuri-de-vizitat-in-romania/page/%s' % page
        ]

    def parse(self, response):
        responseSelector = Selector(response)

	print(response)
        for sel in responseSelector.xpath('//div[@class="post"]'):
            item = PlacesCrawler2Item()
            link = sel.xpath('h2/a/@href').extract()[0]
            item['link'] = self.remove_non_ascii_1(link)
            item['name'] = self.remove_non_ascii_1(sel.xpath('h2/a/@title').extract()[0])
            image = sel.xpath('a/img/@src').extract()
            item['image'] = self.remove_non_ascii_1(image[0]) if image else ""
            item['short_decription'] = self.remove_non_ascii_1(sel.xpath('div[@class="entry"]').extract()[0].encode("utf-8",errors="replace"))

            request = scrapy.Request(link, callback=self.parse_full_page)
            request.meta['item'] = item

            yield request

    def parse_full_page(self, response):
        item = response.meta['item']

        responseSelector = Selector(response)
        sel = responseSelector.xpath('//a[@class="colorbox-link"]')
        url = sel.xpath('@href').extract()[0]
        item['map'] = self.remove_non_ascii_1(url)
	parsed = urlparse.urlparse(url)
        geo = urlparse.parse_qs(parsed.query)['gps_location'][0].split(",")
        item['lat'] = geo[0]
        item['lon'] = geo[1]

        return item

    def remove_non_ascii_1(self, text):
        return ''.join(i for i in text if ord(i)<128)
