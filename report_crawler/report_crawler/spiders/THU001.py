# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import scrapy
from Global_function import get_localtime, print_new_number, save_messages

# now_time = get_localtime(time.strftime("%Y-%m-%d", time.localtime()))
now_time = 20101010


class THU001_Spider(scrapy.Spider):
	name = 'THU001'
	start_urls = ['http://www.cs.tsinghua.edu.cn/publish/cs/4852/index.html']
	domain = 'http://www.cs.tsinghua.edu.cn/'
	counts = 0

	def parse(self, response):
		messages = response.xpath("//div[@class='box_list']/ul/li")


		for i in xrange(len(messages)):
			report_url = self.domain + messages[i].xpath(".//a/@href").extract()[0][1:]
			report_time = get_localtime(messages[i].xpath(".//p/text()").extract()[0].strip())

			if report_time < now_time:
				return
			yield scrapy.Request(report_url, callback=self.parse_pages, meta={'link': report_url, 'number': i + 1})

	def parse_pages(self, response):
		messages = response.xpath("//div[@class='box_detail']/p").xpath(".//text()").extract()

		return {'text': messages, 'number': response.meta['number'], 'organizer': u'清华大学计算机科学与技术系', 'faculty': self.name}

	def get_messages(self, messages, sign):
		text = ''
		message = messages.split(sign)[1:]
		for i in xrange(len(message)):
			if i > 0:
				text += '：'
			text += message[i].strip()
		return text
