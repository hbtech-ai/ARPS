# -*- coding:utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))


def get_localtime(times):
	year, month, day = times.split('-')
	time_number = int(year) * 10000 + int(month) * 100 + int(day)
	return time_number
