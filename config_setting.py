
config = {
	"monitor_config": {
		"jg_threhold_num": 5, # 极光每分钟允许的错误请求数量

	},
	"status_code":{
		"status_code_499": "499",
		"status_code_500": "500"
	},
	"es_setting": {
		"host": "",
		"port" :"9200" ,# es端口
		"user" :"elastic", # es用户名
		"pwd":"changeme" ,# es密码

	},
	"wechat_config":{
		"base_url" :"https://qyapi.weixin.qq.com/cgi-bin/",
		"corpid": "", #微信企业号corpid

	}
}