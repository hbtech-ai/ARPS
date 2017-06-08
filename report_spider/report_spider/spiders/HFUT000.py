# -*- coding:utf-8 -*-

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import scrapy
import time
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from report_spider.spiders.Global_function import get_localtime, print_new_number, save_messages

inf = 0x3f3f3f3f

# local time
# now_time = get_localtime(time.strftime("%Y-%m-%d", time.localtime()))
now_time = 20170420

# HFUT spider for report
class HFUT000_Spider(scrapy.Spider):
	name = 'HFUT000'
	start_urls = ['http://news.hfut.edu.cn/list-28-1.html']
	counts = 0
	domain = 'http://news.hfut.edu.cn/'

	# crawling the urls
	def parse(self, response):
		links = response.xpath("//div[@class='container row main in2']/div/ul/li/a/@href").extract()
		times = response.xpath("//div[@class='container row main in2']/div/ul/li/span/text()").extract()

		l = len(links)
		print_new_number(self.counts, 'HFUT', self.name)
		for i in range(l):
			report_time = get_localtime(times[i])

			if report_time < now_time:
				return
			report_url = self.domain + links[i][1:]
			yield scrapy.Request(report_url, callback=self.parse_pages, meta={'link': report_url, 'number': i + 1})

		number = int(response.url.split('-')[-1].split('.')[0])
		last_number = response.xpath("//div[@id='pages']/a/text()").extract()[-2]
		if number < last_number:
			new_url = 'http://news.hfut.edu.cn/list-28-%d.html' % (number + 1)
			yield scrapy.Request(new_url, callback=self.parse)
		else:
			return

	# get the information
	def parse_pages(self, response):

		title = response.xpath("//h2/text()").extract()[0]

		# other message
		summary = response.xpath("//div[@id='artibody']/p")

		time = self.get_keys(summary[0])

		address = self.get_keys(summary[1])

		speaker = self.get_keys(summary[2])

		# We don't need organization and host
		# organization = self.get_keys(summary[3])

		# host = self.get_keys(summary[4])

		person_introduce, content = self.get_person_and_content(response)

		if title != '':
			self.counts += 1
			print_new_number(self.counts, 'HFUT', self.name)

		all_messages = save_messages('HFUT', self.name, title, time, address, speaker, person_introduce,
		                             content, '', response.meta['link'], response.meta['number'], u'合肥工业大学', u'合肥工业大学')

		return all_messages


	def get_person_and_content(self, response):
		person_and_content = response.xpath("//div[@id='artibody']/p//text()").extract()
		person_name, content_name = self.get_name(response)
		person_introduce = ''
		content = ''
		if person_name == '' and content_name == '':
			pass
		else:
			person_position = inf
			content_position = inf
			l = len(person_and_content)
			for i in range(l):
				information = person_and_content[i]
				if information == person_name:
					person_position = i
				elif information == content_name:
					content_position = i
			person_start = min(person_position+2, l)
			person_end = min(content_position, l)
			content_start = min(content_position+2, l)
			for i in range(person_start, person_end):
				person_introduce += person_and_content[i] + '\n'
			for i in range(content_start, l):
				content += person_and_content[i] + '\n'

		return person_introduce, content

	def get_keys(self, message):
		finder = message.xpath(".//span")
		things = finder.xpath("./text()").extract()
		if len(things) == 3 or len(things) == 5:
			keys = things[-1]
		else:
			keys = things[-1][1:]
		return keys

	def get_name(self, response):
		strong_words = response.xpath("//div[@id='artibody']/p/span/strong")
		l = len(strong_words)
		person_name = ''
		content_name = ''
		if l == 11:
			person_name = strong_words[-2].xpath(".//span/text()").extract()[0]
			content_name = strong_words[-1].xpath(".//span/text()").extract()[0]
		elif l == 10:
			unknown = strong_words[-1].xpath(".//span/text()").extract()[0]
			if u'内容' in unknown:
				content_name = unknown
			else:
				person_name = unknown
		else:
			pass
		return person_name, content_name
