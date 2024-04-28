import os
import sys
import logging
from datetime import datetime
import json
import pytz

from pymongo import MongoClient

import paho.mqtt.client as mqtt

zone_a_visitors = 0

# logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# pymongo configuration
mongo_host = os.getenv('MONGO_HOST', None)
if mongo_host is None:
    logging.error('MONGO_HOST undefined.')
    sys.exit(1)
mongo_port = os.getenv('MONGO_PORT', None)
if mongo_port is None:
    logging.error('MONGO_PORT undefined.')
    sys.exit(1)
mongo_client = MongoClient(mongo_host, int(mongo_port))

# mqtt configuration
mqtt_broker = os.getenv('MQTT_BROKER', None)
if mqtt_broker is None:
    logging.error('MQTT_BROKER undefined.')
    sys.exit(1)
mqtt_port = os.getenv('MQTT_PORT', None)
if mqtt_port is None:
    logging.error('MQTT_PORT undefined.')
    sys.exit(1)

# MQTT data sources
# MQTT_PERSON_TOPIC = os.getenv('MQTT_PERSON_TOPIC', None)
# if MQTT_PERSON_TOPIC is None:
#     logging.error('MQTT_PERSON_TOPIC undefined.')
#     sys.exit(1)
MQTT_CAMERA_TOPIC = os.getenv('MQTT_CAMERA_TOPIC', None)
if MQTT_CAMERA_TOPIC is None:
    logging.error('MQTT_CAMERA_TOPIC undefined.')
    sys.exit(1)
# MQTT_CMD_TOPIC = os.getenv('MQTT_CMD_TOPIC', None)
# if MQTT_CMD_TOPIC is None:
#     logging.error('MQTT_CMD_TOPIC undefined.')
#     sys.exit(1)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    logging.info('Connected to MQTT Broker.')
    client.subscribe(MQTT_CAMERA_TOPIC + '#')
    # client.subscribe(MQTT_CAMERA_TOPIC + '#')
    # client.subscribe(MQTT_HB_TOPIC + '#')

def on_message(client, userdata, msg):
    logging.info('Received message: %s from %s', msg.payload, msg.topic)
    # dev_db = mongo_client.dev_db
    # dev_col = dev_db.devices
    # dev_evts = dev_db.device_events
    # camera_db = mongo_client.camera_db
    # camera_col = camera_db.devices
    # camera_detect_evts = camera_db.detect_evts

    capture_db = mongo_client.capture_db
    capture_status = capture_db.captures
    # capture_detect_evts = capture_db.detect_evts

    # # ----------------Light DB------------------
    # light_db = mongo_client.capture_db
    # light_status = light_db.status
    # light_evts = light_db.light_evts
    #json = {'status':'ON; 'brightness':}
    print("**************Message**************")
    print(msg)
    msg_data = json.loads( msg.payload )
    print()
    print("**************Message Data**************")
    print(msg_data)

    timezone = pytz.timezone('Asia/Bangkok')
    bkk_time = datetime.now(timezone)

    print("*****************Bangkok time*****************")
    print(bkk_time)
    
    c = datetime.now()

    # can we show light status directly from mqtt
    capture_status.insert_one({
        'status': msg_data["status"],
        'location': msg_data["location"],
        'date': bkk_time.strftime("%A %d %B, %Y"),
        'time': bkk_time.strftime("%H:%M")
    })

    # if msg_data["msg_type"] == "entrance":
    #     zone_a_visitors+=1
    # elif msg_data["msg_type"] == "exit":
    #     zone_a_visitors-=1
    dev_id = msg.topic.split('/')[-1]
    evt_type = msg.topic.split('/')[-2]
    # if evt_type == 'sound':
    #     dev_doc = dev_col.find_one({'dev_id': dev_id})
    #     if dev_doc is not None:
    #         msg_data = json.loads( msg.payload )
    #         dev_evts.insert_one({
    #             'dev_id': dev_id,
    #             'type': evt_type,
    #             'timestamp': datetime.now(),
    #             'value': msg_data['status']
    #         })
    # if evt_type == 'person':


# start instance
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.enable_logger()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(mqtt_broker, int(mqtt_port), 60)
mqtt_client.loop_forever()