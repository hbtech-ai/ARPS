# -*- coding:utf-8 -*-
import scrapy
from report_crawler.spiders.__Global_function import get_localtime
from report_crawler.spiders.__Global_variable import now_time, end_time


class SWJTU001_Spider(scrapy.Spider):
	name = 'SWJTU001'
	start_urls = ['http://sist.swjtu.edu.cn/list.do?action=news&navId=40']
	domain = 'http://sist.swjtu.edu.cn/'

	def parse(self, response):
		messages = response.xpath("//div[@id='rightPageContent']/dl/dd")

		for i, message in enumerate(messages):
			report_time = get_localtime(message.xpath("span/text()").extract()[0])
			if report_time > end_time:
				continue
			if report_time < now_time:
				return

			report_url = message.xpath(".//a/@href").extract()[0]
			yield scrapy.Request(report_url, callback=self.parse_pages,
			                     meta={'link': report_url, 'number': i + 1, 'publication': report_time})

	def parse_pages(self, response):
		messages = response.xpath("//div[@id='newsBody']")

		return {'text': messages, 'number': response.meta['number'], 'organizer': u'西南交通大学大学计算机科学与技术学院',
		        'faculty': self.name, 'link': response.meta['link'], 'publication': response.meta['publication'],
		        'location': u"西南:四川省-成都市"}
