# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import scrapy
from Global_function import get_localtime, print_new_number, save_messages

now_time = get_localtime(time.strftime("%Y-%m-%d", time.localtime()))
# now_time = 20170410

class USTC002_Spider(scrapy.Spider):
	name = 'USTC002'
	start_urls = ['http://ess.ustc.edu.cn/notice']
	domain = 'http://ess.ustc.edu.cn/'
	counts = 0

	def parse(self, response):
		messages = response.xpath("//div[@class='view-content']/table/tbody/tr")
		print_new_number(self.counts, 'USTC', self.name)

		sign = 0
		for i in xrange(len(messages)):
			message = messages[i].xpath(".//td")
			report_url = self.domain + message[0].xpath(".//a/@href").extract()[0][1:]
			report_class = message[1].xpath(".//text()").extract()[0].strip()
			report_time = get_localtime(message[2].xpath(".//text()").extract()[0].strip())
			if u'学术报告' not in report_class:
				continue
			if report_time < now_time:
				sign = 1
				continue
			yield scrapy.Request(report_url, callback=self.parse_pages, meta={'link': report_url, 'number': i + 1})

		# The report time of this page is not sorted, so we only stop the procedure in the end of a page.
		if sign:
			return
		now_number = response.xpath("//ul[@class='pager']/li[@class='pager-current first']/text()").extract()
		if len(now_number) == 0:
			now_number = int(response.xpath("//ul[@class='pager']/li[@class='pager-current']/text()").extract()[0])
		else:
			now_number = int(now_number[0])
		next_url = 'http://ess.ustc.edu.cn/notice?page=%d' % now_number

		yield scrapy.Request(next_url, callback=self.parse)

	def parse_pages(self, response):
		messages = response.xpath("//div[@class='inside panels-flexible-region-inside panels-flexible-region-jcjz-center-inside panels-flexible-region-inside-first']/div")

		# address
		address = self.get_message(messages[0])

		# time
		time = self.get_message(messages[1])

		# speaker
		speaker = self.get_message(messages[2])

		# other message: title, person_introduce, content
		img_url = ''
		person_introduce = ''
		title = ''
		content = ''
		for i in range(3, len(messages)):
			part_name = messages[i].xpath(".//div[@class='field-label']/text()").extract()[0]
			img_exist = messages[i].xpath(".//img")
			if len(img_exist) != 0:
				img_url = self.get_img(messages[i])
			if u'报告人简介' in part_name:
				person_introduce = self.get_message(messages[i])
			elif u'题目' in part_name:
				title = self.get_message(messages[i])
			else:
				content = self.get_message(messages[i])
			# break
		if title == '':
			title = response.xpath("//h1/text()").extract()[0]
		if img_url != '':
			img_url = self.domain + img_url[1:]

		if title != '':
			self.counts += 1
			print_new_number(self.counts, 'USTC', self.name)

		all_messages = save_messages('USTC', self.name, title, time, address, speaker, person_introduce,
		                             content, img_url, response.meta['link'], response.meta['number'], u'中国科学技术大学')

		return all_messages

	def get_message(self, messages):
		text_list = messages.xpath(".//div[@class='field-items']").xpath(".//text()").extract()
		texts = ''
		for text in text_list:
			texts += text.strip()
		return texts

	def get_img(self, messages):
		img_url = messages.xpath(".//img/@src").extract()[0]
		return img_url