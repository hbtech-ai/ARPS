# -*- coding: utf-8 -*-
from parser_001._B import BNU001, BUAA001
from parser_001._C import CSU001
from parser_001._E import ECNU001
from parser_001._N import NWPU001, NWSUAF001
from parser_001._P import PKU001
from parser_001._S import SCU001, SDU001, SYSU001
from parser_001._T import THU001
from parser_001._U import UESTC001
from parser_001._W import WHU001


def get_information(text, faculty):
	messages = {}

	if faculty[-3:] == '001':
		messages = _001(text, faculty[:-3])

	return messages


def _001(text, school_name):
	messages = {}

	if school_name == 'BNU':
		messages = BNU001.Parser(text, sub_linefeed)
	elif school_name == 'BUAA':
		messages = BUAA001.Parser(text, sub_linefeed)
	elif school_name == 'CSU':
		messages = CSU001.Parser(text, sub_linefeed)
	elif school_name == 'ECNU':
		messages = ECNU001.Parser(text, sub_linefeed)
	elif school_name == 'NWPU':
		messages = NWPU001.Parser(text, sub_linefeed)
	elif school_name == 'NWSUAF':
		messages = NWSUAF001.Parser(text, sub_linefeed)
	elif school_name == 'PKU':
		messages = PKU001.Parser(text, sub_linefeed)
	elif school_name == 'SCU':
		messages = SCU001.Parser(text, sub_linefeed)
	elif school_name == 'SDU':
		messages = SDU001.Parser(text, sub_linefeed)
	elif school_name == 'SYSU':
		messages = SYSU001.Parser(text, sub_linefeed)
	elif school_name == 'THU':
		messages = THU001.Parser(text, sub_linefeed)
	elif school_name == 'UESTC':
		messages = UESTC001.Parser(text, sub_linefeed)
	elif school_name == 'WHU':
		messages = WHU001.Parser(text, sub_linefeed)

	return messages


def sub_linefeed(text):
	sub_text = ''
	for line in text.splitlines():
		line = line.rstrip()
		if line != '':
			line += '\n'
		sub_text += line
	return sub_text
