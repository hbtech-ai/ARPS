# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
import time
import scrapy
from Global_function import get_localtime

now_time = get_localtime(time.strftime("%Y-%m-%d", time.localtime()))
# now_time = 20100101
end_time = 20991212


class JLU001_Spider(scrapy.Spider):
	name = 'JLU001'
	start_urls = ['http://ccst.jlu.edu.cn/?mod=info&act=list&id=67&page=1']
	domain = 'http://ccst.jlu.edu.cn/'
	counts = 0

	def parse(self, response):
		messages = response.xpath("//div[@class='list']/ul/li")

		for i, message in enumerate(messages):
			report_name = message.xpath("a/text()").extract()[0]

			if u"讲座" not in report_name:
				continue
			report_url = self.domain + message.xpath("a/@href").extract()[0]

			yield scrapy.Request(report_url, callback=self.parse_pages, meta={'number': i + 1})

	def parse_pages(self, response):
		messages = response.xpath("//div[@class='readcontent']").xpath(".//p")

		return {'text': messages, 'number': response.meta['number'], 'organizer': u'吉林大学计算机科学与技术学院', 'faculty': self.name}
