# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import scrapy
from Global_function import get_localtime, print_new_number, save_messages

now_time = get_localtime(time.strftime("%Y-%m-%d", time.localtime()))
# now_time = 20170420

class USTC005_Spider(scrapy.Spider):
	name = 'USTC005'
	start_urls = ['http://www.pmo.cas.cn/gs/gk/xsbg/']
	domain = 'http://www.pmo.cas.cn/'
	counts = 0

	def parse(self, response):
		messages = response.xpath("//div[@class='list']/ul/li")
		print_new_number(self.counts, 'USTC', self.name)

		for i in xrange(len(messages)):
			if u'青年论坛' in messages[i].xpath(".//a/text()").extract()[0]:
				report_url = messages[i].xpath(".//a/@href").extract()[0]
			else:
				report_url = self.domain + messages[i].xpath(".//a/@href").extract()[0][9:]
			if 'Colloquium' in report_url:
				continue
			report_time = get_localtime('20' + messages[i].xpath(".//span/text()").extract()[0].strip('[]'))

			if report_time < now_time:
				return
			yield scrapy.Request(report_url, callback=self.parse_pages, meta={'link': report_url, 'number': i + 1})

	def parse_pages(self, response):
		messages = response.xpath("//div[@class='TRS_Editor']").xpath(".//p")

		sign = 0
		title, speaker, time, address, content, person_introduce = '', '', '', '', '', ''
		for message in messages:
			text = self.get_text(message)
			if u'欢迎大家' in text or u'联系人' in text or u'紫金山天文台学术委员会' in text:
				continue
			elif u'题目：' in text or 'Title：' in text or u'题目:' in text or 'Title:' in text:
				title = self.connect_message(text, '：') if u'题目：' in text or 'Title：' in text else self.connect_message(text, ':')
			elif u'报告人：' in text or 'Speaker：' in text or u'主讲人：' in text or u'报告人:' in text or 'Speaker:' in text or u'主讲人:' in text:
				speaker = self.connect_message(text, '：') if u'报告人：' in text or 'Speaker：' in text or u'主讲人：' in text else self.connect_message(text, ':')
			elif u'时间：' in text or 'Time：' in text or u'时间:' in text or 'Time:' in text:
				time = self.connect_message(text, '：') if u'时间：' in text or 'Time：' in text else self.connect_message(text, ':')
			elif u'地点：' in text or 'Address：' in text or u'地点:' in text or 'Address:' in text:
				address = self.connect_message(text, '：') if u'地点：' in text or 'Address：' in text else self.connect_message(text, ':')
			elif u'简介：' in text or 'Bio：' in text or u'简介:' in text or 'Bio:' in text:
				sign = 1
				person_introduce = self.connect_message(text, '：') if u'简介：' in text or 'Bio：' in text else self.connect_message(text, ':')
			elif u'摘要：' in text or 'Abstract：' in text or u'摘要:' in text or 'Abstract:' in text:
				sign = 2
				content = self.connect_message(text, '：') if u'摘要：' in text or 'Abstract：' in text else self.connect_message(text, ':')
			else:
				if sign == 1:
					person_introduce += text.strip()
				elif sign == 2:
					content += text.strip()

		if title != '':
			self.counts += 1
			print_new_number(self.counts, 'USTC', self.name)

		all_messages = save_messages('USTC', self.name, title, time, address, speaker, person_introduce,
		                             content, '', response.meta['link'], response.meta['number'], u'中国科学技术大学', u'天文与空间科学学院')

		return all_messages

	def get_text(self, message):
		text = ''
		for each in message.xpath(".//text()").extract():
			text += each.strip()
		return text

	def connect_message(self, message, sign):
		text = ''
		all = message.split(sign)[1:]
		for i in xrange(len(all)):
			if i > 0:
				text += '：'
			text += all[i].strip()
		return text