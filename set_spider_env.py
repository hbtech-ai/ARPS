#!/use/bin/env python3
import os, sys

spider_name = sys.argv[1]

os.system('mv {0} {0}_temp'.format(spider_name))
os.system('scrapy startproject {}'.format(spider_name))

for f in os.listdir('./{}_temp'.format(spider_name)):
	if os.path.isdir(f):
		os.system('cp -r ./{0}_temp/{1} ./{0}'.format(spider_name, f))
	else:
		os.system('cp ./{0}_temp/{1} ./{0}'.format(spider_name, f))

os.system('rm -r -f {}_temp'.format(spider_name))

os.chdir('./{}'.format(spider_name))
os.system('bash setup.sh')

		
