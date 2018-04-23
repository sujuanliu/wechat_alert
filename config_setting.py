config = {
	"monitor_config": {
		"jg_threhold_num": 5, # 每分钟允许的错误请求数量
		"limao_threhold_num": 5, # 每分钟允许的错误请求数量
		"check_frequency": 10, # 程序每分钟检测的频率，e.g. 10s
	},
	"status_code":{
		"status_code_499": "499",
		"status_code_500": "500"
	},
	"es_setting": {
		"host": "",
		"port" :"9200" ,# es端口
		"user" :"", # es用户名
		"pwd":"" ,# es密码
		"jg_index_name":"", # JG ES index名称前缀
		"limao_index_name" :  # limao ES index名称前缀
	},
	"wechat_config":{
		"base_url" :"https://qyapi.weixin.qq.com/cgi-bin/",
		"corpid": "", #微信企业号corpid
		"jg_secret":"",  #微信企业应用secret
		"jg_agent_id": "", #极光企业微信应用ID
		"limao_secret":"-" , #微信企业limao应用secret
		"limao_agent_id":"" #limao企业微信应用ID

	}
}