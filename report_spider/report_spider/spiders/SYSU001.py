# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import scrapy
from Global_function import get_localtime, print_new_number, save_messages

now_time = get_localtime(time.strftime("%Y-%m-%d", time.localtime()))

class SYSU001_Spider(scrapy.Spider):
	name = 'SYSU001'
	start_urls = ['http://sdcs.sysu.edu.cn/research/activity']
	domains = 'http://sdcs.sysu.edu.cn/'
	counts = 0

	def parse(self, response):
		messages = response.xpath("//div[@class='full-page-list']/ul/li")

		for message in messages:
			report_name = message.xpath(".//a/text()").extract()[0]
			if u'学术报告：' not in report_name and u'学术报告:' not in report_name:
				continue
			report_url = self.domains + message.xpath(".//a/@href").extract()[0][1:]
			report_time = get_localtime(message.xpath(".//span/text()").extract()[0].replace('/', '-'))

			if report_time < now_time:
				print_new_number(self.counts, 'SYSU', self.name)
				return
			self.counts += 1
			yield scrapy.Request(report_url, callback=self.parse_pages, meta={'link': report_url, 'number': self.counts})

	def parse_pages(self, response):
		messages = response.xpath("//div[@class='field-items']").xpath(".//p")

		sign = 0
		title, time, address, speaker, person_introduce, content, date = '', '', '', '', '', '', ''
		for message in messages:
			text, replace = self.connect_messages(message.xpath(".//text()").extract())
			if u'题目：' in replace or 'Title：' in replace or u'题目:' in replace or 'Title:' in replace:
				title = self.get_messages(text, '：') if u'题目：' in replace or 'Title：' in replace else self.get_messages(text, ':')
			elif u'时间' in replace or 'Time：' in replace or u'时间:' in replace or 'Time:' in replace:
				time = self.get_messages(text, '：') if u'时间：' in replace or 'Time：' in replace else self.get_messages(text, ':')
			elif u'地点：' in replace or 'Address：' in replace or u'地点:' in replace or 'Address:' in replace:
				address = self.get_messages(text, '：') if u'地点：' in replace or 'Address：' in replace else self.get_messages(text, ':')
			elif u'主讲：' in replace or u'报告人：' in replace or 'Speaker：' in replace or u'主讲:' in replace or u'报告人：' in replace or 'Speaker:' in replace:
				speaker = self.get_messages(text, '：') if u'主讲：' in replace or u'报告人：' in replace or 'Speaker：' in replace else self.get_messages(text, ':')
			elif u'日期：' in replace or 'Date：' in replace or u'日期:' in replace or 'Date:' in replace:
				date = self.get_messages(text, '：') if u'日期：' in replace or 'Date：' in replace else self.get_messages(text, ':')
			elif u'地点：' in text or 'Address：' in replace or u'地点:' in replace or 'Address:' in replace:
				address = self.get_messages(text, '：') if u'地点：' in replace or 'Address：' in replace else self.get_messages(text, ':')
			elif u'简介：' in text or 'Biography：' in replace or 'Bio：' in replace or u'简介:' in replace or 'Biography:' in replace or 'Bio:' in replace:
				sign = 1
				person_introduce = self.get_messages(text, '：') if u'简介：' in replace or 'Biography：' in replace or 'Bio：' in replace else self.get_messages(text, ':')
			elif u'摘要：' in replace or 'Abstract：' in replace or u'摘要:' in replace or 'Abstract:' in replace:
				sign = 2
				content = self.get_messages(text, '：') if u'摘要：' in replace or 'Abstract：' in replace else self.get_messages(text, ':')
			else:
				if sign == 1:
					person_introduce += text
				elif sign == 2:
					content += text
		time = (date + ' ' + time).strip()

		all_messages = save_messages('SYSU', self.name, title, time, address, speaker, person_introduce,
		                             content, '', response.meta['link'], response.meta['number'])

		return all_messages

	def get_messages(self, messages, sign):
		text = ''
		message = messages.split(sign)[1:]
		for i in xrange(len(message)):
			if i > 0:
				text += '：'
			text += message[i].strip()
		return text

	def connect_messages(self, messages):
		text = ''
		replace = ''
		for message in messages:
			text += message.strip()
			replace += message.strip().replace(' ', '')
		return text, replace
