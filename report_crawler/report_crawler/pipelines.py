# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
import os
import time
import logging
import pymongo as pm
from parser.parser import get_information
from spiders._Global_function import get_localtime
from spiders._Global_variable import REPORT_SAVEDIR, LOGGING_SAVEDIR

# Log config
logger = logging.getLogger('Scrapy')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('../logging.log')
formatter = logging.Formatter('[%(asctime)s] - %(name)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

now_time = str(get_localtime(time.strftime("%Y-%m-%d", time.localtime())))


class ReportCrawlerPipeline(object):
    def process_item(self, item, spider):
        # self.deal_with(item)
        # return
        text = ''
        for message in item['text']:
            for each in message.xpath(".//text()").extract():
                text += each
            text += '\n'
        messages = get_information(text, item['faculty'])

        # The title come from the item.
        if item.has_key('title') and messages['title'] == '':
            messages['title'] = item['title']

        if re.sub(u"\\s+", '', messages['title']) == '' or re.sub(u"\\s+", '', messages['time']) == '' or \
                    re.sub(u"\\s+", '', messages['address']) == '' or re.sub(u"\\s+", '', messages['speaker']) == '':
            return

        dirname = os.path.join(REPORT_SAVEDIR, now_time, item['faculty'][-3:], item['faculty'][:-3])
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        filename = os.path.join(dirname, '{}.txt'.format(item['number']))

        # send the information from item to messages
        messages['faculty'] = item['faculty']
        messages['organizer'] = item['organizer']
        messages['link'] = item['link']
        messages['publication'] = item['publication']

        with open(filename, 'w') as f:
            f.write('Title：\n' + messages['title'] + '\n' * 2)
            f.write('Time：\n' + messages['time'] + '\n' * 2)
            f.write('Address：\n' + messages['address'] + '\n' * 2)
            f.write('Speaker：\n' + messages['speaker'] + '\n' * 2)
            f.write('Organizer：\n' + messages['organizer'] + '\n' * 2)

            if re.sub(u"\\s+", '', messages['biography']) != '':
                f.write('Biography：\n' + messages['biography'] + '\n' * 2)
            if re.sub(u"\\s+", '', messages['abstract']) != '':
                f.write('Abstract：\n' + messages['abstract'] + '\n' * 2)
                
        # save to db
        #self.db_save(messages)
        
        # write to log
        logger.info(messages['faculty'] + ' - ' + messages['title'])

        return

    def deal_with(self, item):
        text = ''
        for message in item['text']:
            for each in message.xpath(".//text()").extract():
                text += each
            text += '\n'
        with open('WHU001/{}.txt'.format(item['number']), 'w') as f:
            f.write(str(text))
            
    def db_save(self, messages):
        conn = pm.MongoClient('localhost', 27017)
        db = conn.get_database('report_db')
        col = db.get_collection('reports_without_label')
        col.insert(messages)
