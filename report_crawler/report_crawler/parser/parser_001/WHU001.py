# -*- coding: utf-8 -*-
import re


def Parser(text, sub_linefeed):
    text = text.decode('utf-8')
    messages = {}

    # title
    title_pattern = re.compile(u"题目[：:.](.*?)\n")
    messages['title'] = re.search(title_pattern, text)
    if messages['title'] is not None:
        messages['title'] = messages['title'].group().strip()[3:].strip()

    # time
    time_pattern = re.compile(u"时间[：:.](.*?)\n")
    messages['time'] = re.search(time_pattern, text)
    if messages['time'] is not None:
        messages['time'] = messages['time'].group().strip()[3:].strip()

    # address
    address_pattern = re.compile(u"地点[：:.](.*?)\n")
    messages['address'] = re.search(address_pattern, text)
    if messages['address'] is not None:
        messages['address'] = messages['address'].group().strip()[3:].strip()

    # speaker
    speaker_pattern = re.compile(u"报告人[：:.](.*?)\n")
    messages['speaker'] = re.search(speaker_pattern, text)
    if messages['speaker'] is not None:
        messages['speaker'] = messages['speaker'].group().strip()[4:].strip()

    # biography
    biography_pattern = re.compile(u"报告人简介[：:.](.*?)报告摘要", re.S)
    messages['biography'] = re.search(biography_pattern, text)
    if messages['biography'] is not None:
        messages['biography'] = sub_linefeed(messages['biography'].group().strip()[6:-4].strip())
    else:
        biography_pattern = re.compile(u"报告人简介[：:.](.*?)邀请人", re.S)
        messages['biography'] = re.search(biography_pattern, text)
        if messages['biography'] is not None:
            messages['biography'] = sub_linefeed(messages['biography'].group().strip()[6:-3].strip())

    # abstract
    abstract_pattern = re.compile(u"报告摘要[：:.](.*?)邀请人", re.S)
    messages['abstract'] = re.search(abstract_pattern, text)
    if messages['abstract'] is not None:
        messages['abstract'] = sub_linefeed(messages['abstract'].group().strip()[5:-3].strip())

    return messages
