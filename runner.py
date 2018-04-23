import time
from config_setting import config
from es import elasticsearch_engine
from wechat import wechat_sender

'''
极光、狸猫nginx日志监控接口，需要传入以下参数
"""
index_name: elastic search 中index名称
threhold_num: 微信报警的阈值，当错误数量大于等于此设置的阈值的时候，会触发相关企业微信报警
secret: 企业微信应用的secret，可在登陆管理后台-> 企业应用 -> Secret中找到
agent_id: 企业应用的id, 可在登陆管理后台-> 企业应用 -> AgentId中找到
"""
'''
def run(index_name, threhold_num, secret, agent_id):
	error_499_counter = 0
	error_50x_counter = 0
	timer = ""
	while True:
		print("start...")
		elastic_search = elasticsearch_engine(index_name)
		_timer = elastic_search.cur_time()

		if timer != _timer:
			if error_499_counter >= threhold_num:
				print(error_499_counter)
				sender = wechat_sender(secret, agent_id,
									   "报警触发UTC时间:%s 请求超时的数量一分钟内>=%s次，当前次数为%s"
				                       %(timer,threhold_num, error_499_counter))
				sender.send_msg(sender.get_access_token())
			if error_50x_counter >= threhold_num:
				print(error_50x_counter)
				sender = wechat_sender(secret, agent_id,
									   "报警触发UTC时间:%s 50X错误请求的数量一分钟内>=%s次，当前次数为%s"
				                       %(timer, threhold_num, error_50x_counter))
				sender.send_msg(sender.get_access_token())
			error_499_counter = 0
			error_50x_counter = 0
		error_499_counter = elastic_search.query_timeout()
		error_50x_counter = elastic_search.query_server_error()

		timer = _timer
		time.sleep(config['monitor_config']['check_frequency'])