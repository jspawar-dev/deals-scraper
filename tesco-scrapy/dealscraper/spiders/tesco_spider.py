import scrapy
from scrapy.loader import ItemLoader
from dealscraper.items import TescoItem


class TescoSpider(scrapy.Spider):
    name = 'tesco-spider'
    allowed_domains = ['tesco.com']
    start_urls = ['https://www.tesco.com/groceries/en-GB/promotions/all?page=1&count=48']

    def parse(self, response):

        # here we are looping through the products and extracting the name, price & url
        for product in response.css('div.styles__StyledVerticalTileWrapper-dvv1wj-0.dtCNPH'):

            loader = ItemLoader(item=TescoItem(), selector=product)
            loader.add_css('name', 'span.styled__Text-sc-1i711qa-1.xZAYu.ddsweb-link__text')
            loader.add_css('price', 'p.styled__StyledHeading-sc-119w3hf-2.jWPEtj.styled__Text-sc-8qlq5b-1.lnaeiZ.beans-price__text')
            loader.add_css('discount', 'p.text__StyledText-sc-1jpzi8m-0.dxeTiV.ddsweb-text.styled__ContentText-sc-1d7lp92-8.jJQEMH.ddsweb-value-bar__content-text')
            loader.add_css('link', 'a.styled__Anchor-sc-1i711qa-0.hXcydL.ddsweb-link__anchor::attr(href)')

            yield loader.load_item()

        # Logic to handle the next page, currently stops at 50 pages to prevent sending too many requests to the supermarkets servers.
        next_page = response.css('a.pagination--button.prev-next[name="go-to-results-page"]').attrib['href']
        if 'page=51' not in next_page:
            next_page_url = 'https://www.tesco.com' + next_page
            yield response.follow(next_page_url, callback=self.parse)
