# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy
from function import get_title

key_word = '计算机视觉'
start_year, end_year = 2015, 2017
all_name = get_title()
# all_name = []
class Data_Spider(scrapy.Spider):
	name = 'Crawler'
	start_urls = ['http://s.wanfangdata.com.cn/Paper.aspx?q=关键字%3a{}+日期%3a{}-{}&f=top&p=1'.format(key_word, start_year, end_year)]

	def parse(self, response):
		messages = response.xpath("//div[@class='record-item-list']/div/div[@class='left-record']/div[@class='record-title']/a[@class='title']")

		# paper list
		for message in messages:
			paper_url = message.xpath(".//@href").extract()[0]
			paper_name = self.get_name(message)

			if paper_name in all_name:
				continue
			yield scrapy.Request(paper_url, callback=self.parse_pages)
		now_number = int(response.xpath("//p[@class='pager']/strong/text()").extract()[0])
		last_number = int(response.xpath("//p[@class='pager']/span/text()").extract()[0].split('/')[1])

		if now_number == last_number:
			return
		next_url = 'http://s.wanfangdata.com.cn/Paper.aspx?q=关键字%3a{}+日期%3a{}-{}&f=top&p={}'.format(key_word, start_year, end_year, now_number + 1)

		yield scrapy.Request(next_url, callback=self.parse)

	def parse_pages(self, response):
		paper_name = response.xpath("//h1/text()").extract()[0].strip()
		abstract = response.xpath("//div[@class='row clear zh']/div[@class='text']/text()").extract()[0].strip()

		all_messages = {'title': paper_name, 'abstract': abstract}

		return all_messages

	def get_name(self, message):
		texts = ''
		text_list = message.xpath(".//text()").extract()
		for text in text_list:
			texts += text.strip()
		return texts
