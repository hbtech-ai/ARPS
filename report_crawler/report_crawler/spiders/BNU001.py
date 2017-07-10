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
			yield scrapy.Request(report_url, callback=self.parse_pages, meta={'link': report_url, 'number': i + 1})

	def parse_pages(self, response):
		messages = response.xpath("//div[@class='heading']")

		return {'text': messages, 'number': response.meta['number'], 'organizer': u"北京师范大学信息科学与技术学院",
		        'faculty': self.name, 'link': response.meta['link']}


