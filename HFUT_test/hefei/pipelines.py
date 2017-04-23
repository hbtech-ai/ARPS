# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
from settings import SAVEDIR
from spiders.hefei import get_localtime

dirname = SAVEDIR + str(get_localtime(time.strftime("%Y-%m-%d", time.localtime()))) + '/'
class HefeiPipeline(object):
    def process_item(self, item, spider):
        filename = dirname + item['link'].split('/')[-1].split('-')[2] + '.txt'
        self.save(item, filename)
        return item

    def save(self, all_messages, filename):
        with open(filename, 'w') as f:
            f.write('Title: ' + all_messages['title'] + '\n\n')
            f.write('Time: ' + all_messages['time'] + '\n\n')
            f.write('Address: ' + u'合肥工业大学' + all_messages['address'] + '\n\n')
            f.write('Major_character: ' + all_messages['major_character'] + '\n\n')
            f.write('Organization: ' + all_messages['organization'] + '\n\n')
            f.write('Host: ' + u'合肥工业大学' + all_messages['host'] + '\n\n')
            f.write('Person_abstract: ' + '\n' + all_messages['person_abstract'] + '\n')
            f.write('Content: ' + '\n' + all_messages['content'] + '\n\n')
