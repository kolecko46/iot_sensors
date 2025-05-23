import paho.mqtt.client as mqtt
import modules.config as config
import json
from time import sleep
from datetime import datetime
from zoneinfo import ZoneInfo
from modules.database_connector import get_db
from modules.schemas import Dht11Data
from modules.models import ClimateData
import threading
# import config

USERNAME = config.MQTT_USERNAME
PASSWORD = config.MQTT_PASSWORD
BROKER = config.BROKER_ADDRESS
PORT = config.BROKER_PORT
TOPIC = 'dht11/measurement'
STATUS_TOPIC = 'system/status/ping'
RESPONSE_TOPIC = 'system/status/pong'

CLIENT_ID = 'BackendServer'

pong_received = threading.Event()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        # print('Connected to MQTT server')
        client.subscribe(TOPIC)
        client.subscribe(STATUS_TOPIC)
    else:
        print('MQTT server is not running')


def on_message(client, userdata, msg):
    # print(f"[MQTT] Received message on topic {msg.topic}: {msg.payload}") #### DEBUG
    if msg.topic == STATUS_TOPIC:
        pong_received.set()

    else:
        db = next(get_db())
        message = msg.payload.decode()
        json_data = json.loads(message)

        time_now =datetime.now(ZoneInfo('Europe/Bratislava'))
        formatted_time = time_now.strftime("%Y-%m-%d %H:%M:%S")

        json_data['measured_at'] = formatted_time

        validated_data = Dht11Data(**json_data)

        new_measurement = ClimateData(temperature=validated_data.temperature,
                                    humidity=validated_data.humidity,
                                    measured_at=validated_data.measured_at)
        
        db.add(new_measurement)
        db.commit()

client = mqtt.Client(client_id=CLIENT_ID)
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

def mqtt_start():
    while True:
        try:
            client.connect(BROKER, PORT)
            client.loop_start()
            print('Connected to Mosquitto')
            break
        except ConnectionRefusedError as e:
            print("Can't connect to Mosquitto!")
            print(f'ERROR: {e}')
            sleep(2.5)