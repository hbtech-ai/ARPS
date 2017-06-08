# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import scrapy
from Global_function import get_localtime, print_new_number, save_messages

now_time = get_localtime(time.strftime("%Y-%m-%d", time.localtime()))
# now_time = 20170401

class THU003_Spider(scrapy.Spider):
	name = 'THU003'
	start_urls = ['http://www.math.tsinghua.edu.cn/publish/math/2582/index.html']
	domain = 'http://www.math.tsinghua.edu.cn/'
	counts = 0

	def parse(self, response):
		messages = response.xpath("//div[@class='box_list']/ul/li")
		print_new_number(self.counts, 'THU', self.name)

		for i in xrange(len(messages)):
			report_url = self.domain + messages[i].xpath(".//a/@href").extract()[0][1:]
			report_time = get_localtime(messages[i].xpath(".//p/text()").extract()[0].strip())

			if report_time < now_time:
				return
			yield scrapy.Request(report_url, callback=self.parse_pages, meta={'link': report_url, 'number': i + 1})
			# return

	def parse_pages(self, response):
		messages = response.xpath("//div[@class='box_detail']/p")
		print len(messages)

		sign = 0
		title, time, address, speaker, person_introduce, content = '', '', '', '', '', ''
		for message in messages:
			text = self.get_messages(message)
			if u'题目：' in text or u'题目:' in text:
				title = self.connect_messages(text, '：') if u'题目：' in text else self.connect_messages(text, ':')
			if u'时间：' in text or u'时间:' in text:
				time = self.connect_messages(text, '：') if u'时间：' in text else self.connect_messages(text, ':')
			if u'地点：' in text or u'地点:' in text:
				address = self.connect_messages(text, '：') if u'地点：' in text else self.connect_messages(text, ':')
			if u'报告人：' in text or u'报告人:' in text:
				speaker = self.connect_messages(text, '：') if u'报告人：' in text else self.connect_messages(text, ':')
			if u'简介：' in text or u'简介:' in text:
				sign = 1
				person_introduce = self.connect_messages(text, '：') if u'简介：' in text else self.connect_messages(text, ':')
			if u'摘要：' in text or u'摘要:' in text:
				sign = 2
				content = self.connect_messages(text, '：') if u'摘要：' in text else self.connect_messages(text, ':')
			else:
				if u'联系人' in text:
					continue
				elif sign == 1:
					person_introduce += '\n' + text
				elif sign == 2:
					content += '\n' + text
				else:
					pass

		if title != '':
			self.counts += 1
			print_new_number(self.counts, 'THU', self.name)

		all_messages = save_messages('THU', self.name, title, time, address, speaker, person_introduce,
		                             content, '', response.meta['link'], response.meta['number'], u'清华大学', u'数学科学系')

		return all_messages


	def get_messages(self, messages):
		all_text = messages.xpath(".//text()").extract()
		text = ''
		for each in all_text:
			text += each.strip()
		return text

	def connect_messages(self, messages, sign):
		text = ''
		message = messages.split(sign)[1:]
		for i in xrange(len(message)):
			if i > 0:
				text += '：'
			text += message[i].strip()
		return text
