# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import scrapy
from Global_function import get_localtime

now_time = get_localtime(time.strftime("%Y-%m-%d", time.localtime()))
# now_time = 20100101
end_time = 20991212


class NPU001_Spider(scrapy.Spider):
	name = 'NWPU001'
	start_urls = ['http://jsj.nwpu.edu.cn/index/xueshu.htm']
	domain = 'http://jsj.nwpu.edu.cn/'
	counts = 0

	def parse(self, response):
		messages = response.xpath("//table[@class='winstyle54630']").xpath(".//tr[@height='26']")

		for i in xrange(len(messages)):
			report_name = messages[i].xpath(".//td")[0].xpath(".//a/text()").extract()[0]
			if u'学术报告' not in report_name:
				continue

			report_url = self.domain + messages[i].xpath(".//td")[0].xpath(".//a/@href").extract()[0][3:]
			report_time = get_localtime(messages[i].xpath(".//td")[1].xpath(".//span/text()").extract()[0].strip().replace('/', '-'))

			if report_time > end_time:
				continue
			if report_time < now_time:
				return

			yield scrapy.Request(report_url, callback=self.parse_pages, meta={'link': report_url, 'number': i + 1})

	def parse_pages(self, response):
		messages = response.xpath("//div[@id='vsb_content']")

		return {'text': messages, 'number': response.meta['number'], 'organizer': u'西北工业大学计算机学院', 'faculty': self.name}
