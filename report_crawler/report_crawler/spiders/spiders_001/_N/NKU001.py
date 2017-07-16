# -*- coding:utf-8 -*-
import re
import scrapy
from report_crawler.spiders.__Global_function import get_localtime
from report_crawler.spiders.__Global_variable import now_time, end_time


class NKU001_Spider(scrapy.Spider):
	name = 'NKU001'
	start_urls = ['http://cc.nankai.edu.cn/Infomation/NewsList.aspx?newstype=14&cid=1']
	domain = 'http://cc.nankai.edu.cn/Infomation/'

	def parse(self, response):
		messages = response.xpath("//table[@id='dgrdNews']/tr")

		for i, message in enumerate(messages[:len(messages) - 1]):
			report_name = message.xpath(".//a/text()").extract()[0]
			if re.search(u"讲座|报告", report_name) is None:
				continue

			report_time = get_localtime("20" + message.xpath(".//td")[2].xpath(".//text()").extract()[0].split(' ')[0])
			if report_time > end_time:
				continue
			if report_time < now_time:
				return

			report_url = self.domain + message.xpath(".//a/@href").extract()[0]
			yield scrapy.Request(report_url, callback=self.parse_pages,
			                     meta={'link': report_url, 'number': i + 1, 'publication': report_time})

	def parse_pages(self, response):
		messages = response.xpath("//span[@id='lblContent']")

		return {'text': messages, 'number': response.meta['number'], 'organizer': u'南开大学计算机与控制工程学院',
		        'faculty': self.name, 'link': response.meta['link'], 'publication': response.meta['publication'],
		        'location': u"华北:天津市"}
