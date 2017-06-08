# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import tqdm
import scrapy
from Global_function import get_localtime, print_new_number, save_messages

now_time = get_localtime(time.strftime("%Y-%m-%d", time.localtime()))
now_time = 20100101
end_time = 20170101

class NPU001_Spider(scrapy.Spider):
	name = 'NPU001'
	start_urls = ['http://jsj.nwpu.edu.cn/index/xueshu.htm']
	domain = 'http://jsj.nwpu.edu.cn/'
	counts = 0

	def parse(self, response):
		messages = response.xpath("//table[@class='winstyle54630']").xpath(".//tr[@height='26']")

		for i in xrange(len(messages)):
			report_name = messages[i].xpath(".//td")[0].xpath(".//a/text()").extract()[0]
			if u'学术报告' not in report_name:
				continue

			report_url = self.domain + messages[i].xpath(".//td")[0].xpath(".//a/@href").extract()[0][3:]
			report_time = get_localtime(messages[i].xpath(".//td")[1].xpath(".//span/text()").extract()[0].strip().replace('/', '-'))

			if report_time > end_time:
				continue
			if report_time < now_time:
				return

			yield scrapy.Request(report_url, callback=self.parse_pages, meta={'link': report_url, 'number': i + 1})
			# return

		now_number = int(response.xpath("//tr[@valign='middle']/td/text()").extract()[0].strip().split('/')[0][-1])
		last_number = int(response.xpath("//tr[@valign='middle']/td/text()").extract()[0].strip().split('/')[-1])
		# print now_number

		# if now_number >= last_number:
		# 	return
		#
		# next_url = 'http://jsj.nwpu.edu.cn/index/xueshu/{}.htm'.format(last_number - now_number + 1)
		# # print next_url
		# yield scrapy.Request(next_url, callback=self.parse)

	def parse_pages(self, response):
		messages = response.xpath("//div[@id='vsb_content']/p")

		sign = 1
		title, time, address, speaker, person_introduce, content = '', '', '', '', '', ''
		for message in messages:
			text = self.get_messages(message)
			if u'题目：' in text or u'题目:' in text:
				title = self.connect_message(text, '：') if  u'题目：' in text else self.connect_message(text, ':')
			elif u'主持人' in text:
				continue
			elif u'时间：' in text or u'时间:' in text:
				time = self.connect_message(text, '：') if  u'时间：' in text else self.connect_message(text, ':')
			elif u'地点：' in text or u'地点:' in text:
				address = self.connect_message(text, '：') if  u'地点：' in text else self.connect_message(text, ':')
			elif u'报告人：' in text or u'报告人:' in text:
				speaker = self.connect_message(text, '：') if  u'报告人：' in text else self.connect_message(text, ':')
			elif u'简介：' in text or u'简介:' in text:
				sign = 1
				person_introduce = self.connect_message(text, '：') if  u'题目：' in text else self.connect_message(text, ':')
			elif u'摘要：' in text or u'摘要:' in text:
				sign = 2
				content = self.connect_message(text, '：') if  u'题目：' in text else self.connect_message(text, ':')
			else:
				if sign == 1:
					person_introduce += text
				elif sign == 2:
					content += text

		if title != '':
			self.counts += 1
			print_new_number(self.counts, 'NPU', self.name)

		all_messages = save_messages('NPU', self.name, title, time, address, speaker, person_introduce,
		                             content, '', response.meta['link'], response.meta['number'], u'西北工业大学', u'计算机学院')

		return all_messages

	def get_messages(self, messages):
		all_text = messages.xpath(".//text()").extract()
		texts = ''
		for text in all_text:
			texts += text.strip()
		return texts

	def connect_message(self, message, sign):
		ans = ''
		message = message.split(sign)[1:]
		for i in range(len(message)):
			if i > 0:
				ans += '：'
			ans += message[i].strip()
		return ans



