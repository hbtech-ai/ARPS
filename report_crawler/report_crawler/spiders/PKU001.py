# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
import time
import scrapy
from _Global_function import get_localtime
from _Global_variable import now_time, end_time


class PKU001_Spider(scrapy.Spider):
	name = 'PKU001'
	start_urls = ['http://eecs.pku.edu.cn/index.aspx?menuid=18&type=article&lanmuid=82&language=cn']
	domain = 'http://eecs.pku.edu.cn/'

	def parse(self, response):
		messages = response.xpath("//div[@class='uc_lanmu_content']/ul/li")

		for i, message in enumerate(messages):
			report_name = message.xpath(".//a/text()").extract()[0]
			if re.search(u"[：:]", report_name, re.S) != None:
				report_name = re.split(u"[：:]", report_name)[-1]

			print report_name
			report_time = get_localtime(message.xpath(".//span[@class='article_date']/text()").extract()[0])
			if report_time > end_time:
				continue
			if report_time < now_time:
				return

			report_url = self.domain + message.xpath(".//a/@href").extract()[0][1:]
			yield scrapy.Request(report_url, callback=self.parse_pages,
			                     meta={'link': report_url, 'number': i + 1, 'name': report_name, 'publication': report_time})

	def parse_pages(self, response):
		messages = response.xpath("//div[@id='Infor_Content']")

		return {'text': messages, 'number': response.meta['number'], 'organizer': u"北京大学信息科学技术学院",
		        'faculty': self.name, 'link': response.meta['link'], 'title': response.meta['name'], 'publication': response.meta['publication']}
