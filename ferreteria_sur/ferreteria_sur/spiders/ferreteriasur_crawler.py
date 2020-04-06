# -*- coding: utf-8 -*-
import scrapy
import re


class FerreteriasurCrawlerSpider(scrapy.Spider):
    """A Class Spider to scrape data from ferreteriasur.cl"""
    name = 'ferreteriasur_crawler'
    allowed_domains = ['ferreteriasur.cl']
    start_urls = [
        'http://ferreteriasur.cl/producto/herramientas-y-maquinarias.html',
    ]

    def parse(self, response):
        """Process ferreteriasur.cl products"""
        products = response.xpath("//div[@class='product-item-info type1']")

        # iterate over search results
        for product in products:
            # define XPaths
            XPATH_PRODUCT_LINK = ".//a[@class='product-item-link']/@href"
            XPATH_PRODUCT_SKU = ".//div[@class='produc-sku']/text()"
            XPATH_PRODUCT_NAME = ".//a[@class='product-item-link']/text()"
            XPATH_PRODUCT_PRICE = ".//span[@class='price']/text()"
            XPATH_NEXT_PAGE = "//div[@class='pages']//a[@class='action  next']/@href"

            # store product result in variable
            raw_product_link = product.xpath(XPATH_PRODUCT_LINK).extract()
            raw_product_sku = product.xpath(XPATH_PRODUCT_SKU).extract()
            raw_product_name = product.xpath(XPATH_PRODUCT_NAME).extract()
            raw_product_price = product.xpath(XPATH_PRODUCT_PRICE).extract()

            # cleaning results
            product_link = ''.join(raw_product_link).strip(
            ) if raw_product_link else None
            product_sku = ''.join(raw_product_sku).strip(
            ) if raw_product_sku else None
            product_sku = product_sku.replace('SKU: ', '')
            product_name = ''.join(raw_product_name).strip(
            ) if raw_product_name else None
            product_price = ''.join(raw_product_price).strip(
            ) if raw_product_price else None
            # clean blank spaces, currency symbol $ and dot . from price
            product_price = re.sub(' |\$|\.', '', product_price)

            yield {
                'product_sku': product_sku,
                'product_name': product_name,
                'product_price': product_price,
                'product_link': product_link
            }

            # follow pagination link
            next_page = product.xpath(XPATH_NEXT_PAGE).get()
            if next_page:
                yield scrapy.Request(url=next_page, callback=self.parse)
