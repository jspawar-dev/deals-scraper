# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


def remove_currency(value):
    if not None:
        return value.replace('£', '').strip()
    else:
        return '0.00'


def tesco_complete_link(value):
    return 'https://www.tesco.com' + value


# add remove_currency to price
class TescoItem(scrapy.Item):
    name = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(remove_tags, remove_currency), output_processor=TakeFirst())
    discount = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    link = scrapy.Field(input_processor=MapCompose(remove_tags, tesco_complete_link), output_processor=TakeFirst())
