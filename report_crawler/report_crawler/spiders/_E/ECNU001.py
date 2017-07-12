# -*- coding:utf-8 -*-
import re
import scrapy
from report_crawler.spiders.__Global_function import get_localtime
from report_crawler.spiders.__Global_variable import now_time, end_time


class ECNU001_Spider(scrapy.Spider):
	name = 'ECNU001'
	start_urls = ['http://www.cs.ecnu.edu.cn/s/69/t/247/p/11/list.htm']
	domain = 'http://www.cs.ecnu.edu.cn/'
	counts = 0

	def parse(self, response):
		messages = response.xpath("//table[@height='28']").xpath("./tr")

		for i, message in enumerate(messages):
			report_url = self.domain + message.xpath(".//a/@href").extract()[0][1:]

			yield scrapy.Request(report_url, callback=self.parse_pages,
			                     meta={'link': report_url, 'number': i + 1})

	def parse_pages(self, response):
		report_time = get_localtime(re.split(u"[：:]", response.xpath("//td[@height='32']/div/strong")[0].xpath("text()").extract()[0])[-1])

		if report_time < now_time or report_time > end_time:
			return

		messages = response.xpath("//span[contains(@class, 'content')]/p")

		return {'text': messages, 'number': response.meta['number'], 'organizer': u'华东师范大学大学计算机科学技术系',
		        'faculty': self.name, 'link': response.meta['link'], 'publication': report_time}

