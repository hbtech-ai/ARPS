# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
import time
import scrapy
from _Global_function import get_localtime
from _Global_variable import now_time, end_time

# now_time = get_localtime(time.strftime("%Y-%m-%d", time.localtime()))
# now_time = 20100101
# end_time = 20991212


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

