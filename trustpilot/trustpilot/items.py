# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TrustpilotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class TrustItem(scrapy.Item):
    stars = scrapy.Field()
    
    review_date = scrapy.Field()

    description = scrapy.Field()
    
    date_experience = scrapy.Field()