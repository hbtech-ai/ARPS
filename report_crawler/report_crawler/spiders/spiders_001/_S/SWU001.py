# -*- coding:utf-8 -*-
import re
import scrapy
from report_crawler.spiders.__Global_function import get_localtime
from report_crawler.spiders.__Global_variable import now_time, end_time


class SWU001_Spider(scrapy.Spider):
	name = 'SWU001'
	start_urls = ['http://computer.swu.edu.cn/s/computer/kxyj2xsky/index.html']
	domain = 'http://computer.swu.edu.cn/'

	def parse(self, response):
		messages = response.xpath("//div[@class='news-list']/ul/li")

		for i, message in enumerate(messages):
			report_time = get_localtime(re.sub(u"[]\[]", '', message.xpath("span/text()").extract()[0].strip()))
			if report_time > end_time:
				continue
			if report_time < now_time:
				return

			report_url = self.domain + message.xpath(".//a/@href").extract()[0][1:]
			yield scrapy.Request(report_url, callback=self.parse_pages,
			                     meta={'link': report_url, 'number': i + 1, 'publication': report_time})

	def parse_pages(self, response):
		messages = response.xpath("//div[@class='news-detail']")

		return {'text': messages, 'number': response.meta['number'], 'organizer': u'西南大学计算机与信息科学学院',
		        'faculty': self.name, 'link': response.meta['link'], 'publication': response.meta['publication'],
		        'location': u"西南:重庆市"}
