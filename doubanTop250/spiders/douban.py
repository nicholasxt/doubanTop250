# -*- coding: utf-8 -*-

import scrapy
from doubanTop250.items import Doubantop250Item


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        Movie_list = response.xpath('//div[@class="info"]')
        for each in Movie_list:
            item = Doubantop250Item()
            title = each.xpath('div[@class="hd"]/a/span/text()').extract()
            fullTitle = "".join(title)
            movieInfo = each.xpath('div[@class="bd"]/p/text()').extract()
            star = each.xpath('div[@class="bd"]/div[@class="star"]/span/text()').extract()[0]
            quote = each.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            if quote:
                quote = quote[0]
            else:
                quote = ''

            item['title'] = fullTitle.strip().replace(" ", "").replace("\n", "")
            item['movieInfo'] = ';'.join(movieInfo).strip().replace(" ", "").replace("\n", "")
            item['star'] = star
            item['quote'] = quote

            # 数据保存为TXT
            # f = open('douban.txt', 'a', encoding='utf-8')
            # f.write("title:" + item['title'] + ";")
            # f.write("movieInfo:" + item['movieInfo'] + ";")
            # f.write("star:" + item['star'] + ";")
            # f.write("quote:" + item['quote'])
            # f.write('\n')

            yield item

        # f.close()

        nextLink = response.xpath('//span[@class="next"]/link/@href').extract()
        if nextLink:
            nextLink = nextLink[0]
            yield scrapy.Request('https://movie.douban.com/top250' + nextLink, callback=self.parse)

        pass
