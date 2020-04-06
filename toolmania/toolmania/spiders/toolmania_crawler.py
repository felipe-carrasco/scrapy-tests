# -*- coding: utf-8 -*-
import scrapy
import re


class ToolmaniaCrawlerSpider(scrapy.Spider):
    """A Class Spider to scrape data from toolmania.cl"""
    name = 'toolmania_crawler'
    allowed_domains = ['toolmania.cl']
    start_urls = ['https://www.toolmania.cl/rotomartillos-252']

    def parse(self, response):
        """Process toolmania.cl products"""
        products = response.xpath(
            "//div[@class='col-6 col-md-4 col-lg-3 pt-4']")

        # iterate over search results
        for product in products:
            # define xpaths
            XPATH_PRODUCT_TYPE = "//h1[@class='page-title']/text()"
            XPATH_PRODUCT_BRAND = ".//h4[@class='product-manufacturer']/text()"
            XPATH_PRODUCT_NAME = ".//h2[@class='product-name']//a/text()"
            XPATH_PRODUCT_PRICE = ".//span[@class='price']/@content"
            XPATH_PRODUCT_LINK = ".//a[@class='thumbnail product-thumbnail']/@href"
            XPATH_NEXT_PAGE = "//li[@class='page-item directional js-search-link']//a[@rel='next']/@href"

            # store product result in variable
            raw_product_type = product.xpath(XPATH_PRODUCT_TYPE).extract()
            raw_product_brand = product.xpath(XPATH_PRODUCT_BRAND).extract()
            raw_product_name = product.xpath(XPATH_PRODUCT_NAME).extract()
            raw_product_price = product.xpath(XPATH_PRODUCT_PRICE).extract()
            raw_product_link = product.xpath(XPATH_PRODUCT_LINK).extract()

            # sanitize results
            product_type = raw_product_type
            product_brand = raw_product_brand
            product_name = raw_product_name
            product_price = raw_product_price
            product_link = raw_product_link

            yield {
                'product_type': raw_product_type,
                'product_brand': raw_product_brand,
                'product_name': raw_product_name,
                'product_price': raw_product_price,
                'product_link': raw_product_link
            }

            # follow pagination link
            next_page = product.xpath(XPATH_NEXT_PAGE).get()
            if next_page:
                yield scrapy.Request(url=next_page, callback=self.parse)
