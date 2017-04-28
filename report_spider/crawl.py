import os
import time
import shutil
import traceback
from report_spider.spiders.Global_function import get_localtime
from report_spider.settings import SAVEDIR

now_time = get_localtime(time.strftime("%Y-%m-%d", time.localtime()))

class Spider_starter(object):

    def crawl(self):
        # running the spider
        self.HFUT()
        self.USTC()

    def run_spider(self, spider_name):
        dirname = SAVEDIR + '/' + str(now_time) + '/' + spider_name[0:len(spider_name)-3] + '/' + spider_name
        # If the dir is exist, clear the dir(today)
        if os.path.exists(dirname):
            shutil.rmtree(dirname, True)
        # If one of the spiders has error, the print_exc() function will tell us which is criminal
        try:
            os.system('scrapy crawl ' + spider_name)
        except:
            traceback.print_exc()

    def HFUT(self):
        self.run_spider('HFUT000')

    def USTC(self):
        self.run_spider('USTC001')
        self.run_spider('USTC002')
        self.run_spider('USTC003')

if __name__ == '__main__':
    starter = Spider_starter()
    starter.crawl()
