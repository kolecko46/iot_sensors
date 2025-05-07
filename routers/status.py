from fastapi import APIRouter, Depends
from modules.database_connector import check_db_connection, get_db
from sqlalchemy.orm import Session
from modules.mqtt_connector import client as mqtt_client, pong_received

router = APIRouter()

STATUS_TOPIC = 'system/status/ping'

@router.get('/status')
def get_status(db:Session=Depends(get_db)):
    db_status = check_db_connection(db)

    pong_received.clear()
    mqtt_client.publish(STATUS_TOPIC, payload='{"check":"status"}')

    mqtt_ok = pong_received.wait(timeout=10)

    return {"Status":
        {"database_status": db_status,
        "mosquitto_status": "ok" if mqtt_ok else "no_response"}
    }