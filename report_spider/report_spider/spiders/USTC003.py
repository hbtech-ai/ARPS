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
		print_new_number(self.counts, 'USTC', self.name)

		for i in xrange(len(messages)):
			report_title = messages[i].xpath(".//span/a/text()").extract()[0]
			report_url = self.domain + messages[i].xpath(".//span/a/@href").extract()[0]
			report_time = get_localtime(messages[i].xpath(".//span/a/text()").extract()[-1].strip('()'))
			if report_time < now_time:
				return
			if u'本周报告' in report_title:
				continue
			yield scrapy.Request(report_url, callback=self.parse_pages, meta={'link': report_url, 'number': i + 1})

		now_number = int(response.xpath("//a[@href='#']").xpath(".//text()").extract()[0])
		last_number = int(response.xpath("//a[@href='#']").xpath(".//text()").extract()[-1][1:])
		if now_number > last_number:
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
			if 'Title：' in messages[i] or u'题目：' in messages[i] or 'Title:' in messages[i] or u'题目:' in messages[i]:
				sign = 0
				title += self.get_message(messages[i], '：') if 'Title：' in messages[i] or u'题目：' in messages[i] else self.get_message(messages[i], ':')
			elif 'Time：' in messages[i] or u'时间：' in messages[i] or 'Time:' in messages[i] or u'时间:' in messages[i]:
				sign = 1
				time += self.get_message(messages[i], '：') if 'Time：' in messages[i] or u'时间：' in messages[i] else self.get_message(messages[i], ':')
			elif 'Place：' in messages[i] or u'地点：' in messages[i] or 'Place:' in messages[i] or u'地点:' in messages[i]:
				sign = 2
				address += self.get_message(messages[i], '：') if 'Place：' in messages[i] or u'地点：' in messages[i] else self.get_message(messages[i], ':')
			elif 'Speaker：' in messages[i] or u'报告人：' in messages[i] or 'Speaker:' in messages[i] or u'报告人:' in messages[i]:
				sign = 3
				speaker += self.get_message(messages[i], '：') if 'Speaker：' in messages[i] or u'报告人：' in messages[i] else self.get_message(messages[i], ':')
			elif 'Abstract：' in messages[i] or u'摘要：' in messages[i] or 'Abstract:' in messages[i] or u'摘要:' in messages[i]:
				sign = 4
				content += self.get_message(messages[i], '：') if 'Abstract：' in messages[i] or u'摘要：' in messages[i] else self.get_message(messages[i], ':')
			else:
				if u'欢迎' in messages[i]:
					pass
				elif sign == 0:
					title += messages[i]
				elif sign == 1:
					time += messages[i]
				elif sign == 2:
					address += messages[i]
				elif sign == 3:
					speaker += messages[i]
				else:
					content += messages[i]

		if title != '':
			self.counts += 1
			print_new_number(self.counts, 'USTC', self.name)

		all_messages = save_messages('USTC', self.name, title, time, address, speaker, '',
		                             content, '', response.meta['link'], response.meta['number'], u'中国科学技术大学')

		return all_messages

	# Sometimes they use ':', sometimes '：'
	def get_message(self, messages, sign):
		message = messages.split(sign)[1:]
		text = ''
		for i in xrange(len(message)):
			if i > 0:
				text += '：'
			text += message[i].strip()
		return text

	# connent multi secitons to one message
	def connent_message(self, messages, sign):
		message_list = messages.split(sign)
		message = ''
		for i in range(1, len(message_list)):
			if u'欢迎' in messages[i]:
				continue
			message += message_list[i].strip()
		return message
