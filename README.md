# wechat_alert

将Nginx日志通过Logstash接入到Elastic Search中，然后对ES中的日志进行筛选过滤错误请求，当每分钟的错误请求数量大于定义的
阈值时触发微信报警。

1. 运行前请先安装相应的模块
 - pip3 install -r requirements
2. 运行程序
 - python3 runner.py
