
import os
import json
import logging
import requests
import time
import hmac
import hashlib
import base64
import urllib.parse
from urllib.parse import urlparse

from flask import Flask
from flask import request

app = Flask(__name__)

url = 'https://oapi.dingtalk.com/robot/send?access_token=c1248ea4211978447f55ce69ca861913dff58f6e001ca801dab7d59bfd11a8b9'

@app.route('/', methods=['POST', 'GET'])
def send():
    if request.method == 'POST':
        post_data = request.get_data()
        app.logger.debug(post_data)
        send_alert(json.loads(post_data))
        return 'success'
    else:
        return 'weclome to use prometheus alertmanager dingtalk webhook server!'

def send_alert(data):
    print('------------------------data--------------')
    print(data)
    print('-------------------------------------')
    timestamp = int(round(time.time() * 1000))
    alerts = data['alerts']
    print(alerts)
    alert_name = alerts[0]['labels']['alertname']
    print(alert_name)
    alert_status = alerts[0]['status']
    print(alert_status)
    def _mark_item(alert):
        labels = alert['labels']
        annotations = " "
        #for k, v in alert['annotations'].items():
        for k, v in alert['annotations'].items():
            #annotations += "{0}: {1}\n".format(k, v)
            annotations += "{0}\n".format(v)
            #annotations += "\n"+v+"\n"
        #mark_item =  '\n\n' + annotations 
        mark_item = "\n IP : " + labels['addr'] + '\n\n'+  "\n 环境 : " + labels['env'] + '\n\n'+ annotations  
        return mark_item

    def _mark_item_all(alerts):
        mark_str=""
        for alert in alerts:
            mark_str = mark_str+_mark_item(alert)
        return mark_str

    if alert_status == 'resolved':
        title = "告警恢复:%s" % (alert_name)
    else:
        title = "触发告警:%s ___ 实例数量: %d" % (alert_name, len(alerts))

    external_url = alerts[0]['generatorURL']
    prometheus_url = os.getenv('PROME_URL')
    if prometheus_url:
        res = urlparse(external_url)
        external_url = external_url.replace(res.netloc, prometheus_url)

    send_data = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            #"text": title + "\n"  + _mark_item(alerts[0]) 
            "text": title + "\n" +  _mark_item_all(alerts) +  '\n\n'+  " 时间 : " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n"
        }
    }

    print('-----------------------------------')
    print(send_data)
    req = requests.post(url, json=send_data)
    result = req.json()
    if result['errcode'] != 0:
        app.logger.error('notify dingtalk error: %s' % result['errcode'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

