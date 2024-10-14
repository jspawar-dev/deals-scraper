from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import mysql.connector

# removes the word 'tesco' from items aswell as random white space.
# Makes the scraped items easier to read.
class DataCleanerPipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        name = adapter['name'].lower().replace('tesco', '').replace('&amp;', '&')
        adapter['name'] = name.strip().title()

        if 'Clubcard Price' in adapter['discount']:
            adapter['discount'] = adapter['discount'].split('Clubcard Price')[0].strip()

        return item

# looks for any duplicate items and removes them.
class DuplicatesPipeline:

    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if 'name' not in adapter:
            raise DropItem("Product name is required.")
        elif 'price' not in adapter:
            raise DropItem("Product price is required.")
        elif 'discount' not in adapter:
            raise DropItem("Product discount is required.")

        if adapter['name'] in self.names_seen:
            raise DropItem(f"Duplicate item found: {adapter['name']}")
        else:
            self.names_seen.add(adapter['name'])
            return item

# This connects to the database and stores all the items into a table once theyve all been processed and cleaned.
class SavingToMySQLPipeline(object):

    def __init__(self):
        self.create_database()
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='deal-scraper'
        )
        self.curr = self.conn.cursor()
        self.create_table()

    def create_database(self):
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234'
        )
        curr = conn.cursor()
        curr.execute("CREATE DATABASE IF NOT EXISTS `deal-scraper`")
        conn.close()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS shopping_list""")
        self.curr.execute("""DROP TABLE IF EXISTS products""")
        self.curr.execute("""
            CREATE TABLE products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name TEXT,
                price TEXT,
                discount TEXT,
                link TEXT,
                owner INT,
                FOREIGN KEY (owner) REFERENCES user(id)
            )
        """)

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        adapter = ItemAdapter(item)
        self.curr.execute("""
            INSERT INTO products (name, price, discount, link)
            VALUES (%s, %s, %s, %s)
        """, (
            adapter["name"],
            adapter["price"],
            adapter["discount"],
            adapter["link"]
        ))
        self.conn.commit()
