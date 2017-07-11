# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
import time
import scrapy
from _Global_function import get_localtime
from _Global_variable import now_time, end_time

# now_time = get_localtime(time.strftime("%Y-%m-%d", time.localtime()))
# now_time = 20100101
# end_time = 20991212


class SCU001_Spider(scrapy.Spider):
	name = 'SCU001'
	start_urls = ['http://cs.scu.edu.cn/cs/xsky/xskb/H951901index_1.htm']
	domain = 'http://cs.scu.edu.cn/'
	counts = 0

	def parse(self, response):
		messages = response.xpath("//table[@width='100%']/tbody/tr/td/table").xpath(".//tr")

		for i, message in enumerate(messages[:-1]):
			report_url = self.domain + message.xpath(".//a/@href").extract()[0][1:]
			report_time = get_localtime(message.xpath(".//font/text()").extract()[0].strip('[]'))

			if report_time > end_time:
				continue
			if report_time < now_time:
				return

			yield scrapy.Request(report_url, callback=self.parse_pages,
			                     meta={'link': report_url, 'number': i + 1, 'publication': report_time})

	def parse_pages(self, response):
		messages = response.xpath("//div[@id='BodyLabel']")

		return {'text': messages, 'number': response.meta['number'], 'organizer': u'四川大学计算机学院',
		        'faculty': self.name, 'link': response.meta['link'], 'publication': response.meta['publication']}

