# -*- coding:utf-8 -*-
import re

def Parser(text, sub_linefeed):
	text = text.decode('utf-8')
	messages = {}

	# title
	title_pattern = re.compile(u"主[ ]{0,}题[：:. ](.*?)\n", re.S)
	messages['title'] = re.findall(title_pattern, text)
	if len(messages['title']) == 1:
		messages['title'] = messages['title'][0].strip()
	else:
		messages['title'] = ''

	# time
	time_pattern = re.compile(u"时[ ]{0,}间[：:. ](.*?)\n", re.S)
	messages['time'] = re.findall(time_pattern, text)
	if len(messages['time']) == 1:
		messages['time'] = messages['time'][0].strip()
	else:
		messages['time'] = ''

	# address
	address_pattern = re.compile(u"地[ ]{0,}点[：:.](.*?)\n", re.S)
	messages['address'] = re.findall(address_pattern, text)
	if len(messages['address']) == 1:
		messages['address'] = messages['address'][0].strip()
	else:
		messages['address'] = ''

	# speaker
	speaker_pattern = re.compile(u"讲[ ]{0,}师[：:.](.*?)\n", re.S)
	messages['speaker'] = re.findall(speaker_pattern, text)
	if len(messages['speaker']) == 1:
		messages['speaker'] = messages['speaker'][0].strip()
	else:
		messages['speaker'] = ''

	# abstract
	abstract_pattern = re.compile(u"讲座简介[ ]{0,}[：:.]([\s\S]*)", re.S)
	messages['abstract'] = re.findall(abstract_pattern, text)
	if len(messages['abstract']) == 1:
		messages['abstract'] = sub_linefeed(messages['abstract'][0].strip())
	else:
		messages['abstract'] = ''
	if re.search(u"讲师简介[ ]{0,}[：:.]|除[0-9]*级全体本科生|欢迎参加", messages['abstract']) is not None:
		messages['abstract'] = re.sub(u"(讲师简介[ ]{0,}[：:.]|除[0-9]*级全体本科生|欢迎参加)([\s\S]*)", '', messages['abstract'])


	# biography
	biography_pattern = re.compile(u"讲师简介[ ]{0,}[：:.]([\s\S]*)", re.S)
	messages['biography'] = re.findall(biography_pattern, text)
	if len(messages['biography']) == 1:
		messages['biography'] = sub_linefeed(messages['biography'][0].strip())
	else:
		messages['biography'] = ''
	if re.search(u"讲座简介[ ]{0,}[：:.]|除[0-9]*级全体本科生|欢迎参加", messages['biography']) is not None:
		messages['biography'] = re.sub(u"(讲座简介[ ]{0,}[：:.]|除[0-9]*级全体本科生|欢迎参加)([\s\S]*)", '', messages['biography'])

	return messages
