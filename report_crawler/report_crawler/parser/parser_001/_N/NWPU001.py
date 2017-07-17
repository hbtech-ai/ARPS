# -*- coding:utf-8 -*-
import re


def Parser(text, sub_linefeed):
	text = text.decode('utf-8')
	messages = {}

	# title
	title_pattern = re.compile(u"题(?:[\s\S]{0,10})目[：:.](.*?)\n", re.S)
	messages['title'] = re.findall(title_pattern, text)
	if len(messages['title']) == 1:
		messages['title'] = messages['title'][0].strip()
	else:
		messages['title'] = ''

	# time
	time_pattern = re.compile(u"时(?:[\s\S]{0,10})间[：:.](.*?)\n", re.S)
	messages['time'] = re.findall(time_pattern, text)
	if len(messages['time']) == 1:
		messages['time'] = messages['time'][0].strip()
	else:
		messages['time'] = ''

	# address
	address_pattern = re.compile(u"地(?:[\s\S]{0,10})点[：:.](.*?)\n", re.S)
	messages['address'] = re.findall(address_pattern, text)
	if len(messages['address']) == 1:
		messages['address'] = messages['address'][0].strip()
	else:
		messages['address'] = ''

	# speaker
	speaker_pattern = re.compile(u"报(?:[\s\S]{0,10})告(?:[\s\S]{0,10})人[：:.](.*?)\n", re.S)
	messages['speaker'] = re.findall(speaker_pattern, text)
	if len(messages['speaker']) == 1:
		messages['speaker'] = messages['speaker'][0].strip()
	else:
		messages['speaker'] = ''

	# abstract
	abstract_pattern = re.compile(u"(?:(?:摘[\s\S]{0,10}要)|(?:Abstract))[：:.]([\s\S]*)(?:(?:报[\s\S]{0,10}告[\s\S]{0,10}人[\s\S]{0,10}简[\s\S]{0,10}介)|(?:个[\s\S]{0,10}人[\s\S]{0,10}简[\s\S]{0,10}介)|(?:主[\s\S]{0,10}持[\s\S]{0,10}人))", re.S)
	messages['abstract'] = re.findall(abstract_pattern, text)
	if len(messages['abstract']) == 1:
		messages['abstract'] = sub_linefeed(messages['abstract'][0].strip())
	elif len(messages['abstract']) == 0:
		abstract_pattern = re.compile(u"摘[\s\S]{0,10}要[：:.]([\s\S]*)", re.S)
		messages['abstract'] = re.findall(abstract_pattern, text)
		if len(messages['abstract']) == 1:
			messages['abstract'] = sub_linefeed(messages['abstract'][0].strip())
		else:
			messages['abstract'] = ''
	else:
		messages['abstract'] = ''

	# biography
	biography_pattern = re.compile(u"人[\s\S]{0,10}简[\s\S]{0,10}介[：:.]{0,1}([\s\S]*)", re.S)
	messages['biography'] = re.findall(biography_pattern, text)
	if len(messages['biography']) == 1:
		messages['biography'] = sub_linefeed(messages['biography'][0].strip())
		if re.search(u"(摘要[：:.])|(内容简介[：:.])", messages['biography']) is not None:
			messages['biography'] = ''
	else:
		messages['biography'] = ''

	return messages
