# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import scrapy
from Global_function import get_localtime, print_new_number, save_messages

now_time = get_localtime(time.strftime("%Y-%m-%d", time.localtime()))
# now_time = 20170419

class USTC001_Spider(scrapy.Spider):
	name = 'USTC001'
	start_urls = ['http://cs.ustc.edu.cn/xwxx/xshd/']
	domain = 'http://cs.ustc.edu.cn/xwxx/xshd/'
	counts = 0

	def parse(self, response):
		links = response.xpath("//li[@width='30%']/a/@href").extract()
		times = response.xpath("//li[@width='30%']/span/text()").extract()
		print_new_number(self.counts, 'USTC', self.name)

		l = len(links)
		for i in range(l):
			report_url = self.domain + links[i][2:]
			report_time = get_localtime(times[i])

			if report_time < now_time:
				return
			yield scrapy.Request(report_url, callback=self.parse_pages, meta={'link': report_url, 'number': i + 1})

	def parse_pages(self, response):
		# title
		title = response.xpath("//td[@height='30' and @align='center']/h4/text()").extract()[0]

		# crawling img
		url = response.xpath("//td[@align='left' and @class='cc']").xpath('.//img/@src').extract()[0][2:]

		# get img url
		img_domain = response.meta['link'].split('/')
		img_url = ''
		for i in range(len(img_domain) - 1):
			img_url += img_domain[i] + '/'
		img_url += url

		if title != '':
			self.counts += 1
			print_new_number(self.counts, 'USTC', self.name)

		# save
		all_messages = save_messages('USTC', self.name, title, '', '', '', '', '', img_url,
		                             response.meta['link'], response.meta['number'], u'中国科学技术大学')

		return all_messages