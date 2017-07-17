# -*- coding:utf-8 -*-
import scrapy
from report_crawler.spiders.__Global_function import get_localtime
from report_crawler.spiders.__Global_variable import now_time, end_time


class HNU001_Spider(scrapy.Spider):
	name = 'HNU001'
	start_urls = ['http://csee.hnu.edu.cn/Front/TZXX_List?LMXX_BH=20130728174138ec48068e-48bf-49a6-ac51-27d04a9b1baa']
	domain = 'http://csee.hnu.edu.cn/'

	def parse(self, response):
		messages = response.xpath("//ul[@class='article-list']/li")

		for i, message in enumerate(messages):
			report_name = message.xpath(".//a/text()").extract()[0]
			report_time = get_localtime(message.xpath("span/text()").extract()[0].strip().strip("[]"))
			if report_time > end_time:
				continue
			if report_time < now_time:
				return

			report_url = self.domain + message.xpath(".//a/@href").extract()[0][1:]
			yield scrapy.Request(report_url, callback=self.parse_pages,
			                     meta={'link': report_url, 'number': i + 1, 'publication': report_time, 'title': report_name})

	def parse_pages(self, response):
		messages = response.xpath("//div[@class='content-1']")

		return {'text': messages, 'number': response.meta['number'], 'organizer': u"湖南大学大学信息科学与工程学院",
		        'faculty': self.name, 'link': response.meta['link'], 'publication': response.meta['publication'],
		        'location': u"华中:湖南省-长沙市", 'title': response.meta['title']}
