import dateparser
import html2text
import re
import scrapy
from ..items import InternItem


def next_page(response):
    companyLogo = response.css(".artdeco-entity-image--square-5").xpath("@data-delayed-url").extract_first().strip()
    companyName = response.css(".topcard__flavor--black-link::text").extract_first().strip()
    postTitle = response.css(".topcard__title::text").extract_first().strip()
    applyNowPage = response.css(".top-card-layout__cta--primary").xpath("@href").extract_first().strip()
    jobTitle = response.css(".topcard__title::text").extract_first().strip()
    jobDuration = "Nothing Here"
    jobLocation = response.css(".topcard__flavor--bullet::text").extract_first().strip()
    aboutCompany = "Nothing Here"
    lastUpdated = dateparser.parse(response.css(".topcard__flavor--metadata::text").extract_first().strip())
    rawDescription = "".join(response.css(".show-more-less-html__markup--clamp-after-5").extract()).strip()

    htmlParser = html2text.HTML2Text()
    htmlParser.ignore_links = False
    htmlParser.ignore_emphasis = True
    htmlParser.ul_item_mark = "\u2022 "
    htmlParser.strong_mark = ""
    htmlParser.emphasis_mark = ""
    htmlParser.strong_mark = ""

    postDescription = htmlParser.handle(rawDescription)
    jobRequirement = postDescription
    jobEligibility = postDescription

    items = InternItem(
        companyLogo=companyLogo,
        companyName=companyName,
        postTitle=postTitle,
        postDescription=postDescription,
        applyNowPage=applyNowPage,
        jobTitle=jobTitle,
        jobDuration=jobDuration,
        jobLocation=jobLocation,
        jobRequirement=jobRequirement,
        jobEligibility=jobEligibility,
        aboutCompany=aboutCompany,
        lastUpdated=lastUpdated,
    )
    yield items


class LinkedinSpider(scrapy.Spider):
    name = "linkedin"
    jobKeyWord = "Android Developer"
    location = "India"

    start_urls = [
        'https://www.linkedin.com/jobs/search/?keywords={}&location={}'.format(
            jobKeyWord.strip().replace(" ", "%20"), location.strip().replace(" ", "%20")),
    ]

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
