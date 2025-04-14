from fastapi import FastAPI
from routers import books_api, users_api, measure_api
from modules.mqtt.mqtt_connector import mqtt_start

app = FastAPI()

mqtt_start()

@app.get('/')
def root():
    return{'message':'hello world'}

app.include_router(books_api.router)
app.include_router(users_api.router)
app.include_router(measure_api.router)