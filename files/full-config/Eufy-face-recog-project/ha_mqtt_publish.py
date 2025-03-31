import paho.mqtt.client as mqttClient
import time
import json
import requests
# import random
import urllib.request

def on_connect(client, userdata, flags, rc):
    # print("here...")
    if rc == 0:
        print("Connected...")
    else:
        print("Connection failed")

def on_disconnect(client, userdata, rc):
   print("client disconnected ok")
          
def on_publish(client, userdata, mid):
    print(f"Publishing {mqtt_msg} to topic {mqtt_sensor+mqtt_topic}")

def publish(sensor,topic,config_payload,msg):

    global mqtt_sensor
    global mqtt_topic
    global mqtt_msg
    global mqtt_config_payload

    mqtt_sensor = sensor
    mqtt_topic = topic
    mqtt_msg = msg
    mqtt_config_payload = config_payload

    broker_address= "192.168.1.1"          
    port = 1883

    client = mqttClient.Client()                
    client.username_pw_set("user", "pass")
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish    

    client.connect(broker_address, port=port)
        
    client.publish( topic="face-recog/available", payload="online" , qos=0, retain=True)
    client.publish(topic = mqtt_sensor + "/config", payload=json.dumps(mqtt_config_payload), qos=0, retain=True)

    result = client.publish(topic=mqtt_sensor + mqtt_topic, payload=json.dumps(mqtt_msg), qos=0, retain=False)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{mqtt_msg}` to topic `{mqtt_sensor + mqtt_topic}`")
    else:
        print(f"Failed to send message to topic {mqtt_sensor + mqtt_topic}")

    client.disconnect()