# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class Item(scrapy.Item):
    name = Field()
    code = Field()
    parent_name = Field()
    parent_code = Field()
