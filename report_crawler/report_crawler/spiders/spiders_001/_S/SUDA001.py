# -*- coding:utf-8 -*-
import re
import scrapy
from report_crawler.spiders.__Global_function import get_localtime
from report_crawler.spiders.__Global_variable import now_time, end_time


class SUDA001_Spider(scrapy.Spider):
	name = 'SUDA001'
	start_urls = ['http://scst.suda.edu.cn/ShowPage.aspx?id=52']
	domain = 'http://scst.suda.edu.cn/'

	def parse(self, response):
		messages = response.xpath("//div[@id='TextList_time']/table")[0].xpath("tr")

		for i, message in enumerate(messages):
			report_sign = message.xpath(".//a")
			if len(report_sign) == 0:
				continue

			report_time = get_localtime(message.xpath("td")[-1].xpath(".//text()").extract()[0])
			if report_time > end_time:
				continue
			elif report_time < now_time:
				return

			report_url = self.domain + message.xpath(".//a/@href").extract()[0]
			yield scrapy.Request(report_url, callback=self.parse_pages,
			                     meta={'link': report_url, 'number': i + 1, 'publication': report_time})

	def parse_pages(self, response):
		messages = response.xpath("//div[@id='singleNews']")

		return {'text': messages, 'number': response.meta['number'], 'organizer': u'苏州大学计算机科学与技术学院',
		        'faculty': self.name, 'link': response.meta['link'], 'publication': response.meta['publication'],
		        'location': u"华东:江苏省-苏州市"}
