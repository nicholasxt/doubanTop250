# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from twisted.enterprise import adbapi

import pymysql.cursors

# 保存为json格式
class JsonPipeline(object):
    def __init__(self):
        self.file=open('douban.json','w',encoding='utf-8')

    def process_item(self,item,spider):
        line = json.dumps(dict(item),ensure_ascii=False)+'\n'
        self.file.write(line)
        return item

    def spider_closed(self,spider):
        self.file.close()


import csv
# 保存为csv格式
class CsvPipeline(object):
    def __init__(self):
        self.file=open('douban.csv','w',encoding='utf-8')
        self.writer = csv.writer(self.file)
        head = ["title", "movieInfo", "star", "quote"]
        self.writer.writerow(head)

    def process_item(self, item, spider):
        data = [item["title"],item["movieInfo"],item["star"],item["quote"]]
        self.writer.writerow(data)
        return item

    def close_spider(self,spider):
        self.file.close()


import pymysql
# 保存到mysql
class Doubantop250Pipeline(object):
    def __init__(self,dbpool):
        self.dbpool=dbpool

    @classmethod
    def from_settings(cls,settings):
        dbparams=dict(
            host=settings['MYSQL_HOST'],  # 读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool=adbapi.ConnectionPool('pymysql',**dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 爬取速度可能大于数据库存储的速度,异步操作
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handler_error, item, spider)

    def do_insert(self, cursor, item):
        sql, params = item.get_insert_sql()
        cursor.execute(sql, params)

    def handler_error(self, failure, item, spider):
        print('--------------database operation exception!!-----------------')
        print(failure)

