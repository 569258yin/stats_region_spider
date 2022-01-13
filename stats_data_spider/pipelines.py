# -*- coding: utf-8 -*-

from pandas import DataFrame
from stats_data_spider.settings import engine, write_sql_table_name


class ScrapyStatisPipeline(object):

    def process_item(self, item, spider):
        new_col = ['code', 'name', 'parent_code', 'parent_name']
        df = DataFrame({
            'code': [item['code']],
            'name': [item['name']],
            'parent_code': [item['parent_code']],
            'parent_name': [item['parent_name']],
        }, columns=new_col)
        df.to_sql(write_sql_table_name, engine, if_exists='append', index=False)
        return item
