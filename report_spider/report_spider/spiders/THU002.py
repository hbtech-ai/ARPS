# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
import requests
import time
import scrapy
from Global_function import get_localtime, print_new_number, save_messages

now_time = get_localtime(time.strftime("%Y-%m-%d", time.localtime()))
# now_time = 20170401

class THU002_Spider(scrapy.Spider):
	name = 'THU002'
	start_urls = ['http://www.cess.tsinghua.edu.cn/publish/ess/10541/index.html']
	domain = 'http://www.cess.tsinghua.edu.cn/'
	counts = 0

	def parse(self, response):
		messages = response.xpath("//ul[@class='zjlt clearfix mt-45']/li")
		print_new_number(self.counts, 'THU', self.name)

		for i, message in enumerate(messages):
			report_url = self.domain + message.xpath(".//div[@class='info fr']").xpath('.//a/@href').extract()[0][1:]

			yield scrapy.Request(report_url, callback=self.parse_pages, meta={'link': report_url, 'number': i + 1})

	def parse_pages(self, response):
		messages = response.xpath("//div[@class='bbs-info']")

		title = self.try_get_message(messages.xpath(".//h2/text()").extract())

		time = messages.xpath(".//p")[0].xpath(".//text()").extract()[1]

		address = messages.xpath(".//p")[1].xpath(".//text()").extract()[1]

		speaker = messages.xpath(".//p")[2].xpath(".//text()").extract()[1]

		# other = response.xpath("//div[@class='show-new']")

		# if len(other) == 0:
		# 	content = ''
		# else:
		# 	content = other.xpath(".//text()").extract()[0].strip()
		# 	if u'简介：' in content or 'Abstract：' in content or u'简介:' in content or 'Abstract:' in content:
		# 		content = self.connect_messages(content, '：') if u'简介：' in content or 'Abstract：' in content else self.connect_messages(content, ':')
		# 	else:
		# 		pass

		report_time = get_localtime(response.xpath("//div[@class='wtime']/text()").extract()[0].strip())
		if report_time < now_time:
			title = ''
		else:
			self.counts += 1
		print_new_number(self.counts, 'THU', self.name)

		all_messages = save_messages('THU', self.name, title, time, address, speaker, '',
		                             '', '', response.meta['link'], response.meta['number'], u'清华大学', u'地球系统科学系')

		return all_messages

	def try_get_message(self, messages):
		try:
			ans = messages[0]
		except:
			ans = ''
		return ans

	def connect_messages(self, messages, sign):
		text = ''
		message = messages.split(sign)[1:]
		for i in xrange(len(message)):
			if i > 0:
				text += '：'
			text += message[i].strip()
		return text
