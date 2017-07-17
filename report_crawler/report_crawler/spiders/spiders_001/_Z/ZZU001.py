# -*- coding:utf-8 -*-
import re
import scrapy
from report_crawler.spiders.__Global_function import get_localtime
from report_crawler.spiders.__Global_variable import now_time, end_time


class ZZU001_Spider(scrapy.Spider):
	name = 'ZZU001'
	start_urls = ['http://www5.zzu.edu.cn/ie/xygg.htm']
	domain = 'http://www5.zzu.edu.cn/ie/'

	def parse(self, response):
		messages = response.xpath("//div[@class='new']/div")

		for i, message in enumerate(messages[:-1]):
			report_name = message.xpath(".//a/@title").extract()[0]
			if re.search(u"(报告|讲座)", report_name) is None:
				continue

			report_time = get_localtime(message.xpath("div/span/text()").extract()[0].strip().strip("()"))
			if report_time > end_time:
				continue
			if report_time < now_time:
				return

			report_url = self.domain + message.xpath(".//a/@href").extract()[0]
			yield scrapy.Request(report_url, callback=self.parse_pages,
			                     meta={'link': report_url, 'number': i + 1, 'publication': report_time, 'title': report_name})

	def parse_pages(self, response):
		messages = response.xpath("//div[@class='v_news_content']")

		return {'text': messages, 'number': response.meta['number'], 'organizer': u"郑州大学信息工程学院",
		        'faculty': self.name, 'link': response.meta['link'], 'publication': response.meta['publication'],
		        'location': u"华中:河南省-郑州市", 'title': response.meta['title']}
