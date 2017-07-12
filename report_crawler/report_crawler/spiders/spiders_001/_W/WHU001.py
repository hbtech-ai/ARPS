# -*- coding:utf-8 -*-
import scrapy
from report_crawler.spiders.__Global_function import get_localtime
from report_crawler.spiders.__Global_variable import now_time, end_time


class WHU001_Spider(scrapy.Spider):
	name = 'WHU001'
	start_urls = ['http://cs.whu.edu.cn/a/xueshujiangzuofabu/list_39_1.html']
	domain = 'http://cs.whu.edu.cn/'
	counts = 0

	def parse(self, response):
		messages = response.xpath("//div[@id='container']/dl/dd")

		for i in xrange(len(messages)):
			report_url = self.domain + messages[i].xpath(".//a/@href").extract()[0][1:]
			report_time = get_localtime(messages[i].xpath(".//i/text()").extract()[0].split(' ')[0])

			if report_time > end_time:
				continue
			if report_time < now_time:
				return
			yield scrapy.Request(report_url, callback=self.parse_pages,
			                     meta={'link': report_url, 'number': i + 1, 'publication': report_time})

	def parse_pages(self, response):
		messages = response.xpath("//dd[@class='info']")

		return {'text': messages, 'number': response.meta['number'], 'organizer': u'武汉大学计算机学院',
		        'faculty': self.name, 'link': response.meta['link'], 'publication': response.meta['publication']}
