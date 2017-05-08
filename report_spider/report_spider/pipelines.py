# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import time
import requests
from settings import SAVEDIR
from spiders.Global_function import get_localtime

now_time = str(get_localtime(time.strftime("%Y-%m-%d", time.localtime())))
class ReportSpiderPipeline(object):
    def process_item(self, item, spider):
        # find or make the dir for school and faculty
        dirname = SAVEDIR + '/' + now_time + '/' + item['school'] + '/' + item['faculty'] + '/' + str(item['number'])
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        filename = dirname + '/' + str(item['number'])
        # if the img exist, we should save the img
        if item.has_key('img_url'):
            self.img_save(item['img_url'], filename)
        # text save
        self.text_save(item, filename)
        return item

    def text_save(self, all_messages, filename):
        filename += '.txt'
        # We only save six things: title, speaker, time, address, person_introduce, content
        with open(filename, 'w') as f:
            # title must have
            f.write('Title:' + '\n' + all_messages['title'] + '\n' * 2)
            # others may not have
            if all_messages.has_key('speaker'):
                f.write('Speaker: ' + '\n' + all_messages['speaker'] + '\n' * 2)
            if all_messages.has_key('time'):
                f.write('Time: ' + '\n' + all_messages['time'] + '\n' * 2)
            if all_messages.has_key('address'):
                f.write('Address: ' + '\n' + all_messages['address'] + '\n' * 2)
            if all_messages.has_key('person_introduce'):
                f.write('Person_introduce: ' + '\n' + all_messages['person_introduce'] + '\n' * 2)
            if all_messages.has_key('content'):
                f.write('Content: ' + '\n' + all_messages['content'] + '\n' * 2)

    def img_save(self, img_url, filename):
        # get img
        img = requests.get(img_url)
        # save
        filename += '.jpg'
        with open(filename, 'w') as f:
            f.write(img.content)
            f.close()
