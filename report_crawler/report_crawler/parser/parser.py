# -*- coding: utf-8 -*-
from THU.THU001_Parser import THU001_Parser
from SYSU.SYSU001_Parser import SYSU001_Parser
from WHU.WHU001_Parser import WHU001_Parser


def get_information(text, faculty):
	messages = {}
	if faculty[:-3] == 'SYSU':
		messages = SYSU(text, faculty[-3:])
	elif faculty[:-3] == 'WHU':
		messages = WHU(text, faculty[-3:])
	elif faculty[:-3] == 'THU':
		messages = THU(text, faculty[-3:])
	return messages


def SYSU(text, faculty_num):
	messages = {}
	if faculty_num == '001':
		messages = SYSU001_Parser(text, sub_linefeed)
	return messages


def THU(text, faculty_num):
	messages = {}
	if faculty_num == '001':
		messages = THU001_Parser(text, sub_linefeed)
	return messages


def WHU(text, faculty_num):
	messages = {}
	if faculty_num == '001':
		messages = WHU001_Parser(text, sub_linefeed)
	return messages


def sub_linefeed(text):
	sub_text = ''
	for line in text.splitlines():
		line = line.rstrip()
		if line != '':
			line += '\n'
		sub_text += line
	return sub_text
