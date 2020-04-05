# -*- coding: utf-8 -*-
import scrapy
import re


class FerretekCrawlerSpider(scrapy.Spider):
    name = 'ferretek_crawler'
    allowed_domains = ['herramientas.cl']
    start_urls = [
        'https://herramientas.cl/subcategorias/101010/taladros-electricos'
        #'https://herramientas.cl/subcategorias/101010/taladros-electricos/0/0/0/0/0/12/pagina-2'
    ]

    def parse(self, response):
        """Process Ferretek(herramientas.cl) products"""
        products = response.xpath("//div[@class='grilla grilla-dos']")

        # iterate over search results
        for product in products:
            # define the XPaths
            XPATH_PRODUCT_NAME = ".//a[@class='nombreGrilla link']/text()"
            XPATH_PRODUCT_PRICE = ".//a[@class='valorGrilla link']/text()"
            # define alternative Xpath if product is on sale
            XPATH_PRODUCT_PRICE_SALE = ".//a[@class='valorGrilla link']//span[@class='conDescuento']/text()"
            XPATH_PRODUCT_BRAND = ".//a[@class='marca link']/span/text()"
            XPATH_PRODUCT_LINK = ".//a[@class='imgGrilla']/@href"
            XPATH_NEXT_PAGE = "//div[@class='cont100Centro paginador']//a[@class='paginate next']/@href"

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
