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
	time_pattern = re.compile(u"间[：:.](.*?)\n")
	messages['time'] = re.findall(time_pattern, text)
	if len(messages['time']) == 1:
		messages['time'] = messages['time'][0].strip()
	else:
		messages['time'] = ''

	# address
	address_pattern = re.compile(u"点[：:.](.*?)\n")
	messages['address'] = re.findall(address_pattern, text)
	if len(messages['address']) == 1:
		messages['address'] = messages['address'][0].strip()
	else:
		messages['address'] = ''

	# speaker
	speaker_pattern = re.compile(u"讲[：:.](.*?)\n")
	messages['speaker'] = re.findall(speaker_pattern, text)
	if len(messages['speaker']) == 1:
		messages['speaker'] = messages['speaker'][0].strip()
	else:
		messages['speaker'] = ''

	# abstract
	abstract_pattern = re.compile(u"(?:摘要|Abstract)[：:.]([\s\S]*)(?:主讲人|报告人|Bio)", re.S)
	messages['abstract'] = re.findall(abstract_pattern, text)
	if len(messages['abstract']) == 1:
		messages['abstract'] = sub_linefeed(messages['abstract'][0].strip())
	else:
		abstract_pattern = re.compile(u"(?:摘要|Abstract)[：:.]([\s\S]*)", re.S)
		messages['abstract'] = re.findall(abstract_pattern, text)
		if len(messages['abstract']) == 1:
			messages['abstract'] = sub_linefeed(messages['abstract'][0].strip())
		else:
			messages['abstract'] = ''

	# biography
	biography_pattern = re.compile(u"(?:简介|Bio)[：:.]([\s\S]*)", re.S)
	messages['biography'] = re.findall(biography_pattern, text)
	if len(messages['biography']) == 1:
		messages['biography'] = sub_linefeed(messages['biography'][0].strip())
	else:
		messages['biography'] = ''

	return messages
