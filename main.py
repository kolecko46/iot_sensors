from fastapi import FastAPI
from routers import users_api, measure_api, status
from modules.mqtt_connector import mqtt_start
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

mqtt_start()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def root():
    return{'message':'hello world'}

app.include_router(users_api.router)
app.include_router(measure_api.router)
app.include_router(status.router)