# -*- coding:utf-8 -*-
import scrapy
from report_crawler.spiders.__Global_function import get_localtime
from report_crawler.spiders.__Global_variable import now_time, end_time


class THU001_Spider(scrapy.Spider):
	name = 'THU001'
	start_urls = ['http://www.cs.tsinghua.edu.cn/publish/cs/4852/index.html']
	domain = 'http://www.cs.tsinghua.edu.cn/'
	counts = 0

	def parse(self, response):
		messages = response.xpath("//div[@class='box_list']/ul/li")


		for i in xrange(len(messages)):
			report_url = self.domain + messages[i].xpath(".//a/@href").extract()[0][1:]
			report_time = get_localtime(messages[i].xpath(".//p/text()").extract()[0].strip())

			if report_time > end_time:
				continue
			if report_time < now_time:
				return
			yield scrapy.Request(report_url, callback=self.parse_pages,
			                     meta={'link': report_url, 'number': i + 1, 'publication': report_time})

	def parse_pages(self, response):
		messages = response.xpath("//div[@class='box_detail']/p")

		return {'text': messages, 'number': response.meta['number'], 'organizer': u'清华大学计算机科学与技术系',
		        'faculty': self.name, 'link': response.meta['link'], 'publication': response.meta['publication']}
