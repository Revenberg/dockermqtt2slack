import paho.mqtt.client as mqtt
import time
import configparser
import sys
import json
import datetime
import os
import requests

config = configparser.RawConfigParser(allow_no_value=True)
config.read("config.ini")

log_path = config.get('Logging', 'log_path', fallback='/var/log/mqtt2slack/')
do_raw_log = config.getboolean('Logging', 'do_raw_log')

mqttBroker = config.get('mqtt', 'mqttBroker')
mqttPort = int(config.get('mqtt', 'mqttPort'))
mqttKeepAlive = int(config.get('mqtt', 'mqttKeepAlive'))

slack_webhook = os.getenv('webhook', '')

if __debug__:
    print("running with debug")
    print(mqttBroker)
    print(mqttPort)
    print(mqttKeepAlive)
    print(do_raw_log)
    print(slack_webhook)
    sys.stdout.flush()

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

def send_slack(text):
    global slack_webhook
    
    headers = {'content-type': 'application/json'}
    
    payload = { 
        'text': text  
    }

    rc = requests.post(slack_webhook, 
        data=json.dumps(payload),
        headers=headers
        )

def on_message(mqtt_client, userdata, msg):
    global slack_webhook 
    
    send_slack( msg.payload.decode("utf-8") )
    
def getData(mqttBroker, mqttPort, mqttKeepAlive):   
    mqtt_client = mqtt.Client("reader")
    mqtt_client.connect(mqttBroker, mqttPort, mqttKeepAlive)    
    mqtt_client.loop_start()
    mqtt_client.subscribe("slack/msg")
    
    while True:        
        mqtt_client.on_message = on_message
        mqtt_client.on_publish = on_publish

        today = datetime.datetime.now()
        print(today)
        mqtt_client.publish("slack/msg", today.strftime("%d/%m/%Y %H:%M:%S"))
        sys.stdout.flush()
        time.sleep(300)
    
    mqtt_client.loop_stop()

getData(mqttBroker, mqttPort, mqttKeepAlive)

