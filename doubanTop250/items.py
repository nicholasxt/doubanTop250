# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Doubantop250Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    movieInfo = scrapy.Field()
    star = scrapy.Field()
    quote = scrapy.Field()

    def get_insert_sql(self):
        sql="insert into top250movies(title,movieInfo,star,quote) values (%s,%s,%s,%s)"
        params=(self['title'],self['movieInfo'],self['star'],self['quote'])
        return sql,params

    pass
