# -*- coding: utf-8 -*-
import scrapy
import logging
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from places_crawler.items import PlacesCrawlerItem

logger = logging.getLogger('mycustomlogger')

class LocuridinroSpider(scrapy.Spider):
    name = "locuridinro"
    allowed_domains = ["locuridinromania.ro"]

    start_urls = []
    for page in xrange(1,7):
        start_urls += [
            'http://www.locuridinromania.ro/categorie/locuri-de-vizitat-in-romania/locuri-din-judetul-alba/page/%s' % page,
            'http://www.locuridinromania.ro/categorie/locuri-de-vizitat-in-romania/locuri-din-judetul-arad/page/%s' % page
        ]

    def parse(self, response):
        responseSelector = Selector(response)

        for sel in responseSelector.xpath('//article'):
            item = PlacesCrawlerItem()
            name = sel.xpath('header/a/@title').extract()
            item['name'] = name[0] if name else ""

            link = sel.xpath('header/a/@href').extract()
            item['link'] = link
            item['short_decription'] = sel.xpath('div[@class="entry-content"]').extract()

            request = scrapy.Request(link[0], callback=self.parse_full_page)
            request.meta['item'] = item

            #
            yield request

    def parse_full_page(self, response):
        item = response.meta['item']
        logger.info('Visited %s', response.url)

        responseSelector = Selector(response)
        sel = responseSelector.xpath('//article')
        item['image'] = sel.xpath('div[@class="entry-content"]/h3/img/@data-lazy-src').extract()

        if item['image'] == []:
            item['image'] = sel.xpath('div[@class="entry-content"]/h3/img/@src').extract()
        if item['image'] == []:
            item['image'] = sel.xpath('div[@class="entry-content"]/p/img/@src').extract()
        if item['image'] == []:
            item['image'] = sel.xpath('div[@class="entry-content"]/p/a/img/@data-lazy-src').extract()
        if item['image'] == []:
            item['image'] = sel.xpath('div[@class="entry-content"]/h3/a/img/@data-lazy-src').extract()
        if item['image'] == []:
            item['image'] = sel.xpath('div[@class="entry-content"]/div/em/strong/a/img/@data-lazy-src').extract()

        item['map'] = sel.css('div[class=gm-map]').extract()

        return item
