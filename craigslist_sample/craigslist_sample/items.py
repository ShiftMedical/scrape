# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class CraigslistItem(Item):
    title = Field()
    link = Field()
    loc = Field()
    id = Field()
    email = Field()
#    job_desc = Field()
    recruiter_notice = Field()
    services_notice = Field()
    comp = Field()
    job_type = Field()
    date_created = Field()
