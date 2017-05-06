# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import scrapy
from Global_function import get_localtime, print_new_number, save_messages

now_time = get_localtime(time.strftime("%Y-%m-%d", time.localtime()))
# now_time = 20170301

class WHU001_Spider(scrapy.Spider):
	name = 'WHU001'
	start_urls = ['http://cs.whu.edu.cn/a/xueshujiangzuofabu/list_39_1.html']
	domain = 'http://cs.whu.edu.cn/'
	counts = 0

	def parse(self, response):
		messages = response.xpath("//div[@id='container']/dl/dd")

		for message in messages:
			report_url = self.domain + message.xpath(".//a/@href").extract()[0][1:]
			report_time = get_localtime(message.xpath(".//i/text()").extract()[0].split(' ')[0])
			if report_time < now_time:
				print_new_number(self.counts, 'WHU', self.name)
				return
			self.counts += 1
			yield scrapy.Request(report_url, callback=self.parse_pages, meta={'link': report_url, 'number': self.counts})

		now_number = int(response.xpath("//div[@class='page fn_clear']/ul/li[@class='thisclass']/text()").extract()[0])
		last_number = int(response.xpath("//span[@class='pageinfo']/strong")[0].xpath(".//text()").extract()[0])

		if not (now_number < last_number):
			print_new_number(self.counts, 'WHU', self.name)
			return
		new_url = 'http://cs.whu.edu.cn/a/xueshujiangzuofabu/list_39_{}.html'.format(now_number + 1)
		yield scrapy.Request(new_url, callback=self.parse)


	def parse_pages(self, response):
		messages = response.xpath("//dd[@class='info']").xpath(".//text()").extract()

		sign = 0
		title, time, address, speaker, person_introduce, content = '', '', '', '', '', ''
		for message in messages:
			if u'题目：' in message or u'题目:' in message:
				title = self.connect_message(message, '：') if u'题目：' in message else self.connect_message(message, ':')
			elif u'时间：' in message or u'时间:' in message:
				time = self.connect_message(message, '：') if u'时间：' in message else self.connect_message(message, ':')
			elif u'地点：' in message or u'地点:' in message:
				address = self.connect_message(message, '：') if u'地点：' in message else self.connect_message(message, ':')
			elif u'报告人：' in message or u'报告人:' in message:
				speaker = self.connect_message(message, '：') if u'报告人：' in message else self.connect_message(message, ':')
			elif u'简介：' in message or u'简介:' in message:
				sign = 0
				person_introduce = self.connect_message(message, '：') if u'简介：' in message else self.connect_message(message, ':')
			elif u'摘要：' in message or u'摘要:' in message:
				sign = 1
				content = self.connect_message(message, '：') if u'摘要：' in message else self.connect_message(message, ':')
			elif u'邀请人' in message:
				break
			elif not sign:
				person_introduce += message.strip()
			elif sign:
				content += message.strip()
			else:
				pass

		all_messages = save_messages('WHU', self.name, title, time, address, speaker, person_introduce,
		                             content, '', response.meta['link'], response.meta['number'])

		return all_messages

	def connect_message(self, message, sign):
		ans = ''
		message = message.split(sign)[1:]
		for i in range(len(message)):
			if i > 0:
				ans += '：'
			ans += message[i].strip()
		return ans
