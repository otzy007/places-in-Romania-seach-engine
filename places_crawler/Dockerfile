FROM rabbit52/scrapy

RUN pip install ScrapyElasticSearch

COPY . /places_crawler

CMD cd places_crawler/; scrapy crawl locuridinro
