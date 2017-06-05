# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import scrapy
from Global_function import get_localtime, print_new_number, save_messages

now_time = get_localtime(time.strftime("%Y-%m-%d", time.localtime()))
# now_time = 20170401

class THU004_Spider(scrapy.Spider):
	name = 'THU004'
	start_urls = ['http://www.chemeng.tsinghua.edu.cn/podcast.do?method=news&cid=34']
	domain = 'http://www.chemeng.tsinghua.edu.cn/'
	counts = 0

	def parse(self, response):
		messages = response.xpath("//div[@class='employlist']/ul/li")

		for i in xrange(len(messages)):
			report_url = self.domain + messages[i].xpath(".//a/@href").extract()[0]
			report_time = get_localtime(messages[i].xpath(".//cite/text()").extract()[0].strip().strip('[]'))

			yield scrapy.Request(report_url, callback=self.parse_pages, meta={'link': report_url, 'number': i + 1})

	def parse_pages(self, response):
		messages = response.xpath("//td[@height='400']/p")

		title = response.xpath("//h4/text()").extract()[0].strip()

		time, address, speaker, img_url = '', '', '', ''
		for message in messages:
			text = self.get_messages(message)
			if u'时间：' in text or u'时间:' in text:
				time = self.connect_messages(text, '：') if u'时间：' in text else self.connect_messages(text, ':')
			if u'地点：' in text or u'地点:' in text:
				address = self.connect_messages(text, '：') if u'地点：' in text else self.connect_messages(text, ':')
			if u'报告人：' in text or u'报告人:' in text:
				speaker = self.connect_messages(text, '：') if u'报告人：' in text else self.connect_messages(text, ':')
			img = message.xpath(".//img/@src")
			img_url = (self.domain + img.extract()[0][1:]) if len(img) > 0 else ''

		if title != '':
			self.counts += 1
			print_new_number(self.counts, 'THU', self.name)

		all_messages = save_messages('THU', self.name, title, time, address, speaker, '',
		                             '', img_url, response.meta['link'], response.meta['number'], u'清华大学')

		return all_messages

	def get_messages(self, messages):
		text = ''
		message = messages.xpath(".//text()").extract()
		for each in message:
			text += each.strip()
		return text

	def connect_messages(self, messages, sign):
		message = messages.split(sign)[1:]
		text = ''
		for i in xrange(len(message)):
			if i > 0:
				text += '：'
			text += message[i].strip()
		return text
