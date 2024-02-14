import scrapy

from dealscraper.itemloaders import TescoProductLoader
from dealscraper.items import TescoItem


class TescoSpider(scrapy.Spider):
    name = 'tesco-spider'
    allowed_domains = ['tesco.com']
    start_urls = ['https://www.tesco.com/groceries/en-GB/promotions/all?page=1']

    def parse(self, response):

        # here we are looping through the products and extracting the name, price & url
        products = response.css('div.styles__StyledVerticalTileWrapper-dvv1wj-0.dtCNPH')

        for product in products:
            # here we put the data returned into the format we want to output for our csv or json file
            item = TescoProductLoader(item=TescoItem(), selector=product)
            item.add_css('name', 'span.styled__Text-sc-1i711qa-1.xZAYu.ddsweb-link__text::text')
            item.add_css('price',
                         'p.styled__StyledHeading-sc-119w3hf-2.jWPEtj.styled__Text-sc-8qlq5b-1.lnaeiZ.beans'
                         '-price__text::text')
            item.add_css('discount', 'span.offer-text::text')
            yield item.load_item()

        # Logic to handle the next page
        next_page = response.css('a.pagination--button.prev-next[name="go-to-results-page"]').attrib['href']
        if 'page=51' not in next_page:
            next_page_url = 'https://www.tesco.com' + next_page
            yield response.follow(next_page_url, callback=self.parse)
