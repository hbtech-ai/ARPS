# -*- coding: utf-8 -*-

import random

class ReportSpiderSpiderMiddleware(object):
	# Randomly choice user agents
	def __init__(self, user_agents):
		self.user_agents = user_agents

	@classmethod
	def from_crawler(cls, crawler):
		return cls(crawler.settings.getlist('USER_AGENTS'))

	def process_request(self, request, spider):
		# print "**************************" + random.choice(self.agents)
		request.headers.setdefault('User-Agent', random.choice(self.user_agents))