# -*- coding: utf-8 -*-
import scrapy
import re


class ToolmaniaCrawlerSpider(scrapy.Spider):
    """A Class Spider to scrape data from toolmania.cl"""
    name = 'toolmania_crawler'
    allowed_domains = ['toolmania.cl']
    start_urls = [
        'https://www.toolmania.cl/rotomartillos-252'
        # url for whole category
        #'https://www.toolmania.cl/herramientas-electricas-248'
    ]

    def parse(self, response):
        """Process toolmania.cl products"""
        # define product url xpath
        XPATH_PRODUCT_LINK = "//a[@class='thumbnail product-thumbnail']/@href"
        products = response.xpath(XPATH_PRODUCT_LINK).extract()
        for product in products:
            url = product
            yield scrapy.Request(url, callback=self.parse_product)

        # follow pagination link
        XPATH_NEXT_PAGE = "//li[@class='page-item directional js-search-link']//a[@rel='next']/@href"
        next_page = response.xpath(XPATH_NEXT_PAGE).get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_product(self, response):
        # iterate over search results
        XPATH_SINGLE_PRODUCT = "//div[@class='single-product']"
        for product in response.xpath(XPATH_SINGLE_PRODUCT):
            # define xpaths for product details
            XPATH_PRODUCT_MODEL = ".//h5[@class='product-reference-single']/text()"
            XPATH_PRODUCT_NAME = ".//h1[@class='product-name-single mb-md-4']/text()"
            XPATH_PRODUCT_PRICE = ".//div[@class='product-prices margin__bottom__20']//span[@itemprop='price']/@content"

            product_model = product.xpath(XPATH_PRODUCT_MODEL).get()
            # clean product model
            product_model = re.sub('Código de referencia: ', '', product_model)
            # get current url
            product_link = response.url

            yield {
                'product_model': product_model,
                'product_name': product.xpath(XPATH_PRODUCT_NAME).extract(),
                'product_price': product.xpath(XPATH_PRODUCT_PRICE).extract(),
                'product_link': product_link,
            }
