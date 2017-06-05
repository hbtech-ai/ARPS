# -*- coding:utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import time
import math

SAVEDIR = '/var/lib/spider_save'

def get_localtime(times):
	year, month, day = times.split('-')
	time_number = int(year) * 10000 + int(month) * 100 + int(day)
	return time_number

def count_number(counts):
	try:
		ans = math.log10(counts)
	except:
		ans = 0
	finally:
		return int(ans)

# count the number of new reports
def print_new_number(counts, school, faculty):
	dirname = SAVEDIR + '/' + str(get_localtime(time.strftime("%Y-%m-%d", time.localtime()))) + '/' + school + '/' + faculty
	if not os.path.exists(dirname):
		os.system('mkdir -p ' + dirname)
	filename = dirname + '/&new_report_number.txt'
	with open(filename, 'w') as f:
		f.write('-' * (21+count_number(counts)) + '\n')
		f.write("We got %d new reports." % counts + '\n')
		f.write('-' * (21+count_number(counts)) + '\n')

def save_messages(school, faculty, title, time, address, speaker, person_introduce,
                  content, img_url, link, number, school_name, organizer):
	all_messages = {}

	# message that must have
	all_messages['school'] = school
	all_messages['faculty'] = faculty
	all_messages['title'] = title
	all_messages['link'] = link
	all_messages['number'] = number
	all_messages['school_name'] = school_name
	all_messages['organizer'] = organizer

	# message that may have
	if time != '':
		all_messages['time'] = time
	if address != '':
		all_messages['address'] = address
	if speaker != '':
		all_messages['speaker'] = speaker
	if person_introduce != '':
		all_messages['person_introduce'] = person_introduce
	if content != '':
		all_messages['content'] = content
	if img_url != '':
		all_messages['img_url'] = img_url

	return all_messages

def get_last(school, faculty):
	filename = os.path.join('report_spider/spiders/last_name/' + school, faculty + '.txt')
	with open(filename, 'r') as f:
		title = f.readline()
		f.close()
	return title

def sent_first(school, faculty, title):
	filename = os.path.join('report_spider/spiders/last_name/' + school, faculty + '.txt')
	with open(filename, 'w') as f:
		f.write(title)
		f.close()
	return

def get_messages(messages):
	message = messages.xpath(".//text()").extract()
	text = ''
	for each in message:
		text += each.strip()
	return text

def connect_messages(messages, sign):
	message = messages.split(sign)[1:]
	text = ''
	for i in xrange(len(message)):
		if i > 0:
			text += '：'
		text += message[i].strip()
	return text

