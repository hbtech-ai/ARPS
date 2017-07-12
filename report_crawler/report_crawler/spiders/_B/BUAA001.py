# -*- coding:utf-8 -*-
import scrapy
from report_crawler.spiders.__Global_function import get_localtime
from report_crawler.spiders.__Global_variable import now_time, end_time


class BUAA001_Spider(scrapy.Spider):
	name = 'BUAA001'
	start_urls = ['http://scse.buaa.edu.cn/buaa-css-web/navigationTemplateListAction.action?firstSelId=6e011b46-2c70-4f68-a633-ec51f42b4718&secondSelId=ACADEMIC_EXCHANGE_ACTIVITIES&thirdSelId=&language=0']
	domain = 'http://scse.buaa.edu.cn/'
	counts = 0

	def parse(self, response):
		messages = response.xpath("//div[@class='article_list']/ul/li")

		for i, message in enumerate(messages):
			report_name = message.xpath(".//a/text()").extract()[0]
			if u"学术报告预告" not in report_name:
				continue

			report_time = get_localtime(message.xpath(".//div[@class='p_date']/text()").extract()[0].replace('/', '-'))
			if report_time > end_time:
				continue
			if report_time < now_time:
				return

			report_url = self.domain + message.xpath(".//a/@href").extract()[0][1:]
			yield scrapy.Request(report_url, callback=self.parse_pages,
			                     meta={'link': report_url, 'number': i + 1, 'publication': report_time})

	def parse_pages(self, response):
		messages = response.xpath("//div[@class='article_content_div']")

		return {'text': messages, 'number': response.meta['number'], 'organizer': u"北京航空航天大学计算机学院",
		        'faculty': self.name, 'link': response.meta['link'], 'publication': response.meta['publication']}

