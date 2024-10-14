# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags

# removes currency symbols to clean the data before its stored.
def remove_currency(value):
    if not None:
        return value.replace('£', '').strip()
    else:
        return '0.00'

# the href link scraped does not include the domain. so here we complete the link before its stored.
def tesco_complete_link(value):
    return 'https://www.tesco.com' + value


# add remove_currency to price
# This allows us to create a an item which is like a python dictionary.
class TescoItem(scrapy.Item):
    name = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(remove_tags, remove_currency), output_processor=TakeFirst())
    discount = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    link = scrapy.Field(input_processor=MapCompose(remove_tags, tesco_complete_link), output_processor=TakeFirst())
