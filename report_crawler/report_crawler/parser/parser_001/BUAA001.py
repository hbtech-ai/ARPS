# -*- coding:utf-8 -*-
import re


def Parser(text, sub_linefeed):
	text = text.decode('utf-8')
	messages = {}

	# title
	title_pattern = re.compile(u"(?:(?:题(?:.*?){0,1}目)|(?:Title))[：:. ](.*?)\n", re.S)
	messages['title'] = re.findall(title_pattern, text)
	if len(messages['title']) == 1:
		messages['title'] = messages['title'][0].strip()
	else:
		messages['title'] = ''

	# time
	time_pattern = re.compile(u"时(?:.*?){0,1}间[：:. ](.*?)\n", re.S)
	messages['time'] = re.findall(time_pattern, text)
	if len(messages['time']) == 1:
		messages['time'] = messages['time'][0].strip()
	else:
		messages['time'] = ''

	# address
	address_pattern = re.compile(u"地(?:.*?){0,1}点[：:.](.*?)\n", re.S)
	messages['address'] = re.findall(address_pattern, text)
	if len(messages['address']) == 1:
		messages['address'] = messages['address'][0].strip()
	else:
		messages['address'] = ''

	# speaker
	speaker_pattern = re.compile(u"(?:(?:主(?:.*?){0,1}讲)|(?:报(?:.*?){0,1}告))(?:.*?){0,1}人[：:.](.*?)\n", re.S)
	messages['speaker'] = re.findall(speaker_pattern, text)
	if len(messages['speaker']) == 1:
		messages['speaker'] = messages['speaker'][0].strip()
	else:
		messages['speaker'] = ''

	# abstract
	abstract_pattern = re.compile(u"(?:(?:摘(?:.*?){0,1}要)|(?:内(?:.*?){0,1}容)|(?:Bio))[：:.]([\s\S]*)(?:(?:(?:报(?:.*?){0,1}告)|(?:主(?:.*?){0,1}讲)人)|(?:讲(?:.*?){0,1}者)|(?:Abstract))(?:.*?){0,1}[：:.]", re.S)
	messages['abstract'] = re.findall(abstract_pattern, text)
	if len(messages['abstract']) == 1:
		messages['abstract'] = sub_linefeed(messages['abstract'][0].strip())
	else:
		abstract_pattern = re.compile(u"(?:(?:摘(?:.*?){0,1}要)|(?:内(?:.*?){0,1}容)|(?:Bio))[：:.]([\s\S]*)", re.S)
		messages['abstract'] = re.findall(abstract_pattern, text)
		if len(messages['abstract']) == 1:
			messages['abstract'] = sub_linefeed(messages['abstract'][0].strip())
		else:
			messages['abstract'] = ''

	# biography
	biography_pattern = re.compile(u"(?:(?:者|人)(?:简(?:.*?){0,1}介|介(?:.*?){0,1}绍)|Abstract)[：:.]([\s\S]*)(?:(?:(?:报告)|(?:讲座))(?:(?:摘要)|(?:内容)|(?:简介))|Bio)[：:.]", re.S)
	messages['biography'] = re.findall(biography_pattern, text)
	if len(messages['biography']) == 1:
		messages['biography'] = sub_linefeed(messages['biography'][0].strip())
	else:
		biography_pattern = re.compile(u"(?:(?:者|人)(?:(?:简(?:.*?){0,1}介)|(?:介(?:.*?){0,1}绍))|Abstract)[：:.]([\s\S]*)", re.S)
		messages['biography'] = re.findall(biography_pattern, text)
		if len(messages['biography']) == 1:
			messages['biography'] = sub_linefeed(messages['biography'][0].strip())
		else:
			messages['biography'] = ''

	return messages

