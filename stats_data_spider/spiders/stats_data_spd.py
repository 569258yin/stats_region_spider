# -*- coding: utf-8 -*-

import re
import time
from ..settings import region_year, sleep_time
from scrapy import Request

from ..items import *

# 每个页面爬取的间隔时间，目前国家统计局的页面是有反爬保护的
url_prefix = r'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/%d/' % region_year

class StatsDataSpdSpider(scrapy.Spider):
    name = 'stats_data_spd'
    allowed_domains = ['stats.gov.cn']
    start_urls = [r'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/%d/index.html' % region_year]

    def parse(self, response):
        # 省级
        for node in response.xpath('//tr[@class="provincetr"]/td'):
            name = node.xpath('./a/text()').extract()[0]
            # 为了一个一个省的爬取全量，防止中间因为网站反爬而漏了部分数据，又要全量重爬一遍
            # if name != '湖北省':
            #     continue
            item = Item()
            item['parent_name'] = ''
            item['parent_code'] = '0'
            item['name'] = node.xpath('./a/text()').extract()[0]
            item['code'] = node.xpath('./a/@href').extract()[0].split('.')[0]+'0000000000'
            url = url_prefix + node.xpath('./a/@href').extract()[0]
            yield item
            time.sleep(sleep_time)
            yield Request(url, meta={'parent': item}, callback=self.parse2, )
        print("爬取完省份信息")

    def parse2(self, response):
        # 市级
        parent = response.meta['parent']
        for node in response.xpath('//tr[@class="citytr"]'):
            item = Item()
            item['parent_name'] = parent['name']
            item['parent_code'] = parent['code']
            item['name'] = node.xpath('./td[2]/a/text()').extract()[0]
            item['code'] = node.xpath('./td[1]/a/text()').extract()[0]
            url = url_prefix + node.xpath('./td[2]/a/@href').extract()[0]
            yield item
            time.sleep(sleep_time)
            yield Request(url, meta={'parent': item}, callback=self.parse3)
        print(r'爬取完%s省份的城市信息' % parent['name'])

    def parse3(self, response):
        # 区级
        parent = response.meta['parent']
        for node in response.xpath('//tr[@class="countytr"]'):
            item = Item()
            name = node.xpath('./td[2]/a/text()').extract()
            if name:
                item['parent_name'] = parent['name']
                item['parent_code'] = parent['code']
                item['name'] = node.xpath('./td[2]/a/text()').extract()[0]
                item['code'] = node.xpath('./td[1]/a/text()').extract()[0]
                url1 = response.request.url
                url1 = re.split('/\d+.html', url1)[0]

                url = url1 + '/' + node.xpath('./td[2]/a/@href').extract()[0]
                yield item
                time.sleep(sleep_time)
                yield Request(url, meta={'parent': item}, callback=self.parse4)
        print(r'爬取完%s城市的区县信息' % parent['name'])

    def parse4(self, response):
        # 街道
        parent = response.meta['parent']
        for node in response.xpath('//tr[@class="towntr"]'):
            item = Item()
            item['parent_name'] = parent['name']
            item['parent_code'] = parent['code']
            item['name'] = node.xpath('./td[2]/a/text()').extract()[0]
            item['code'] = node.xpath('./td[1]/a/text()').extract()[0]

            url1 = response.request.url
            url1 = re.split('/\d+.html', url1)[0]

            url = url1 + '/' + node.xpath('./td[2]/a/@href').extract()[0]

            yield item
            # time.sleep(sleep_time)
            # yield Request(url, callback=self.parse5)
        print(r'爬取完%s区县的街道信息' % parent['name'])

    # def parse5(self, response):
    #     # 居委会
    #     for node in response.xpath('//tr[@class="villagetr"]'):
    #         item = Item()
    #         item['name'] = node.xpath('./td[3]/text()').extract()[0]
    #         item['code'] = node.xpath('./td[1]/text()').extract()[0]
    #         item['code2'] = node.xpath('./td[2]/text()').extract()[0]
    #         yield item
