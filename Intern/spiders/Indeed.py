import scrapy


class IndeedSpider(scrapy.Spider):
    name = "indeed"

    def start_requests(self, jobKeyWord="Android Developer", location="India"):
        for pages in range(0, 100, 10):
            yield scrapy.Request(
                url='https://in.indeed.com/jobs?q={}&l={}&start={}&sort=date'.format(
                    jobKeyWord.strip().replace(" ", "%20"), location.strip().replace(" ", "%20"), pages),
                callback=self.parse)

    def parse(self, response, **kwargs):
        pass
