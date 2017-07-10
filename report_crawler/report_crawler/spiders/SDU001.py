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
# now_time = 20170303
# end_time = 20991212


class SUD001_Spider(scrapy.Spider):
	name = 'SDU001'
	start_urls = ['http://www.cs.sdu.edu.cn/getMoreNews.do?pageNum=1&newsType=jsj2102']
	domain = 'http://www.cs.sdu.edu.cn/'
	counts = 0

	def parse(self, response):
		messages = response.xpath("//div[@class='sub_text']").xpath(".//div[@class='news-list']")

		for i, message in enumerate(messages):
			report_name = message.xpath(".//a/text()").extract()[0]
			if re.search(u"学术(报告)|(讲座)", report_name) is None:
				continue

			report_url = self.domain + message.xpath(".//a/@href").extract()[0][1:]
			report_time = get_localtime(message.xpath(".//div[@class='lastTime']/text()").extract()[0])

			if report_time > end_time:
				continue
			if report_time < now_time:
				return

			yield scrapy.Request(report_url, callback=self.parse_pages, meta={'link': report_url, 'number': i + 1})

	def parse_pages(self, response):
		messages = response.xpath("//div[@class='newsContent']")[1].xpath(".//p")

		if len(messages) == 0:
			messages = response.xpath("//div[@class='newsContent']")[1].xpath(".//div")

		return {'text': messages, 'number': response.meta['number'], 'organizer': u'山东大学计算机科学与技术学院',
		        'faculty': self.name, 'link': response.meta['link']}
