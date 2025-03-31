from PIL import Image
import os, json
import datetime
import requests
from pathlib import Path

from ha_sensors import mqtt_sensors
import ha_mqtt_publish as mqtt_pub
import ha_mqtt_subscribe as mqtt_sub


directory = "Images/Doorbell"
filename = "capture.jpg"
image_file = os.path.join(directory, filename)
# img_files = []

def init():
    mqtt_sub.subscribe()

    #check for changes in file
    get_time = lambda f: os.stat(f).st_ctime
    prev_time = datetime.datetime.now() #get_time(image_file)

    try:
        while True:
            if Path(image_file).exists():
                t = get_time(image_file)
                if t != prev_time:
                    prev_time = t
                    recognize_faces()

    except KeyboardInterrupt:
        print("Exiting..")

        # for filename in os.listdir(directory):
        #     if filename.endswith(".png") or filename.endswith(".jpg"): 
        #         # print(os.path.join(directory, filename))
        #         image_path = os.path.join(directory, filename)
                
        #         img_files.append(image_path)
        #     else:
        #         continue


def recognize_faces():
    count=0
    matched=0
    names=[]
    # for image_file in img_files:

    # url = "http://localhost:8000/api/v1/recognition/recognize? \
    #        limit=<limit>&prediction_count=<prediction_count> \
    #         &det_prob_threshold=<det_prob_threshold> \
    #         &face_plugins=<face_plugins>&status=<status> \
    #         &detect_faces=<detect_faces>"

    url = "http://192.168.1.2:8000/api/v1/recognition/recognize"

    headers = {"x-api-key": "your-compreface-api-key"}

    # files = { "file": open(image_file , 'rb') }

    print(f"uploading file {image_file}")

    file_basename = os.path.basename(image_file)
    with open(image_file, 'rb') as f:
        files = {'file': (str(file_basename),f.read())}

    response = requests.post(url, headers=headers, files=files)
    print(response.text)

    if response.status_code == 200:
        data = response.json()

        for result in data['result']:
            x_max = result['box']['x_max']
            y_max = result['box']['y_max']
            x_min = result['box']['x_min']
            y_min = result['box']['y_min']

            # print(f"{result['subjects'][0]['subject']}")
            subject = result['subjects'][0]['subject']
            confidence = result['subjects'][0]['similarity']

            count+=1

            if confidence >= 0.75:
                name = subject
                names.append(subject)
                matched+=1
            else:
                name = "Unknown"
                names.append(name)
                
            
    print(f"Found {matched} match(es) out of {count}")
    # print(f"{names}")

    print("publishing to mqtt..")
    faces = { "count": count, "match": matched, "last_triggered": str(datetime.datetime.now())}

    mqtt_pub.publish(mqtt_sensors.FACES_SENSOR,mqtt_sensors.FACES_TOPIC, mqtt_sensors.FACES_PAYLOAD, faces)

    matches = { "names": names, "image": image_file, "last_triggered": str(datetime.datetime.now()) }

    # print(f"{matches}")

    mqtt_pub.publish(mqtt_sensors.MATCHES_SENSOR, mqtt_sensors.MATCHES_TOPIC, mqtt_sensors.MATCHES_PAYLOAD, matches)

if __name__ == '__main__':
    init()