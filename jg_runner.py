from config_setting import config
from runner import *

if __name__ == "__main__":
	run(config['es_setting']['jg_index_name'], 
		config['monitor_config']['jg_threhold_num'],
		config['wechat_config']['jg_secret'],
		config['wechat_config']['jg_agent_id'] )