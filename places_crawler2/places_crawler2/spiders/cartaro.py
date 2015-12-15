# -*- coding: utf-8 -*-
import scrapy
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from places_crawler2.items import PlacesCrawler2Item


class CartaroSpider(scrapy.Spider):
    name = "cartaro"
    allowed_domains = ["carta.ro"]
    start_urls = [
        u'http://carta.ro/obiective-turistice-romania/'
    ]

    def parse(self, response):
        responseSelector = Selector(response)

	print(response)
        for sel in responseSelector.xpath('//div[@itemtype="http://schema.org/TouristAttraction"]'):
            item = PlacesCrawler2Item()
            item['name'] = sel.xpath('a/h3').extract()[0]
            item['address'] = sel.xpath('div[@itemprop="address"]').extract()
            item['image'] = sel.xpath('div/img/@src').extract()
            item['short_decription'] = sel.xpath('div/span[@itemprop="description"]').extract()

            yield item
