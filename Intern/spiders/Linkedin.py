import json
import os
import dateparser
import html2text
import re
import scrapy
import requests
from Intern.Intern.items import InternItem
from scrapy.crawler import CrawlerProcess


def next_page(response):
    items = InternItem()

    items['companyLogo'] = response.css(".artdeco-entity-image--square-5").xpath(
        "@data-delayed-url").extract_first().strip()
    items['companyName'] = response.css(".topcard__flavor--black-link::text").extract_first().strip()
    items['postTitle'] = response.css(".topcard__title::text").extract_first().strip()
    items['jobTitle'] = response.css(".topcard__title::text").extract_first().strip()
    items['jobLocation'] = response.css(".topcard__flavor--bullet::text").extract_first().strip()
    items['lastUpdated'] = int(dateparser.parse(
        response.css(".topcard__flavor--metadata::text").extract_first().strip()).timestamp())
    items['jobDuration'] = "Nothing Here"
    items['aboutCompany'] = "Nothing Here"

    applyLink = response.css(".top-card-layout__cta--primary").xpath("@href").extract_first()
    if not applyLink:
        items['applyNowPage'] = response.css(".topcard__link").xpath("@href").extract_first().strip()
    else:
        items['applyNowPage'] = applyLink.strip()

    htmlParser = html2text.HTML2Text()
    htmlParser.ignore_links = False
    htmlParser.ignore_emphasis = True
    htmlParser.ul_item_mark = "\u2022 "
    htmlParser.strong_mark = ""
    htmlParser.emphasis_mark = ""
    htmlParser.strong_mark = ""

    rawDescription = "".join(response.css(".show-more-less-html__markup--clamp-after-5").extract()).strip()
    items['postDescription'] = htmlParser.handle(rawDescription)
    items['jobRequirement'] = items['postDescription']
    items['jobEligibility'] = items['postDescription']

    yield items


class LinkedinSpider(scrapy.Spider):
    name = "linkedin"

    def start_requests(self, jobKeyWord="Kotlin", location="India", numberOfPages=1):
        for pages in range(0, numberOfPages * 25, 25):
            yield scrapy.Request(
                url='https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?start={}&keywords={}&location={}'.format(
                    pages, jobKeyWord.strip().replace(" ", "%20"), location.strip().replace(" ", "%20")),
                callback=self.parse)

    def parse(self, response, **kwargs):
        dataEntityUrn = response.css(".base-card").xpath("@data-entity-urn").extract()
        dataSearchId = response.css(".base-card").xpath("@data-search-id").extract()
        dataTrackingId = response.css(".base-card").xpath("@data-tracking-id").extract()

        for i in range(0, len(dataEntityUrn)):
            currentJobPostingId = re.sub("urn:li:jobPosting:", "", dataEntityUrn[i])
            currentDataSearchId = dataSearchId[i]
            currentDataTrackingId = dataTrackingId[i]

            nextPageUrl = "https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}?refId={}%3D%3D&trackingId={}%3D%3D".format(
                currentJobPostingId, currentDataSearchId, currentDataTrackingId)

            yield scrapy.Request(url=nextPageUrl, callback=next_page)


def send_data():
    baseUrl = "https://aditya-intern-backend.herokuapp.com/job/all"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": "Bearer {ADD YOUR TOKEN HERE}"
    }
    jsonData = json.load(open('output.json'))
    response = requests.post(baseUrl, headers=headers, json=jsonData)

    if response.status_code == 200:
        print("Data Inserted Successfully")
    else:
        print("Something Went Wrong.")


if __name__ == "__main__":

    if os.path.exists("output.json"):
        os.remove("output.json")

    process = CrawlerProcess(settings={
        'FEED_URI': 'output.json',
        'FEED_FORMAT': 'json',
        'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'ROBOTSTXT_OBEY': 'True',
        'DOWNLOAD_DELAY': '1'
    })

    process.crawl(LinkedinSpider)
    process.start()
    send_data()
