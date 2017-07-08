# -*- coding:utf-8 -*-
from __future__ import print_function

import os
import time
import shutil
import traceback
from report_crawler.spiders.Global_function import get_localtime

now_time = get_localtime(time.strftime("%Y-%m-%d", time.localtime()))

SAVEDIR = "/var/lib/spider_save"
DATADIR = SAVEDIR + '/' + str(now_time)


class Spider_starter(object):

	def crawl(self):
		self.X001()

	def run_spider(self, spider_name):
		dirname = SAVEDIR + '/' + str(now_time) + '/' + spider_name[len(spider_name)-3:] + '/' + spider_name[0:len(spider_name)-3]
		# If the dir is exist, clear the dir(today)
		if os.path.exists(dirname):
			shutil.rmtree(dirname, True)
		# If one of the spiders has error, the print_exc() function will tell us which is criminal
		try:
			if not os.path.exists(DATADIR):
				os.mkdir(SAVEDIR + '/' + str(now_time))
			os.system('scrapy crawl ' + spider_name)
		except:
			traceback.print_exc()

	def X001(self):
		self.run_spider('ECNU001')
		self.run_spider('NWPU001')
		self.run_spider('SCU001')
		self.run_spider('SDU001')
		self.run_spider('SYSU001')
		self.run_spider('THU001')
		self.run_spider('WHU001')

if __name__ == '__main__':
	starter = Spider_starter()
	starter.crawl()
