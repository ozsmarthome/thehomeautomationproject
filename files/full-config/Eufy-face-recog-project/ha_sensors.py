class mqtt_sensors:


    FACES_PAYLOAD = {
            "name": "face_recog_faces",
            "state_topic": "homeassistant/sensor/face-recog/faces/state",
            "json_attributes_topic" : "homeassistant/sensor/face-recog/faces/state",
            "value_template": "{{ value_json.faces }}",
            "unique_id": "face_recog_faces",
            "availability_topic" : "face-recog/available",
            "platform": "mqtt"
        }
    
    FACES_SENSOR = "homeassistant/sensor/face-recog/faces" #/config
    FACES_TOPIC = "/state"

    # face_location = { x_min, y_min, x_mac, y_max }
    # match = { name, confidence, face_location }

    MATCHES_PAYLOAD = {
            "name": "face_recog_matches",
            "state_topic": "homeassistant/sensor/face-recog/matches/state",
            "json_attributes_topic" : "homeassistant/sensor/face-recog/matches/state",
            "value_template": "{{ value_json.matches }}",
            "unique_id": "face_recog_matches",
            "availability_topic" : "face-recog/available",
            "platform": "mqtt"
        }
    
    MATCHES_SENSOR = "homeassistant/sensor/face-recog/matches" #/config
    MATCHES_TOPIC = "/state"