# -*- coding: utf-8 -*-
import scrapy
import re


class FerretekCrawlerSpider(scrapy.Spider):
    """A Class Spider to scrape data from herramientas.cl"""
    name = 'ferretek_crawler'
    allowed_domains = ['herramientas.cl']
    start_urls = [
        # línea herramientas completa
        'https://herramientas.cl/categorias/1040/dremel',
        'https://herramientas.cl/categorias/1015/estacionarias',
        'https://herramientas.cl/categorias/1090/herramientas-a-combustion',
        'https://herramientas.cl/categorias/1010/herramientas-electricas',
        'https://herramientas.cl/categorias/1020/herramientas-inalambricas',
        'https://herramientas.cl/categorias/1080/herramientas-manuales',
        'https://herramientas.cl/categorias/1030/instrumentos-de-medicion',
        'https://herramientas.cl/categorias/1052/linea-neumatica',
    ]

    def parse(self, response):
        """Process herramientas.cl (ferretek) products"""
        products = response.xpath("//div[@class='grilla grilla-dos']")

        # iterate over search results
        for product in products:
            # define the XPaths
            XPATH_PRODUCT_FAMILY = "//ul[@class='breadcrumb']//li[@class='active']/text()"
            XPATH_PRODUCT_NAME = ".//a[@class='nombreGrilla link']/text()"
            XPATH_PRODUCT_PRICE = ".//a[@class='valorGrilla link']/text()"
            # define alternative Xpath if product is on sale
            XPATH_PRODUCT_PRICE_SALE = ".//a[@class='valorGrilla link']//span[@class='conDescuento']/text()"
            XPATH_PRODUCT_BRAND = ".//a[@class='marca link']/span/text()"
            XPATH_PRODUCT_LINK = ".//a[@class='imgGrilla']/@href"
            XPATH_NEXT_PAGE = "//div[@class='cont100Centro paginador']//a[@class='paginate next']/@href"

            raw_product_family = product.xpath(XPATH_PRODUCT_FAMILY).extract()
            raw_product_name = product.xpath(XPATH_PRODUCT_NAME).extract()
            raw_product_price = product.xpath(XPATH_PRODUCT_PRICE).extract()
            # check if regular price is not available
            if raw_product_price:
                pass
            else:
                raw_product_price = product.xpath(
                    XPATH_PRODUCT_PRICE_SALE).extract()
            raw_product_brand = product.xpath(XPATH_PRODUCT_BRAND).extract()
            link = product.xpath(XPATH_PRODUCT_LINK).get()
            raw_product_link = response.urljoin(link)

            # cleaning results
            product_family = ''.join(raw_product_family).strip(
            ) if raw_product_family else None
            product_name = ''.join(raw_product_name).strip(
            ) if raw_product_name else None
            product_price = ''.join(raw_product_price).strip(
            ) if raw_product_price else None
            # clean blank spaces, currency symbo $ and dot . from price
            product_price = re.sub(' |\$|\.', '', product_price)
            product_brand = ''.join(raw_product_brand).strip(
            ) if raw_product_brand else None
            product_link = ''.join(raw_product_link).strip(
            ) if raw_product_link else None

            yield {
                'product_family': product_family,
                'product_name': product_name,
                'product_price': product_price,
                'product_brand': product_brand,
                'product_link': product_link
            }

            # follow pagination link
            next_page_relative = product.xpath(
                XPATH_NEXT_PAGE).get()
            if next_page_relative:
                next_page_url = response.urljoin(next_page_relative)
                yield scrapy.Request(url=next_page_url, callback=self.parse)
