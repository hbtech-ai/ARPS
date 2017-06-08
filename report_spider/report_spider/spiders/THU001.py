# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import scrapy
from Global_function import get_localtime, print_new_number, save_messages

now_time = get_localtime(time.strftime("%Y-%m-%d", time.localtime()))
# now_time = 20170320

class THU001_Spider(scrapy.Spider):
	name = 'THU001'
	start_urls = ['http://www.cs.tsinghua.edu.cn/publish/cs/4852/index.html']
	domain = 'http://www.cs.tsinghua.edu.cn/'
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


	def parse_pages(self, response):
		title = ''
		for text in response.xpath("//h2").xpath(".//text()").extract():
			title += text.strip()

		messages = response.xpath("//div[@class='box_detail']/p").xpath(".//text()").extract()
		sign = 0
		time, address, speaker, person_introduce, content = '', '', '', '', ''
		for message in messages:
			if 'Time：' in message or 'Time:' in message:
				sign = 1
				time = self.get_messages(message, '：') if 'Time：' in message else self.get_messages(message, ':')
			elif 'Venue：' in message or 'Meeting Room：' in message or 'Location：' in message or 'Venue:' in message or 'Meeting Room:' in message or 'Location:' in message:
				sign = 2
				address = self.get_messages(message, '：') if 'Venue：' in message or 'Meeting Room：' in message or 'Location：' in message else self.get_messages(message, ':')
			elif 'Speaker：' in message or 'Speaker:' in message:
				sign = 3
				speaker = self.get_messages(message, '：') if 'Speaker：' in message else self.get_messages(message, ':')
			elif 'Bio：' in message or 'Biography：' in message or 'Bio:' in message or 'Biography:' in message:
				sign = 4
				person_introduce = self.get_messages(message, '：') if 'Bio：' in message or 'Biography：' in message else self.get_messages(message, ':')
			elif 'Abstract：' in message or 'Abstract:' in message:
				sign = 5
				content = self.get_messages(message, '：') if 'Abstract：' in message else self.get_messages(message, ':')
			else:
				if sign == 1:
					time += '\n' + message.strip()
				elif sign == 2:
					address += '\n' + message.strip()
				elif sign == 3:
					speaker += '\n' + message.strip()
				elif sign == 4:
					person_introduce += '\n' + message.strip()
				elif sign == 5:
					content += '\n' + message.strip()
				else:
					pass

		if title != '':
			self.counts += 1
			print_new_number(self.counts, 'THU', self.name)

		all_messages = save_messages('THU', self.name, title, time, address, speaker, person_introduce,
		                             content, '', response.meta['link'], response.meta['number'], u'清华大学', u'计算机科学与技术系')

		return all_messages

	def get_messages(self, messages, sign):
		text = ''
		message = messages.split(sign)[1:]
		for i in xrange(len(message)):
			if i > 0:
				text += '：'
			text += message[i].strip()
		return text
