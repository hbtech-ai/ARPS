# -*- coding:utf-8 -*-
import time
import scrapy
from _Global_function import get_localtime
from _Global_variable import now_time, end_time

# now_time = get_localtime(time.strftime("%Y-%m-%d", time.localtime()))
# now_time = 20170101
# end_time = 20991212


class SYSU001_Spider(scrapy.Spider):
	name = 'SYSU001'
	start_urls = ['http://sdcs.sysu.edu.cn/research/activity']
	domains = 'http://sdcs.sysu.edu.cn/'
	counts = 0

	def parse(self, response):
		messages = response.xpath("//div[@class='full-page-list']/ul/li")

		for i in xrange(len(messages)):
			report_url = self.domains + messages[i].xpath(".//a/@href").extract()[0][1:]
			report_time = get_localtime(messages[i].xpath(".//span/text()").extract()[0].replace('/', '-'))

			if report_time > end_time:
				continue
			if report_time < now_time:
				return
			yield scrapy.Request(report_url, callback=self.parse_pages, meta={'link': report_url, 'number': i + 1})

	def parse_pages(self, response):
		messages = response.xpath("//div[@class='field-items']")

		return {'text': messages, 'number': response.meta['number'], 'organizer': u'中山大学计算机学院',
		        'faculty': self.name, 'link': response.meta['link']}
