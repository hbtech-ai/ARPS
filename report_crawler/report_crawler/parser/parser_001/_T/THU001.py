# -*- coding:utf-8 -*-
import re


def Parser(text, sub_linefeed):
	text = text.decode('utf-8')
	messages = {}

	# title
	title_pattern = re.compile(u"(?:(?:Title)|(?:Topic))[：:.](.*?)(?:(?:Speaker(?:s){0,1})|(?:Time)|(?:Venue)|(?:Meeting Room)|(?:Location)|(?:Place))[：:.]", re.S)
	messages['title'] = re.findall(title_pattern, text)
	if len(messages['title']) == 1:
		messages['title'] = messages['title'][0].strip()
	else:
		messages['title'] = ''

	# time
	time_pattern = re.compile(u"Time[：:.](.*?)(?:(?:Venue)|(?:Meeting Room)|(?:Location)|(?:Place)|(?:Speaker(?:s){0,1})|(?:Abstract))[：:.]", re.S)
	messages['time'] = re.findall(time_pattern, text)
	if len(messages['time']) == 1:
		messages['time'] = messages['time'][0].strip()
	else:
		messages['time'] = ''

	# address
	address_pattern = re.compile(u"(?:(?:Venue)|(?:Meeting Room)|(?:Location)|(?:Place))[：:.](.*?)(?:(?:Speaker(?:s){0,1})|(?:Time)|(?:Abstract))[：:.]", re.S)
	messages['address'] = re.findall(address_pattern, text)
	if len(messages['address']) == 1:
		messages['address'] = messages['address'][0].strip()
	else:
		messages['address'] = ''

	# speaker
	speaker_pattern = re.compile(u"Speaker(?:s){0,1}[：:.](.*?)(?:(?:Time)|(?:Venue)|(?:Meeting Room)|(?:Location)|(?:Place)|(?:Abstract))[：:.]", re.S)
	messages['speaker'] = re.findall(speaker_pattern, text)
	if len(messages['speaker']) == 1:
		messages['speaker'] = messages['speaker'][0].strip()
	else:
		messages['speaker'] = ''

	# abstract
	abstract_pattern = re.compile(u"Abstract[：:.](.*?)(?:(?:Bio[：:.])|(?:Biography[：:.])|(?:Short-Biography[：:.]{0,1})|(?:Short bio[：:.]{0,1}))", re.S)
	messages['abstract'] = re.findall(abstract_pattern, text)
	if len(messages['abstract']) == 1:
		messages['abstract'] = sub_linefeed(messages['abstract'][0].strip())
	elif len(messages['abstract']) == 0:
		abstract_pattern = re.compile(u"Abstract[：:.]([\s\S]*)", re.S)
		messages['abstract'] = re.findall(abstract_pattern, text)
		if len(messages['abstract']) == 1:
			messages['abstract'] = sub_linefeed(messages['abstract'][0].strip())
		else:
			messages['abstract'] = ''
	else:
		messages['abstract'] = ''

	# biography
	biography_pattern = re.compile(u"(?:(?:Bio[：:.])|(?:Biography[：:.])|(?:Short-Biography[：:.]{0,1})|(?:Short bio[：:.]{0,1}))([\s\S]*)", re.S)
	messages['biography'] = re.findall(biography_pattern, text)
	if len(messages['biography']) == 1:
		messages['biography'] = sub_linefeed(messages['biography'][0].strip())
	else:
		messages['biography'] = ''

	return messages
