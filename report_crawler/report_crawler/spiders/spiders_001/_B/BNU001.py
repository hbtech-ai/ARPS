# -*- coding:utf-8 -*-
import scrapy
from report_crawler.spiders.__Global_function import get_localtime
from report_crawler.spiders.__Global_variable import now_time, end_time


class BNU001_Spider(scrapy.Spider):
	name = 'BNU001'
	start_urls = ['http://cist.bnu.edu.cn/tzgg/index.html']
	domain = 'http://cist.bnu.edu.cn/tzgg/'
	counts = 0

	def parse(self, response):
		messages = response.xpath("//div[@class='twelve columns alpha']/ul/li")

		for i, message in enumerate(messages):
			report_name = message.xpath(".//a/@title").extract()[0]
			if u"【预告】" not in report_name or u"论坛" in report_name:
				continue

			report_time = get_localtime(message.xpath("span/text()").extract()[0])
			if report_time > end_time:
				continue
			if report_time < now_time:
				return

			report_url = self.domain + message.xpath(".//a/@href").extract()[0]
			yield scrapy.Request(report_url, callback=self.parse_pages,
			                     meta={'link': report_url, 'number': i + 1, 'publication': report_time})

	def parse_pages(self, response):
		messages = response.xpath("//div[@class='heading']")

		return {'text': messages, 'number': response.meta['number'], 'organizer': u"北京师范大学信息科学与技术学院",
		        'faculty': self.name, 'link': response.meta['link'], 'publication': response.meta['publication'],
		        'location': u"华北:北京市"}
