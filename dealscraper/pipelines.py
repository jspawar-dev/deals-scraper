from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class DuplicatesPipeline:

    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['name'] in self.names_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.names_seen.add(adapter['name'])
            return item


class PriceNotNullPipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # check is price present
        if adapter.get('price'):

            adapter['price'] = float(adapter['price'])

            return item

        else:
            # drop item if no price
            raise DropItem(f"Missing price in {item}")


class NameCleaningPipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if 'Tesco' in adapter.get('name'):
            adapter['name'] = adapter['name'].replace('Tesco', '')

            return item


class DiscountCleaningPipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if 'Clubcard' in adapter.get('discount'):
            adapter['discount'] = adapter['discount'].strip('Clubcard')

            return item
