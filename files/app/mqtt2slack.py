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

slack_token = os.getenv('slack_token', '')
slack_channel = config.get('slack', 'slack_channel')
slack_icon_emoji = config.get('slack', 'slack_icon_emoji')
slack_user_name = config.get('slack', 'slack_user_name')

if __debug__:
    print("running with debug")
    print(mqttBroker)
    print(mqttPort)
    print(mqttKeepAlive)
    print(do_raw_log)
    print(slack_token)
    print(slack_channel)
    print(slack_user_name)
    sys.stdout.flush()

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

def on_message(mqtt_client, userdata, msg):
    global slack_token 
    global slack_channel 
    global slack_icon_emoji
    global slack_user_name
    
    today = datetime.datetime.now()
    print(msg.topic.lower())
    print(msg.payload.decode("utf-8"))


    
    rc = requests.post('https://slack.com/api/users.conversations', {
        'token': slack_token,
        'channel': slack_channel,
        'text': msg.payload.decode("utf-8"),
        'icon_emoji': slack_icon_emoji,
        'username': slack_user_name
    }).json()	
    print(rc)


    rc = requests.post('https://slack.com/api/chat.postMessage', {
        'token': slack_token,
        'channel': slack_channel,
        'text': msg.payload.decode("utf-8"),
        'icon_emoji': slack_icon_emoji,
        'username': slack_user_name
    }).json()	
    print(rc)
    sys.stdout.flush()

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
    mqtt_client = mqtt.Client("reader")

    mqtt_client.connect(mqttBroker, mqttPort, mqttKeepAlive)

    mqtt_client.loop_start()

    while True:
        mqtt_client.subscribe("slack/#")
        mqtt_client.on_message = on_message
        mqtt_client.on_publish = on_publish

        time.sleep(10)
        today = datetime.datetime.now()
        mqtt_client.publish("slack/msg", today.strftime("%d/%m/%Y %H:%M:%S"))

    mqtt_client.loop_stop()

getData(mqttBroker, mqttPort, mqttKeepAlive)
