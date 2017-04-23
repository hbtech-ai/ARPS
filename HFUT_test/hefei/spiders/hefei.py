# -*- coding:utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import scrapy
import time
import math
from settings import SAVEDIR

inf = 0x3f3f3f3f

def get_localtime(times):
	year, month, day = times.split('-')
	time_number = int(year) * 10000 + int(month) * 100 + int(day)
	return time_number

# local time
now_time = get_localtime(time.strftime("%Y-%m-%d", time.localtime()))
# now_time = 20170410

# HFUT spider for report
class HFUT_Spider(scrapy.Spider):
	name = 'HFUT'
	start_urls = ['http://news.hfut.edu.cn/list-28-1.html']
	counts = 0

	# crawling the urls
	def parse(self, response):
		basic_html = 'http://news.hfut.edu.cn'
		links = response.xpath("//div[@class='container row main in2']/div/ul/li/a/@href").extract()
		times = response.xpath("//div[@class='container row main in2']/div/ul/li/span/text()").extract()
		l = len(links)
		for i in range(l):
			told_time = get_localtime(times[i])
			if told_time < now_time:
				self.print_new_number()
				return
			self.counts += 1
			html = basic_html + links[i]
			yield scrapy.Request(html, callback=self.parse_pages, meta={'link': html})
		number = int(response.url.split('-')[-1].split('.')[0])
		last_number = response.xpath("//div[@id='pages']/a/text()").extract()[-2]
		if number < last_number:
			new_url = 'http://news.hfut.edu.cn/list-28-%d.html' % (number + 1)
			yield scrapy.Request(new_url, callback=self.parse)
		else:
			self.print_new_number()
			return

	def count_number(self):
		try:
			ans = math.log10(self.counts)
		except:
			ans = 0
		finally:
			return int(ans)

	# count the number of new reports
	def print_new_number(self):
		filename = SAVEDIR + str(get_localtime(time.strftime("%Y-%m-%d", time.localtime()))) + '/new_number.txt'
		with open(filename, 'w') as f:
			f.write('-' * (21+self.count_number()) + '\n')
			f.write("We got %d new reports." % self.counts + '\n')
			f.write('-' * (21+self.count_number()) + '\n')

	# get the information
	def parse_pages(self, response):

		title = response.xpath("//h2/text()").extract()[0]

		# other message
		summary = response.xpath("//div[@id='artibody']/p")

		time = self.get_keys(summary[0])

		address = self.get_keys(summary[1])

		major_character = self.get_keys(summary[2])

		organization = self.get_keys(summary[3])

		host = self.get_keys(summary[4])

		person_abstract, content = self.get_person_and_content(response)


		all_messages = {'title': title, 'time': time, 'address': address, 'major_character':major_character,
		                'organization': organization, 'host': host, 'person_abstract': person_abstract,
		                'content': content, 'link': response.meta['link']}
		return all_messages


	def get_person_and_content(self, response):
		person_and_content = response.xpath("//div[@id='artibody']/p//text()").extract()
		person_name, content_name = self.get_name(response)
		person_abstract = ''
		content = ''
		if person_name == '' and content_name == '':
			if person_abstract == '':
				person_abstract = u'无' + '\n'
			if content == '':
				content = u'无' + '\n'
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
				person_abstract += person_and_content[i] + '\n'
			for i in range(content_start, l):
				content += person_and_content[i] + '\n'
			if person_abstract == '':
				person_abstract = u'无' + '\n'
			if content == '':
				content = u'无' + '\n'

		return person_abstract, content

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

