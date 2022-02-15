import scrapy


class IndeedSpider(scrapy.Spider):
    name = "indeed"

    def start_requests(self):
        urls = [
            'https://in.indeed.com/',
        ]

    def parse(self, response, **kwargs):
        pass
