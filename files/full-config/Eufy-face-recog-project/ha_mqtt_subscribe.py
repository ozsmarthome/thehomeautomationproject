import paho.mqtt.client as mqttClient
import time
import json
import requests
import random
import urllib
import threading

topic_to_subscribe = "doorbell/snapshot"
image_url = ''

def getImageFile():
    return image_file_path

def download_image(url):
    name = "capture" #random.randrange(1,100)
    fullname = 'Images/Doorbell/' + str(name)+".jpg"

    # urllib.request.urlretrieve(url, fullname)
    with open(fullname, 'wb') as handle:
        response = requests.get(url, stream=True)

        if not response.ok:
            print(response)
        else:
            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)

    handle.close()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker for topic " + topic_to_subscribe)
        client.subscribe(topic_to_subscribe)

    else:
        print("Connection failed")

def on_message(client, userdata, message):
    # print("Message received : "  + str(message.payload) + " on " + message.topic)
    data = json.loads(message.payload)
    image_url = data["image"]
    # if not image_url == '':
    download_image(image_url)

def mqtt_subscribe(arg):
       
    broker_address= "192.168.1.1"          
    port = 1883    
    client = mqttClient.Client()

    client.username_pw_set("user", "pass")
    client.on_connect= on_connect    
    client.on_message= on_message 

    client.connect(broker_address, port=port)     
    client.loop_start()


    try:
        while True:
            time.sleep(arg)

    except KeyboardInterrupt:
        print("Exiting subscribe..")
        client.disconnect()
        client.loop_stop()

def subscribe():
    t = threading.Thread(target=mqtt_subscribe, args=(1,))
    t.start()
    # t.join()
    print("Stopping subscribe..")