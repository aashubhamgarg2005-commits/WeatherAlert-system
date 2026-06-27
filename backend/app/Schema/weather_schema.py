from pydantic import BaseModel
from datetime import date

class WeatherResponse(BaseModel):
    city:str
    tempreture:float
    wind_speed:float
    precipitation:float
    condition:str

    class Config:
        from_attributes = True