import sys
import json
import requests
import configparser

'''
注册企业微信号后，可以通过API接口推送消息至关注本企业应用的微信成员
具体接口可参考：https://work.weixin.qq.com/api/doc#10167 
"""
touser  否   成员ID列表（消息接收者，多个接收者用‘|’分隔，最多支持1000个）。特殊情况：指定为@all，则向关注该企业应用的全部成员发送
toparty 否   部门ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为@all时忽略本参数
totag   否   标签ID列表，多个接收者用‘|’分隔。当touser为@all时忽略本参数
msgtype 是   消息类型，此时固定为：text
agentid 是   企业应用的id，整型。需要先创建应用，然后在应用的设置页面查看
content 是   消息内容
safe    否   表示是否是保密消息，0表示否，1表示是，默认0
"""
'''
class wechat_sender(object):
	def __init__(self, config, msg_content):
		self.msg_content = msg_content
		self.config = config

	# 获取微信企业应用的access_token
	def get_access_token(self):
		re = requests.get("%sgettoken?corpid=%s&corpsecret=%s" 
							%( self.config["wechat_config"]["base_url"], 
								self.config["wechat_config"]["corpid"],
								self.config['wechat_config']['secret'] ))
		return re.json()["access_token"]

	# 向关注微信企业应用的微信成员发送信息
	def send_msg(self, access_token):
		headers = {'content-type': 'application/json'}
		payload = {
		   "toparty" : "2",
		   "msgtype" : "text",
		   "agentid" : self.config['wechat_config']['agent_id'],
		   "text" : {
		       "content" : self.msg_content
		   },
		   "safe":0
		}

		print ("%smessage/send?access_token=%s" %(self.config["wechat_config"]["base_url"], access_token ))
		print(payload)
		re = requests.post("%smessage/send?access_token=%s" %(self.config["wechat_config"]["base_url"], access_token ), 
							data=json.dumps(payload))
		return re.status_code