import os
import time
from hefei.spiders.hefei import get_localtime
from hefei.settings import SAVEDIR

def crawl():
    # get the dir for today
    dirname = SAVEDIR + str(get_localtime(time.strftime("%Y-%m-%d", time.localtime())))
    # if it is the first crawling today, we will create the new dir.
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    else:
        # clear the dir(today)
        os.system('rm -rf ' + dirname + '/*')
    # running the spider
    os.system('scrapy crawl HFUT')

if __name__ == '__main__':
    crawl()
