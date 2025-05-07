from dotenv import load_dotenv
import os

load_dotenv('/home/miro/envs/.env')
# load_dotenv('C:/Users/Miro/python/BackEnd_raspberry/iot_sensors/modules/.env')

DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_NAME = os.getenv('DATABASE_NAME')

DATABASE_URL = f"mysql+mysqlconnector://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:3306/{DATABASE_NAME}"

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCES_TOKEN_EXPIRE_TIME = os.getenv('ACCES_TOKEN_EXPIRE_TIME')

MQTT_USERNAME = os.getenv('MQTT_USERNAME')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')
BROKER_ADDRESS = os.getenv('BROKER_ADDRESS')
BROKER_PORT = int(os.getenv('BROKER_PORT'))