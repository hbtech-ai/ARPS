# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import scrapy
from Global_function import get_localtime, print_new_number, save_messages

now_time = get_localtime(time.strftime("%Y-%m-%d", time.localtime()))
# now_time = 20170501

class USTC004_Spider(scrapy.Spider):
	name = 'USTC004'
	start_urls = ['http://scms.ustc.edu.cn/xwxx/xshd/']
	domain = 'http://scms.ustc.edu.cn/xwxx/xshd/'
	counts = 0

	def parse(self, response):
		messages = response.xpath("//div[@class='page2']/ul/li")
		print_new_number(self.counts, 'USTC', self.name)

		for i in xrange(len(messages)):
			report_url = self.domain + messages[i].xpath(".//a/@href").extract()[0][2:]
			report_time = get_localtime(messages[i].xpath(".//span/text()").extract()[0].strip())

			if report_time < now_time:
				return
			yield scrapy.Request(report_url, callback=self.parse_pages, meta={'link': report_url,
			                                                                  'number': i + 1,
			                                                                  'time': report_time})

	def parse_pages(self, response):
		title = ''
		img_url = self.domain + str(response.meta['time'])[0:6] + response.xpath("//p[@align='center']/img/@src").extract()[0][1:]

		if title != '':
			self.counts += 1
			print_new_number(self.counts, 'USTC', self.name)

		all_messages = save_messages('USTC', self.name, '', '', '', '', '', '', img_url,
		                             response.meta['link'], response.meta['number'], u'中国科学技术大学', u'化学与材料科学学院')

		return all_messages
