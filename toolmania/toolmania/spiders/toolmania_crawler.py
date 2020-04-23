# -*- coding: utf-8 -*-
import scrapy
import re


class ToolmaniaCrawlerSpider(scrapy.Spider):
    """A Class Spider to scrape data from toolmania.cl"""
    name = 'toolmania_crawler'
    allowed_domains = ['toolmania.cl']
    start_urls = ['https://www.toolmania.cl/pulidoras-562']

    def parse(self, response):
        """Process toolmania.cl products"""
        products = response.css('div.product-list')

        for product in products:
            # obtain product brand
            brand = product.css('.product-manufacturer::text').get()
            url = product.css('.thumbnail::attr(href)').get()
            yield scrapy.Request(url, callback=self.parse_product, meta={'brand': brand})

        # follow pagination link
        XPATH_NEXT_PAGE = "//li[@class='page-item directional js-search-link']//a[@rel='next']/@href"
        next_page = response.xpath(XPATH_NEXT_PAGE).get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_product(self, response):
        """Get details from single product"""
        XPATH_SINGLE_PRODUCT = "//div[@class='single-product']"

        for product in response.xpath(XPATH_SINGLE_PRODUCT):
            # define xpaths for product details
            XPATH_PRODUCT_TYPE = "//li[@itemprop='itemListElement'][5]//span/text()"
            XPATH_PRODUCT_MODEL = ".//h5[@class='product-reference-single']/text()"
            XPATH_PRODUCT_NAME = ".//h1[@class='product-name-single mb-md-4']/text()"
            XPATH_PRODUCT_PRICE = ".//div[@class='product-prices margin__bottom__20']//span[@itemprop='price']/@content"
            XPATH_PRODUCT_STOCK = ".//div[@class='form-group col-12']//p[@id='product-quantities']/text()"

            # get and clean results
            product_type = product.xpath(XPATH_PRODUCT_TYPE).get()
            product_model = product.xpath(XPATH_PRODUCT_MODEL).get()
            product_model = re.sub('Código de referencia: ', '', product_model)
            product_price = product.xpath(XPATH_PRODUCT_PRICE).get()
            product_price = int(product_price)
            product_stock = product.xpath(XPATH_PRODUCT_STOCK).get()
            if product_stock:
                product_stock = int(product_stock.split()[0])
            else:
                product_stock = 0

            yield {
                'product_brand': response.meta['brand'].lower(),
                'product_model': product_model,
                'product_type': product_type,
                'product_price': product_price,
                'product_name': product.xpath(XPATH_PRODUCT_NAME).get(),
                'product_stock': product_stock,
                'product_link': response.url,
            }
