import scrapy


class AngellistSpider(scrapy.Spider):
    name = "angellist"

    def start_requests(self):
        urls = [
            'https://angel.co/',
        ]

    def parse(self, response, **kwargs):
        pass
