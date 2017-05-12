# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import scrapy
from Global_function import get_localtime, print_new_number, save_messages

now_time = get_localtime(time.strftime("%Y-%m-%d", time.localtime()))
# now_time = 20170401

class USTC006_Spider(scrapy.Spider):
	name = 'USTC006'
	start_urls = ['http://biox.ustc.edu.cn/xsbg/']
	domain = 'http://biox.ustc.edu.cn/xsbg/'
	counts = 0

	def parse(self, response):
		messages = response.xpath("//ul[@class='list-none metlist']/li")
		print_new_number(self.counts, 'USTC', self.name)

		for i in xrange(len(messages)):
			report_url = self.domain + messages[i].xpath(".//a/@href").extract()[0][2:]
			report_time = get_localtime(messages[i].xpath(".//span/text()").extract()[0].strip())

			if report_time < now_time:
				return
			yield scrapy.Request(report_url, callback=self.parse_pages, meta={'link': report_url, 'number': i + 1})
			# return
	def parse_pages(self, response):
		messages = response.xpath("//div[@class='justify']").xpath(".//p").xpath(".//text()").extract()

		sign = 0
		title, time, address, speaker, person_introduce, content = '', '', '', '', '', ''
		for message in messages:
			if u'题目：' in message or u'题目:' in message:
				title = self.connect_messages(message, '：') if u'题目：' in message else self.connect_messages(message, ':')
			elif u'时间：' in message or u'时间:' in message:
				time = self.connect_messages(message, '：') if u'时间：' in message else self.connect_messages(message, ':')
			elif u'地点：' in message or u'地点:' in message:
				address = self.connect_messages(message, '：') if u'地点：' in message else self.connect_messages(message, ':')
			elif u'报告人：' in message or u'报告人:' in message:
				speaker = self.connect_messages(message, '：') if u'报告人：' in message else self.connect_messages(message, ':')
			elif u'摘要：' in message or u'摘要:' in message:
				sign = 1
				content = self.connect_messages(message, '：') if u'摘要：' in message else self.connect_messages(message, ':')
			elif u'简介：' in message or u'简介:' in message:
				sign = 2
				person_introduce = self.connect_messages(message, '：') if u'简介：' in message else self.connect_messages(message, ':')
			else:
				if u'联系人' in message:
					continue
				if sign == 1:
					content += '\n' + message.strip()
				elif sign == 2:
					person_introduce += '\n' + message.strip()
				else:
					pass

		if title != '':
			self.counts += 1
			print_new_number(self.counts, 'USTC', self.name)

		all_messages = save_messages('USTC', self.name, title, time, address, speaker, person_introduce,
		                             content, '', response.meta['link'], response.meta['number'], u'中国科学技术大学')

		return all_messages

	def connect_messages(self, messages, sign):
		text = ''
		message = messages.split(sign)[1:]
		for i in xrange(len(message)):
			if i > 0:
				text += '：'
			text += message[i].strip()
		return text
