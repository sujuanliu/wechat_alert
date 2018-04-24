import datetime
import configparser
from elasticsearch import Elasticsearch

STATUS_CODE_500 = "500"
STATUS_CODE_499 = "499"

class elasticsearch_engine(object):
	def __init__(self, config):
		self.config = config
		self.serverError_filter_json = { 
					"range": {
						 "status": {
							  "gte": STATUS_CODE_500
							  }
					  }}
		self.timeout_filter_json = {
					"term":{
						"status": STATUS_CODE_499
						}
					}

	# 获取当前时间
	def cur_time(self):
		now_time = datetime.datetime.utcnow()
		return now_time.strftime("%Y-%m-%dT%H:%M")

	# 获取当前日期
	def cur_date(self):
		now_date = datetime.datetime.utcnow()
		return now_date.strftime("%Y.%m.%d")

	# 根据@timestamp和status字段过滤搜索ES日志
	def query(self, filter_string):
		es = Elasticsearch([{
			  'host': self.config['es_setting']['host'], 
		      'port': self.config['es_setting']['port'],
		      'http_auth':( self.config['es_setting']['user'], self.config['es_setting']['pwd'])
		    }])
		index_name = ('{0}{1}'.format(self.config['es_setting']['index_name'], self.cur_date() ))
		data = {
				  "query": { 
				    "bool": { 
				      "must": [
				        { "match": { "@timestamp": self.cur_time() }}  
				      ],
				      "filter": [ filter_string ]
				    }
				  }
				}
		print(self.cur_time(), data, index_name)
		search = es.search(index = index_name, body = data)
		return search['hits']['total']
	
	# 在ES中过滤请求返回码等于499，并返回记录总数	
	def query_timeout(self):
	 	return self.query(self.timeout_filter_json)

	# 在ES中过滤请求返回码大于等于500，并返回记录总数
	def query_server_error(self):
	 	return self.query(self.serverError_filter_json)