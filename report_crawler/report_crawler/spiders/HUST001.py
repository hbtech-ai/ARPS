# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
import time
import scrapy
from Global_function import get_localtime

now_time = get_localtime(time.strftime("%Y-%m-%d", time.localtime()))
# now_time = 20100101
end_time = 20991212


class HUST001_Spider(scrapy.Spider):
	name = 'HUST001'
	start_urls = ['http://www.cs.hust.edu.cn/xueshu/index?page=1']
	domain = 'http://www.cs.hust.edu.cn/'
	counts = 0

	def parse(self, response):
		messages = response.xpath("//ul[@class='rolinList']/li")

		for i, message in enumerate(messages):
			report_name = message.xpath(".//div[@class='d_new_left1']/a/text()").extract()[0]
			if re.search(u"学术(讲座|报告)", report_name) is None:
				continue
			report_url = self.domain + message.xpath(".//div[@class='d_new_left1']/a/@href").extract()[0]
			report_time = get_localtime(message.xpath(".//div[@class='d_new_right1']/text()").extract()[0])

			if report_time > end_time:
				continue
			if report_time < now_time:
				return

			yield scrapy.Request(report_url, callback=self.parse_pages, meta={'number': i + 1})

		numbers = response.xpath("//div[@class='btn_page2']/text()").extract()[0].replace('\n', '').replace(' ', '').strip()
		now_number = int(numbers.split('/')[0][1:])
		last_number = int(numbers.split('/')[1][:-1])

		if now_number == 1:
			return

		next_url = 'http://www.cs.hust.edu.cn/xueshu/index?page={}'.format(now_number + 1)
		yield scrapy.Request(next_url, callback=self.parse)

	def parse_pages(self, response):
		messages = response.xpath("//div[@class='show_cont']").xpath(".//text()").extract()

		return {'text': messages, 'number': response.meta['number'], 'organizer': u'华中科技大学计算机科学与技术学院', 'faculty': self.name}
