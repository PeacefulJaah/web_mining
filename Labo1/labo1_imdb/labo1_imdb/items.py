# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Movie(scrapy.Item):
    rank = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()
    duration = scrapy.Field()
    certificate = scrapy.Field()
    rating = scrapy.Field()
    votes = scrapy.Field()
    url = scrapy.Field()
    poster_url = scrapy.Field()