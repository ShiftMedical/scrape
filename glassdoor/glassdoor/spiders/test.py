
import re
import scrapy
from Glassdoor.items import GlassdoorItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MySpider(CrawlSpider):
    name = "glass"
    allowed_domains = ["glassdoor.com"]
    start_urls = ["http://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=per+diem+nurse&sc.keyword=per+diem+nurse&locT=C&locId=1147401"]

    BASE_URL = 'http://www.glassdoor.com/'

    def parse_start_url(self, response):
        return self.parse_func(response)

    # RULES THAT DETERMINE WHICH LINKS ARE FOLLOWED ON THE SITE
    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="button next"]',)), callback="parse_func", follow=True),
    )

    #INITIAL FUNCTION THAT CALLS THE CRAIGSLIST SEARCH PAGE AND PARSES AND ITERATES THROUGH THE RESULTS
    #THIS FUNCTION ALSO USES THE LINK TRAVERSAL RULES TO MOVE THROUGH ALL OF THE RESULTS PAGES
    def parse_func(self, response):
        links = response.xpath('//a[@class="hdrlnk"]/@href').extract()
        for link in links:
            absolute_url = self.BASE_URL + link
            yield scrapy.Request(absolute_url, callback=self.parse_attr)

    #CALLBACK FUNCTION TO PARSE THE WEBSITE FOR EACH INDIVIDUAL POSTING
    def parse_attr(self, response):
        match = re.search(r"(\w+)\.html", response.url)
        if match:
            item_id = match.group(1)
            url = self.BASE_URL + "reply/sfo/hea/" + item_id

            item = GlassdoorItem()
            item["link"] = response.url
            item["loc"] = "".join(response.xpath("//span[@class='postingtitletext']/small/text()").extract())
            item["title"] = "".join(response.xpath("//span[@class='postingtitletext']//text()").extract())
            item["comp"] = "".join(response.xpath("//p[@class='attrgroup']/span/b/text()").extract()[0])
##            item["job_desc"] = "".join(response.xpath('//section[@id="postingbody"]/text()').extract())
            item["recruiter_notice"] = response.xpath('//ul[@class="notices"]/li[1]/text()').extract()[0]
            item["services_notice"] = response.xpath('//ul[@class="notices"]/li[2]/text()').extract()[0]
            item["job_type"] = response.xpath('//p[@class="attrgroup"]/span[2]/b/text()').extract()[0]
            item["date_created"] = response.xpath('//div[@class="postinginfos"]/p/time/text()')[0].extract()
            item["id"] = response.xpath('//p[@class="postinginfo"][1]/text()').extract()[0]
            return scrapy.Request(url, meta={'item': item}, callback=self.parse_contact)

            items.append(item)
            return items

    ## CALLBACK FUNCTION TO PULL THE E-MAIL ADDRESS FOR EACH POSTING (IF AVAILABLE)
    def parse_contact(self, response):
        item = response.meta['item']
        item["email"] = "".join(response.xpath("//div[@class='anonemail']//text()").extract())
        return item
