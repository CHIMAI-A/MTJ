import os
import sys
import logging
from datetime import datetime
import json
import pytz

import pymongo

import paho.mqtt.client as mqtt

mongo_client = pymongo.MongoClient('mongodb://localhost:27017')

# mydb = mongo_client['Park_Camera']

# capture = mydb.capture_evts

# timezone = pytz.timezone('Asia/Bangkok')
# bkk_time = datetime.now(timezone)

# capture.insert_one({
#         'capture': 'detected',
#         'count': 4,
#         'location': 'Zone A',
#         'date': bkk_time.strftime("%A %d %B, %Y"),
#         'time': bkk_time.strftime("%H:%M")
# })

def on_connect(client, userdata, flags, reason_code):
    logging.info('Connected to MQTT Broker.')
    client.subscribe('esp32/park/cam/person/' + '#')

def on_message(client, userdata, msg):
    logging.info('Received message: %s from %s', msg.payload, msg.topic)
    capture_db = mongo_client["Park_Camera"]
    capture_detect_evts = capture_db.capture_evts

    msg_data = json.loads(msg.payload)
    timezone = pytz.timezone('Asia/Bangkok')
    bkk_time = datetime.now(timezone)

    capture_detect_evts.insert_one({
        'capture': msg_data["capture"],
        'count': msg_data["new_capture"],
        'location': msg_data["location"],
        'date': bkk_time.strftime("%A %d %B, %Y"),
        'time': bkk_time.strftime("%H:%M:%S")
    })

# start instance
mqtt_client = mqtt.Client()
# mqtt_client.enable_logger()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect('broker.hivemq.com', 1883, 60)
mqtt_client.loop_forever()