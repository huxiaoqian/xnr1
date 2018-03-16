#!/usr/bin/env python
#encoding: utf-8

import json
import elasticsearch
from elasticsearch import Elasticsearch

class Es_fb():
	def __init__(self):
		self.es = Elasticsearch('219.224.134.213:9205',timeout=600)

	def executeES(indexName,typeName,data_list):
		self.es.index(indexName,typeName,data_list)