import scrapy


class LinkedinSpider(scrapy.Spider):
    name = "linkedin"

    def start_requests(self):
        urls = [
            'https://www.linkedin.com/jobs/',
        ]

    def parse(self, response, **kwargs):
        pass
