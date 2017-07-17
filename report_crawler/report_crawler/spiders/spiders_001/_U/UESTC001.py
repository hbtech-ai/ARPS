# -*- coding:utf-8 -*-
import scrapy
from report_crawler.spiders.__Global_function import get_localtime
from report_crawler.spiders.__Global_variable import now_time, end_time


class UESTC_Spider(scrapy.Spider):
	name = 'UESTC001'
	start_urls = ['http://www.ccse.uestc.edu.cn/list?type=11']
	domain = 'http://www.ccse.uestc.edu.cn/'

	def parse(self, response):
		messages = response.xpath("//div[@id='newsList']/p")

		for i, message in enumerate(messages):
			report_time = get_localtime(message.xpath(".//span[@id='time']/text()").extract()[0])
			if report_time > end_time:
				continue
			if report_time < now_time:
				return

			report_url = self.domain + message.xpath(".//a/@href").extract()[0]
			yield scrapy.Request(report_url, callback=self.parse_pages,
			                     meta={'link': report_url, 'number': i + 1, 'publication': report_time})

	def parse_pages(self, response):
		messages = response.xpath("//div[@id='newsContent']")

		return {'text': messages, 'number': response.meta['number'], 'organizer': u"电子科技大学计算机科学与工程学院",
		        'faculty': self.name, 'link': response.meta['link'], 'publication': response.meta['publication'],
		        'location': u"西南:四川省-成都市"}
