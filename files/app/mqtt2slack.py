import paho.mqtt.client as mqtt
import time
import configparser
import sys
import json
import datetime
import os

config = configparser.RawConfigParser(allow_no_value=True)
config.read("config.ini")

log_path = config.get('Logging', 'log_path', fallback='/var/log/mqtt2slack/')
do_raw_log = config.getboolean('Logging', 'do_raw_log')

mqttBroker = config.get('mqtt2slack', 'mqttBroker')
mqttPort = int(config.get('mqtt2slack', 'mqttPort'))
mqttKeepAlive = int(config.get('mqtt2slack', 'mqttKeepAlive'))

slack_token = os.getenv('slack_token', '')
slack_channel = int(config.get('slack', 'slack_channel'))
slack_icon_emoji = config.get('slack', 'slack_icon_emoji')
slack_user_name = config.get('slack', 'slack_user_name')

values = dict()

previous_value = 0

def on_message(mqtt_client, userdata, msg):
    global values
    global previous_value

    today = datetime.datetime.now()
    print(msg.topic.lower())
#    if msg.topic.lower() == "mqtt2slack/reading/current_value" :        
#        if previous_value > 0:
#            values['current_value'] = int(str(msg.payload.decode("utf-8")))
#            values['usages'] = int(str(msg.payload.decode("utf-8"))) - previous_value            
#        else:
#            values['current_value'] = int(str(msg.payload.decode("utf-8")))
#            values['usages'] = 0
#        previous_value = int(str(msg.payload.decode("utf-8")))
#        values['datetime'] = today.strftime("%d/%m/%Y %H:%M:%S")    

#    if msg.topic.lower() == "mqtt2slack/reading/pulse_count" :
#        values['pulse_count'] = int(str(msg.payload.decode("utf-8")))
#        values['datetime'] = today.strftime("%d/%m/%Y %H:%M:%S")
    
def getData(mqttBroker, mqttPort, mqttKeepAlive):
    global values
    global previous_value
    
    mqtt_client = mqtt.Client("reader")

    mqtt_client.connect(mqttBroker, mqttPort, mqttKeepAlive)

    mqtt_client.loop_start()

    while True:
        mqtt_client.subscribe("#")
        mqtt_client.on_message=on_message
    
    mqtt_client.loop_stop()

getData(mqttBroker, mqttPort, mqttKeepAlive)
