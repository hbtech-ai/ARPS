#!/use/bin/env python3
import os

os.system('mv report_spider report_spider_temp')
os.system('scrapy startproject report_spider')

for f in os.listdir('./report_spider_temp'):
	if os.path.isdir(f):
		os.system('cp -r ./report_spider_temp/{} ./report_spider'.format(f))
	else:
		os.system('cp ./report_spider_temp/{} ./report_spider'.format(f))

os.system('rm -r -f report_spider_temp')

os.chdir('./report_spider')
os.system('bash setup.sh')

		
