import scrapy
from scrapy.loader import ItemLoader
from product_scrapper.items import ProductScrapperItem
from urllib.parse import urljoin


class ProductSpider(scrapy.Spider):
    name = "products"

    def start_requests(self):
        base_url = "http://www.boohoo.com"

        yield scrapy.Request(url=base_url, callback=self.parse)

    def parse(self, response):

        product_category = {}
        product_by_gender = "/html/body/div[@class='pt_storefront']" \
                            "/div[@class='top-banner']" \
                            "/div['sticky-header js-sticky-header']" \
                            "/div/nav/ul/li/a/@href"

        links = response.xpath(product_by_gender).extract()
        for link in links:
            yield scrapy.Request(url=link, callback=self.get_categories)

    def get_categories(self, response):
        # yield scrapy.Request(url=response.text,
        #                      callback=self.get_products)
        product_by_type = "/html/body/div[@class='pt_categorylanding']" \
                          "/div[@id='main']/div/div/a/@href"

        links = response.xpath(product_by_type).extract()
        for link in links:
            yield scrapy.Request(url=link, callback=self.get_products)

    def get_products(self, response):
        product = "/html/body/div[@class='pt_product-search-result ']/" \
                  "div[@id='main']/div[1]/div[@id='primary']/" \
                  "div['search-result-content']/ul/" \
                  "li/div/div[1]/a/@href"
        links = response.xpath(product).extract()
        for link in links:
            complete_link = urljoin(response.url, link)
            yield scrapy.Request(url=complete_link,
                                 callback=self.retrieve_product_info)

        # moving onto the next page
        next_page = "/html/body/div[@class='pt_product-search-result ']/" \
                    "div[@id='main']/div[1]/div[@id='primary']/" \
                    "div[5]/div/ul/" \
                    "li[@class='pagination-item pagination-item-next']/a/@href"
        link = response.xpath(next_page).extract_first()
        if link:
            yield scrapy.Request(url=link, callback=self.get_products)

    def retrieve_product_info(self, response):
        name = "/html/body/div[@class='pt_product-details']/div[@id='main']/" \
               "div/div/div[@class='product-col-2 product-detail']/h1/text()"

        product_id = "/html/body/div[@class='pt_product-details']/" \
                     "div[@id='main']/div/div/@data-product-details-amplience"

        product_desc = "/html/body/div[@class='pt_product-details']/" \
                       "div[@id='main']/div/div/" \
                       "div[@class='product-col-2 product-detail']/div/ul/" \
                       "li[@id='product-short-description-tab']/div/p/text()"

        product_care = "/html/body/div[@class='pt_product-details']/" \
                       "div[@id='main']/div/div/" \
                       "div[@class='product-col-2 product-detail']/div/ul/" \
                       "li[@id='product-custom-composition-tab']/div/text()"

        colors = "/html/body/div[3]/div[5]/div/div/div[2]/div/div[3]/ul" \
                 "/li[1]/div[2]/ul/li[1]/span/@title"

        product_price = "/html/body/div[@class='pt_product-details']/" \
                        "div[@id='main']/div/div/div[@class='product-col-2" \
                        " product-detail']/div/div[@class='product-price']" \
                        "/span/text()"

        product_id = response.xpath(product_id).extract_first()
        product_id = product_id.split(',')[0].split(':')[1]
        product_id = product_id.strip('""')

        colors = response.xpath(colors).extract()
        url = response.url

        products = ItemLoader(item=ProductScrapperItem(), response=response)
        products.add_xpath('name', name)
        products.add_xpath('product_desc', product_desc)
        products.add_xpath('product_price', product_price)
        products.add_xpath('product_care', product_care)

        products.add_value('url', url)
        products.add_value('product_id', product_id)

        for color in colors:
            color = color.split(':')[1].strip(' ')
            products.add_value('colors', color)

            products.add_value('image_urls', "http://i1.adis.ws/i/"
                               "boohooamplience/" +
                               product_id.lower() + "_" + color +
                               "_xl?$product_image_main_thumbnail")

            products.add_value('image_urls', "http://i1.adis.ws/i/"
                               "boohooamplience/" +
                               product_id.lower() + "_" + color +
                               "_xl?$product_image_main")

            for i in range(1, 4):
                products.add_value('image_urls', "http://i1.adis.ws/i/"
                                   "boohooamplience/" +
                                   product_id.lower() +
                                   "_" + color + "_xl_" + str(i) +
                                   "?$product_image_main_thumbnail")

                products.add_value('image_urls', "http://i1.adis.ws/i/"
                                   "boohooamplience/" +
                                   product_id.lower() +
                                   "_" + color + "_xl_" + str(i) +
                                   "?$product_image_main")

        return products.load_item()
