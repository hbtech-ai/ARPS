# -*- coding:utf-8 -*-
import re


def connect_messages(messages, mode):
	text = ''
	if mode == 'start':
		for message in messages[1:]:
			text += message.strip()
	else:
		for message in messages[:-1]:
			text += message.strip()
	return text


def Parser(text, sub_linefeed):
	text = text.decode('utf-8')
	messages = {}

	# title
	title_pattern = re.compile(u"目[：:.](.*?)\n")
	messages['title'] = re.findall(title_pattern, text)
	if len(messages['title']) == 1:
		messages['title'] = messages['title'][0].strip()
	else:
		messages['title'] = None

	# time
	time_pattern = re.compile(u"间[：:.](.*?)\n")
	messages['time'] = re.search(time_pattern, text)
	if messages['time'] is not None:
		messages['time'] = messages['time'].group().strip()[2:].strip()

	# address
	address_pattern = re.compile(u"点[：:.](.*?)\n")
	messages['address'] = re.search(address_pattern, text)
	if messages['address'] is not None:
		messages['address'] = messages['address'].group().strip()[2:].strip()

	# speaker
	speaker_pattern = re.compile(u"讲[：:.](.*?)\n")
	messages['speaker'] = re.search(speaker_pattern, text)
	if messages['speaker'] is not None:
		messages['speaker'] = messages['speaker'].group().strip()[2:].strip()

	# abstract
	abstract_pattern = re.compile(u"(摘要|Abstract)[：:.](.*?)(主讲人|报告人|Bio)", re.S)
	abstract_split_pattern_start = re.compile(u"[摘要|Abstract][：:.]")
	abstract_split_pattern_end = re.compile(u"主讲人|报告人|Bio")
	messages['abstract'] = re.search(abstract_pattern, text)
	if messages['abstract'] is not None:
		messages['abstract'] = sub_linefeed(connect_messages(re.split(abstract_split_pattern_end, connect_messages(re.split(abstract_split_pattern_start, messages['abstract'].group()), mode='start')), mode='end').strip())
	else:
		abstract_pattern = re.compile(u"(摘要|Abstract)[：:.]([\s\S]*)", re.S)
		messages['abstract'] = re.search(abstract_pattern, text)
		if messages['abstract'] is not None:
			messages['abstract'] = sub_linefeed(connect_messages(re.split(abstract_split_pattern_start, messages['abstract'].group()), mode='start'))

	# biography
	biography_pattern = re.compile(u"(简介|Bio)[：:.]([\s\S]*)", re.S)
	biography_split_pattern_start = re.compile(u"[简介|Bio][：:.]")
	messages['biography'] = re.search(biography_pattern, text)
	if messages['biography'] is not None:
		messages['biography'] = sub_linefeed(connect_messages(re.split(biography_split_pattern_start, messages['biography'].group()), mode='start'))

	return messages
