# -*- coding:utf-8 -*-

import re
import os
import sys
import time
import datetime
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))


def get_localtime(times):

	date = times.split('-')
	if len(date) == 3:
		year, month, day = date
		if len(year) != 4:
			year = time.strftime("%Y", time.localtime())[:2] + year
	else:
		month, day = date
		year = time.strftime("%Y", time.localtime())

	time_number = int(year) * 10000 + int(month) * 100 + int(day)
	return time_number


class startTime():
	def __init__(self, time):
		self.now_time = str(time)[0:4] + '-' + str(time)[4:6] + '-' + str(time)[6:8]

		self.month_E2C = {
			'Jan': '1',
			'Feb': '2',
			'Mar': '3',
			'Apr': '4',
			'May': '5',
			'June': '6',
			'July': '7',
			'Aug': '8',
			'Sept': '9',
			'Oct': '10',
			'Nov': '11',
			'Dec': '12'
		}

		self.week2day = {
			u'一': '1',
			u'二': '2',
			u'三': '3',
			u'四': '4',
			u'五': '5',
			u'六': '6',
			u'七': '7',
			u'日': '7',
			u'天': '7',
			u'末': '7'
		}

	# day
	def get_day(self, text):

		day = re.search(u"[0-9]*(?=(日|号))", text)

		if day is not None:
			day = day.group()
		else:
			Eng_day = re.search(u"(?<=(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))[\s\S]*", text)
			day = re.search(u"[0-9]{1,}", Eng_day.group()) if Eng_day is not None else None
			day = day.group() if day is not None else None

		return day

	# month
	def get_month(self, text, day):
		month = re.search(u"[0-9]*(?=月)", text)
		if month is not None:
			month = month.group()
		else:
			now_day = int(self.now_time.split('-')[-1])
			now_month = int(self.now_time.split('-')[-2])
			month = re.search(u"Jan|Feb|Mar|Apr|May|June|July|Aug|Sept|Oct|Nov|Dec", text)
			if month is not None:
				month = self.month_E2C[month.group()]
			elif day is not None:
				month = str(now_month + 1) if int(day) < now_day else str(month)

		return month

	# year
	def get_year(self, text, day, month):
		year = re.search(u"[0-9]*(?=年)", text)
		if year is not None:
			year = "20" + year.group() if len(year.group().strip()) < 4 else year.group()
		elif day is not None and month is not None:
			now_year = int(self.now_time.split('-')[0])
			now_month_day = int(str(get_localtime(self.now_time))[4:])
			report_month_day = int(month) * 100 + int(day)
			year = str(now_year + 1) if report_month_day < now_month_day else str(now_year)

		return year

	def get_time(self, text):
		day = self.get_day(text)
		month = self.get_month(text, day)
		year = self.get_year(text, day, month)
		if day is not None and month is not None and year is not None:
			start_time = year + '-' + month + '-' + day
		else:
			start_time = re.search(u"([\d]*)[-~.,，]*([\d]{1,})[-~.,，]{1,}([\d]{1,})", text)
			if start_time is not None:
				start_time = re.split(u"[-~.,，]*", start_time.group())
				if len(start_time) == 3:
					start_time = start_time[0] + '-' + start_time[1] + '-' + start_time[2]
				elif len(start_time) == 2:
					start_time = self.get_year('', start_time[1], start_time[0]) + '-' + start_time[0] + '-' + start_time[1]
				else:
					start_time = None
			else:
				weekday = re.findall(u"(?:星期|周)(一|二|三|四|五|六|七|日|天|末|[\d])", text)
				if len(weekday) != 0:
					weekday = weekday[0]
					if re.sub(u"\\s+", '', weekday) != '':
						weekday = int(self.week2day[weekday]) if self.week2day.has_key(weekday) else int(weekday)

						now_weekday = datetime.datetime.now().weekday() + 1
						delay_days = weekday + 7 - now_weekday if weekday < now_weekday else weekday - now_weekday
						start_time = str(datetime.datetime.now() + datetime.timedelta(days=delay_days)).split(' ')[0]
				else:
					start_time = None

		if start_time is None or re.sub(u"\\s+", '', start_time) == '':
			return None

		# try return the right time, or return None
		try:
			return get_localtime(start_time)
		except:
			return None
