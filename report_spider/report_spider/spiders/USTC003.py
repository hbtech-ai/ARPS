# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import scrapy
from Global_function import get_localtime, print_new_number, save_messages

now_time = get_localtime(time.strftime("%Y-%m-%d", time.localtime()))
# now_time = 20170420

class USTC003_Spider(scrapy.Spider):
	name = 'USTC003'
	start_urls = ['http://math.ustc.edu.cn/new/list.php?fid=35&page=1']
	domain = 'http://math.ustc.edu.cn/new/'
	counts = 0

	def parse(self, response):
		messages = response.xpath("//td[@class='middle']").xpath(".//tr")

		for message in messages:
			report_title = message.xpath(".//span/a/text()").extract()[0]
			report_url = self.domain + message.xpath(".//span/a/@href").extract()[0]
			report_time = get_localtime(message.xpath(".//span/a/text()").extract()[-1].strip('()'))
			if report_time < now_time:
				print_new_number(self.counts, 'USTC', self.name)
				return
			if u'本周报告' in report_title:
				continue
			self.counts += 1
			yield scrapy.Request(report_url, callback=self.parse_pages, meta={'link': report_url})

		now_number = int(response.xpath("//a[@href='#']").xpath(".//text()").extract()[0])
		last_number = int(response.xpath("//a[@href='#']").xpath(".//text()").extract()[-1][1:])
		if now_number > last_number:
			print_new_number(self.counts, 'USTC', self.name)
			return
		next_url = 'http://math.ustc.edu.cn/new/list.php?fid=35&page=%d' % (now_number + 1)

		yield scrapy.Request(next_url, callback=self.parse)

	# get the report message
	def parse_pages(self, response):
		messages = response.xpath("//table[@width='96%']").xpath(".//td[@align='left' and @class='dh01']").xpath(".//text()").extract()

		sign = -1
		title = ''; time = ''; address = ''; speaker = ''; content = ''
		# the order of message is not stable, so we can only use the key words. And some messages not only have one section.
		for i in range(len(messages) - 1):
			if 'Title' in messages[i] or u'题目' in messages[i]:
				sign = 0
				title += self.get_message(messages[i])
			elif 'Time' in messages[i] or u'时间' in messages[i]:
				sign = 1
				time += self.get_message(messages[i])
			elif 'Room' in messages[i] or u'地点' in messages[i]:
				sign = 2
				address += self.get_message(messages[i])
			elif 'Speaker' in messages[i] or u'报告人' in messages[i]:
				sign = 3
				speaker += self.get_message(messages[i])
			elif 'Abstract' in messages[i] or u'摘要' in messages[i]:
				sign = 4
				content += self.get_message(messages[i])
			elif '：' not in messages[i] and ':' not in messages[i]:
				if sign == 0:
					title += messages[i]
				elif sign == 1:
					time += messages[i]
				elif sign == 2:
					address += messages[i]
				elif sign == 3:
					speaker += messages[i]
				else:
					content += messages[i]

		all_messages = save_messages('USTC', self.name, title, time, address, speaker,
		                             '', content, '', response.meta['link'])

		return all_messages

	# Sometimes they use ':', sometimes '：'
	def get_message(self, messages):
		message = messages.split('：')
		if len(message) > 1:
			return self.connent_message(messages, '：')
		else:
			message = messages.split(':')
			if len(message) > 1:
				return self.connent_message(messages, ':')
			else:
				return message[0].strip()

	# connent multi secitons to one message
	def connent_message(self, messages, sign):
		message_list = messages.split(sign)
		message = ''
		for i in range(len(message_list)):
			if u'欢迎' in messages[i]:
				continue
			message += message_list[i].strip()
		return message
