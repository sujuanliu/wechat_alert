import time
import configparser
from runner import *
from es import elasticsearch_engine
from wechat import wechat_sender

'''
需要传入以下参数
"""
config: 传入configparser类型的参数，配置文件模板请参考config_setting.cfg
"""
'''
def run(config):
	error_499_counter = 0
	error_50x_counter = 0
	timer = ""
	while True:
		print("start...")
		elastic_search = elasticsearch_engine(config)
		_timer = elastic_search.cur_time()
		print(config.getint('monitor_config','threhold_num'))

		if timer != _timer:
			if error_499_counter >= config.getint('monitor_config','threhold_num'):
				print(error_499_counter)
				sender = wechat_sender(config,
									   "报警触发UTC时间:%s 请求超时的数量一分钟内>=%s次，当前次数为%s"
				                       %(timer,config['monitor_config']['threhold_num'], error_499_counter))
				sender.send_msg(sender.get_access_token())
			if error_50x_counter >= config.getint('monitor_config','threhold_num'):
				print(error_50x_counter)
				sender = wechat_sender(config,
									   "报警触发UTC时间:%s 50X错误请求的数量一分钟内>=%s次，当前次数为%s"
				                       %(timer, config['monitor_config']['threhold_num'], error_50x_counter))
				sender.send_msg(sender.get_access_token())
			error_499_counter = 0
			error_50x_counter = 0
		error_499_counter = elastic_search.query_timeout()
		error_50x_counter = elastic_search.query_server_error()

		timer = _timer
		time.sleep(config.getint('monitor_config','check_frequency'))


if __name__ == "__main__":
	parser = configparser.ConfigParser()
	parser.read_file(open('config_setting.cfg'))
	run(parser)