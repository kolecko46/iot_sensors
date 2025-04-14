import modules.schemas as schemas
from fastapi import APIRouter, HTTPException, status, Depends, Response
from modules.database_connector import get_db
from modules.models import Base, ClimateData
from sqlalchemy.orm import Session
from modules.utils import create_plot

router = APIRouter()

@router.get('/dht11')
def get_data(db:Session=Depends(get_db)):
    data = db.query(ClimateData).order_by(ClimateData.measured_at.desc()).limit(10).all()

    timestamps = []
    temperatures = []

    for time_record in data:
        timestamps.append(time_record.measured_at.strftime("%H:%M:%S"))

    for temp_record in data:
        temperatures.append(temp_record.temperature)

    timestamps = timestamps[::-1]
    temperatures = temperatures[::-1]

    img = create_plot(timestamps, temperatures)

    return Response(content=img.getvalue(), media_type="image/png")