# -*- coding:utf-8 -*-
import re


def Parser(text, sub_linefeed):
	text = text.decode('utf-8')
	messages = {}
	
	# title
	title_pattern = re.compile(u"目[：:.](.*?)\n")
	messages['title'] = re.findall(title_pattern, text)
	if len(messages['title']) == 1:
		messages['title'] = messages['title'][0].strip()
	else:
		messages['title'] = ''
	
	# time
	time_pattern = re.compile(u"间[：:.](.*?)\n", re.S)
	messages['time'] = re.findall(time_pattern, text)
	if len(messages['time']) == 1:
		messages['time'] = messages['time'][0].strip()
	else:
		messages['time'] = ''
	
	# speaker
	speaker_pattern = re.compile(u"人[：:.](.*?)\n", re.S)
	messages['speaker'] = re.findall(speaker_pattern, text)
	if len(messages['speaker']) == 1:
		messages['speaker'] = messages['speaker'][0].strip()
	else:
		messages['speaker'] = ''
	
	# address
	address_pattern = re.compile(u"点[：:.](.*?)\n", re.S)
	messages['address'] = re.findall(address_pattern, text)
	if len(messages['address']) == 1:
		messages['address'] = messages['address'][0].strip()
	else:
		messages['address'] = ''
	
	# biography
	biography_pattern = re.compile(u"介绍[：:.]\s*(.*?)\n", re.S)
	messages['biography'] = re.findall(biography_pattern, text)
	if len(messages['biography']) == 1:
		messages['biography'] = sub_linefeed(messages['biography'][0].strip())
	else:
		messages['biography'] = ''
		
	# abstract
	messages['abstract'] = ''
	
	return messages
