import scrapy


class GlassdoorSpider(scrapy.Spider):
    name = "glassdoor"

    def start_requests(self):
        urls = [
            'https://www.glassdoor.co.in/Job/',
        ]

    def parse(self, response, **kwargs):
        pass
