# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import scrapy
from Global_function import get_localtime, print_new_number, save_messages, get_last, sent_first, connect_messages, get_messages

now_time = get_localtime(time.strftime("%Y-%m-%d", time.localtime()))

class THU007_Spider(scrapy.Spider):
	name = 'THU007'
	start_urls = ['http://www.phys.tsinghua.edu.cn/publish/phy/5286/index.html']
	domain = 'http://www.phys.tsinghua.edu.cn/'
	counts = 0
	last_name = get_last('THU', name)

	def parse(self, response):
		messages = response.xpath("//div[@class='box_info_list']/ul/li")
		report_num = 0

		print_new_number(self.counts, 'THU', self.name)
		for i in xrange(len(messages)):
			report_num += 1
			name = messages[i].xpath(".//a/text()").extract()
			report_name = name[0].strip() + name[1].strip()
			report_url = self.domain + messages[i].xpath(".//a/@href").extract()[0][1:]

			if u'安排预告' in report_name:
				report_num -= 1
				continue
			if report_name == self.last_name:
				return
			elif report_num == 1:
				sent_first('THU', self.name, report_name)

			yield scrapy.Request(report_url, callback=self.parse_pages, meta={'link': report_url, 'number': i + 1})

	def parse_pages(self, response):
		messages = response.xpath("//div[@class='box_detail']/p")

		sign = 0
		title, time, address, content = '', '', '', ''
		speaker = ''
		for message in messages:
			text = get_messages(message)
			if '题目：' in text or '题目:' in text:
				title = connect_messages(text, '：') if '题目：' in text else connect_messages(text, ':')
			elif '时间：' in text or '时间:' in text:
				time = connect_messages(text, '：') if '时间：' in text else connect_messages(text, ':')
			elif '地点：' in text or '地点:' in text:
				address = connect_messages(text, '：') if '地点：' in text else connect_messages(text, ':')
			if '人：' in text or '人:' in text:
				speaker = connect_messages(text, '：') if '人：' in text else connect_messages(text, ':')
			elif '摘要：' in text or '摘要:' in text:
				sign = 1
				content = connect_messages(text, '：') if '摘要：' in text else connect_messages(text, ':')
			elif sign == 1:
				content += text.strip()

		if title != '':
			self.counts += 1
			print_new_number(self.counts, 'THU', self.name)

		all_messages = save_messages('THU', self.name, title, time, address, speaker, '',
		                             content, '', response.meta['link'], response.meta['number'], u'清华大学')

		return all_messages





