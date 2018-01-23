# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime

url_begin = "http://titanst.ru"

class TitanstSpider(scrapy.Spider):
    name = 'titanst'
    allowed_domains = ['titanst.ru']
    start_urls = ['http://titanst.ru/catalog/avtotovary/', 'http://titanst.ru/catalog/instrumenty/', 'http://titanst.ru/catalog/osveshchenie/', 'http://titanst.ru/catalog/sadovyy_tsentr/', 'http://titanst.ru/catalog/santekhnika/', 'http://titanst.ru/catalog/stroitelnye_materialy/', 'http://titanst.ru/catalog/tovary_dlya_doma/']

    def parse(self, response):
    	#get utr products
        urls = response.xpath('//div[@class="info"]/p[@class="title"]/a/@href').extract()
        for url in urls:
        	url = url_begin + url
        	yield scrapy.Request(url=url, callback=self.parse_details)
        #follow pagination link
        next_page_url = response.xpath('//a[@class="p_nxt"]/@href').extract_first()
        if next_page_url:
        	next_page_url = url_begin + next_page_url
        	yield scrapy.Request(url=next_page_url, callback=self.parse)
    #get product detail page
    def parse_details (self, response):
        yield {
            'date_time_crawl': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'url': response.request.url,
            'category': response.xpath('//div[@class="breadcrumbs"]/a/text()')[-1].extract(),
            'product': response.xpath('//h1/text()').extract_first(),
            'price': response.xpath('//p[@class="new_price"]/text()').extract_first().replace(" ","").replace(".",","),
            'availability': response.xpath('//p[@class="info_p orange"]/text()').extract_first().rstrip().replace(":",""),
            'quantity': response.xpath('//p[@class="info_p orange"]/span/text()').extract_first().split()[0].replace(".",","),
            'unit': response.xpath('//p[@class="info_p orange"]/span/text()').extract_first().split()[1],
            'img_url': url_begin + response.xpath('//div[@class="detail_img"]/a/@href').extract_first(),
        }
