import datetime
from config_setting import config
from elasticsearch import Elasticsearch

class elasticsearch_engine(object):
	def __init__(self, es_index_name):
		self.es_index_name = es_index_name
		self.serverError_filter_json = { 
					"range": {
						 "status": {
							  "gte": config['status_code']['status_code_500']
							  }
					  }}
		self.timeout_filter_json = {
					"term":{
						"status":config['status_code']['status_code_499']
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
			  'host': config['es_setting']['host'], 
		      'port': config['es_setting']['port'],
		      'http_auth':(config['es_setting']['user'], config['es_setting']['pwd'])
		    }])
		index_name = ('{0}{1}'.format(self.es_index_name, self.cur_date() ))
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
		print(self.cur_time(),data,index_name)
		search = es.search(index=index_name,body=data)
		return search['hits']['total']
	
	# 在ES中过滤请求返回码等于499，并返回记录总数	
	def query_timeout(self):
	 	return self.query(self.timeout_filter_json)

	# 在ES中过滤请求返回码大于等于500，并返回记录总数
	def query_server_error(self):
	 	return self.query(self.serverError_filter_json)
