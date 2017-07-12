# -*- coding:utf-8 -*-
import scrapy
from report_crawler.spiders.__Global_function import get_localtime
from report_crawler.spiders.__Global_variable import now_time, end_time


class SYSU001_Spider(scrapy.Spider):
    name = 'NWSUAF001'
    start_urls = ['http://cie.nwsuaf.edu.cn/xzhd/index.htm']
    domains = 'http://cie.nwsuaf.edu.cn/xzhd/'

    def parse(self, response):
        messages = response.xpath("//dd/ul/li")

        for i in xrange(len(messages)):
            report_url = self.domains + messages[i].xpath(".//a/@href").extract()[0]
            report_time = get_localtime(messages[i].xpath(".//span/text()").extract()[0])
            
            if report_time > end_time:
                continue
            if report_time < now_time:
                return
            yield scrapy.Request(report_url, callback=self.parse_pages,
                                 meta={'link': report_url, 'number': i + 1, 'publication': report_time})

    def parse_pages(self, response):
        messages = response.xpath("//div[@class='article_content']/p")

        return {'text': messages, 'number': response.meta['number'], 'organizer': u'西北农林科技大学信息工程学院',
                'faculty': self.name, 'link': response.meta['link'], 'publication': response.meta['publication']}