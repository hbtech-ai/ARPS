# -*- coding:utf-8 -*-
import re


def Filter(text, ab_sign=0):
	# title
	if re.search(u"(((报[ ]*告|讲[ ]*座)*(主[ ]*题|题[ ]*目))([ (（](Title|Topic))*|Title|Topic)[）) ]*[：:.]+", text) is not None:
		text = re.sub(u"(((报[ ]*告|讲[ ]*座)*(主[ ]*题|题[ ]*目))([ (（](Title|Topic))*|Title|Topic)[）) ]*[：:.]+[\s\S]*", '', text)

	# time
	if re.search(u"(((报[ ]*告|讲[ ]*座)*(日期及)*(时[ ]*间|日[ ]*期))([ (（]Time)*|Time)[）) ]*[：:.]+", text) is not None:
		text = re.sub(u"(((报[ ]*告|讲[ ]*座)*(日期及)*(时[ ]*间|日[ ]*期))([ (（]Time)*|Time)[）) ]*[：:.]+[\s\S]*", '', text)

	# address
	if re.search(u"(((报[ ]*告|讲[ ]*座){0,1}地[ ]*点)([ (（](Address|Venue|Location|Meeting Room|Place))*|Address|Venue|Location|Meeting Room|Place)[）) ]*[：:.]+", text) is not None:
		text = re.sub(u"(((报[ ]*告|讲[ ]*座){0,1}地[ ]*点)([ (（](Address|Venue|Location|Meeting Room|Place))*|Address|Venue|Location|Meeting Room|Place)[）) ]*[：:.]+[\s\S]*", '', text)

	# speaker
	if re.search(u"(((讲[ ]*授|演[ ]*讲|报[ ]*告|主[ ]*讲)[ ]*(人|专[ ]*家|嘉[ ]*宾)|讲[ ]*(师|者)|主[ ]*讲)([ (（]Speaker)*|Speaker)[）) ]*[：:.]+", text) is not None:
		text = re.sub(u"(((讲[ ]*授|演[ ]*讲|报[ ]*告|主[ ]*讲)[ ]*(人|专[ ]*家|嘉[ ]*宾)|讲[ ]*(师|者)|主[ ]*讲)([ (（]Speaker)*|Speaker)[）) ]*[：:.]+[\s\S]*", '', text)

	# abstract
	if re.search(u"((((报告|讲座|内容)*(摘要|内容|提要))|(报告|讲座|内容)简介)([ (（]Abstract)*|Abstract)[）) ]*[：:.]+", text) is not None:
		text = re.sub(u"((((报告|讲座|内容)*(摘要|内容|提要))|(报告|讲座|内容)简介)([ (（]Abstract)*|Abstract)[）) ]*[：:.]+[\s\S]*", '', text)

	# biography
	if re.search(u"(((讲座|主讲|报告|演讲|讲)(者|人|师|专家|嘉宾)|个人)(及其)*(简介|介绍|简历)([ (（](Biography|Bio|Short-Biography|Short bio))*|Biography|Bio|Short-Biography|Short bio)[）) ]*[：:.]+", text) is not None:
		text = re.sub(u"(((讲座|主讲|报告|演讲|讲)(者|人|师|专家|嘉宾)|个人)(及其)*(简介|介绍|简历)([ (（](Biography|Bio|Short-Biography|Short bio))*|Biography|Bio|Short-Biography|Short bio)[）) ]*[：:.]+[\s\S]*", '', text)

	# chairman
	if re.search(u"主[ ]*持[ ]*(人)*([ (（]Chair)*[）) ]*[：:.]+", text) is not None:
		text = re.sub(u"主[ ]*持[ ]*(人)*([ (（]Chair)*[）) ]*[：:.]+[\s\S]*", '', text)

	# invitee
	if re.search(u"邀[ ]*请[ ]*人([ (（]Invitee)*[）) ]*[：:.]+", text) is not None:
		text = re.sub(u"邀[ ]*请[ ]*人([ (（]Invitee)*[）) ]*[：:.]+[\s\S]*", '', text)

	# others
	if re.search(u"欢迎(各位|广大)", text) is not None:
		text = re.sub(u"欢迎(各位|广大)[\s\S]*", '', text)
	if re.search(u"报[ ]*告[ ]*([一二三四五]|[\d])[ ]*[：:.]*", text) is not None:
		text = re.sub(u"报[ ]*告[ ]*([一二三四五]|[\d])[ ]*[：:.]*[\s\S]*", '', text)
	if re.search(u"查看次数[：:.]", text) is not None:
		text = re.sub(u"查看次数[：:.][\s\S]*", '', text)
	if re.search(u"附件下载[：:.]", text) is not None:
		text = re.sub(u"附件下载[：:.][\s\S]*", '', text)
	if re.search(u"(主办|讲座|报告|演讲)(人)*(单位|企业)[：:.]", text) is not None:
		text = re.sub(u"(主办|讲座|报告|演讲)(人)*(单位|企业)[：:.][\s\S]*", '', text)
	if re.search(u"[一二三四五六七八九][、.]", text) != None:
		text = re.sub(u"[一二三四五六七八九][、.][\s\S]*", '', text)

	return text


def Parser(text, sub_linefeed):
	text = text.decode('utf-8')
	messages = {}

	# title
	title_pattern = re.compile(u"(?:(?:(?:报[ ]*告|讲[ ]*座)*(?:主[ ]*题|题[ ]*目))|Title|Topic)[）) ]*[：:.]+([\s\S]*)", re.S)
	messages['title'] = re.findall(title_pattern, text)
	if len(messages['title']) == 1:
		messages['title'] = messages['title'][0].strip()
	else:
		messages['title'] = ''
	messages['title'] = Filter(messages['title'], 0)

	# time
	time_pattern = re.compile(u"(?:(?:(?:报[ ]*告|讲[ ]*座)*(?:时[ ]*间|日[ ]*期))|Time)[）) ]*[：:.]+([\s\S]*)", re.S)
	messages['time'] = re.findall(time_pattern, text)
	if len(messages['time']) == 1:
		messages['time'] = messages['time'][0].strip()
	else:
		messages['time'] = ''
	messages['time'] = Filter(messages['time'], 0)

	# address
	address_pattern = re.compile(u"(?:(?:(?:报[ ]*告|讲[ ]*座){0,1}地[ ]*点)|Address|Venue|Location|Meeting Room|Place)[）) ]*[：:.]+([\s\S]*)", re.S)
	messages['address'] = re.findall(address_pattern, text)
	if len(messages['address']) == 1:
		messages['address'] = messages['address'][0].strip()
	else:
		messages['address'] = ''
	messages['address'] = Filter(messages['address'], 0)

	# speaker
	speaker_pattern = re.compile(u"(?:(?:讲[ ]*授|演[ ]*讲|报[ ]*告|主[ ]*讲)[ ]*(?:人|专[ ]*家|嘉[ ]*宾)|讲[ ]*(?:师|者)|主[ ]*讲|Speaker)[）) ]*[：:.]+([\s\S]*)", re.S)
	messages['speaker'] = re.findall(speaker_pattern, text)
	if len(messages['speaker']) == 1:
		messages['speaker'] = messages['speaker'][0].strip()
	else:
		messages['speaker'] = ''
	messages['speaker'] = Filter(messages['speaker'], 0)

	# abstract
	abstract_pattern = re.compile(u"(?:(?:(?:报告|讲座|内容)*(?:摘要|内容|提要))|(?:报告|讲座|内容)简介|Abstract)[）) ]*[：:.]+([\s\S]*)", re.S)
	messages['abstract'] = re.findall(abstract_pattern, text)
	if len(messages['abstract']) == 1:
		messages['abstract'] = sub_linefeed(messages['abstract'][0].strip())
	else:
		messages['abstract'] = ''
	messages['abstract'] = Filter(messages['abstract'], 1)

	# biography
	biography_pattern = re.compile(u"(?:(?:(?:讲座|主讲|报告|演讲|讲)(?:者|人|师|专家|嘉宾)|个人)(?:及其)*(?:简介|介绍|简历)|Biography|Bio|Short-Biography|Short bio)[）) ]*[：:.]+([\s\S]*)", re.S)
	messages['biography'] = re.findall(biography_pattern, text)
	if len(messages['biography']) == 1:
		messages['biography'] = sub_linefeed(messages['biography'][0].strip())
	else:
		messages['biography'] = ''
	messages['biography'] = Filter(messages['biography'], 1)

	# If speaker is not exist, we could get it from the biography.
	if messages['speaker'] == '':
		speakerFromBioChina = re.match(u"(.*?)(教授|副教授|博士|讲师)", messages['biography'])
		messages['speaker'] = '' if speakerFromBioChina is None else speakerFromBioChina.group()
	if messages['speaker'] == '':
		speakerFromBioEng = re.match(u"([A-Z][a-zA-Z]*[ .]*)+", messages['biography'])
		messages['speaker'] = '' if speakerFromBioEng is None else speakerFromBioEng.group()

	return messages
