from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session 
from datetime import date
from backend.app.core.database_connection import get_db
from backend.app.services.weather_services import (fetch_future_weather,
                                                   fetch_rain_weather,
                                                   fetch_today_weather,
                                                   fetch_weather_by_date,
                                                   fetch_weather_condition,
                                                   city_exists,
                                                   fetch_wind_data,
                                                   fetch_weather_icon
                                                )
from backend.app.services.alert_service import (genrate_forecast_alert,
                                                genrate_weather_alert)
from backend.app.Schema.weather_schema import WeatherResponse
from backend.app.Schema.alert_schema import AlertResponse

router = APIRouter(
    prefix="/alert",
    tags=["Weather Alert"]
)

@router.get("/today_alert/{city}")
def today_weather_alert(
    city:str,db:Session = Depends(get_db)
):
    weather = fetch_today_weather(db=db,city=city)
    if weather is None:
        raise HTTPException(
            status_code=404,
            detail="Weather data not found"
        )
    alert = genrate_weather_alert(weather=weather)
    return {
        "city":city,
        "alerts":alert
    }

@router.get("/forecast_alert/{city}")
def forecast_weather_alert(
    city:str,
    db:Session=Depends(get_db)
):
    forecast = fetch_future_weather(db=db,city=city)
    if not forecast:
        raise HTTPException(
            status_code=404,
            detail="Forecast data not found"
        )

    alert = genrate_forecast_alert(forecast_record=forecast)
    return{
        "city":city,
        "forecast_alert":alert
    }
@router.get("/today_weather/{city}")
def get_today_weather(city: str, db: Session = Depends(get_db)):
    weather = fetch_today_weather(db=db, city=city)
    if weather is None:
        raise HTTPException(
            status_code=404,
            detail="No weather data found for this city"
        )
    return {
        "city": city,
        "tempreture_in_celsius": weather.temperature_in_celsius,
        "humidity": weather.humidity,
        "wind_kph": weather.wind_kph,
        "wind_direction": weather.wind_direction,
        "precip_mm": weather.precip_mm,
        "cloud": weather.cloud,
        "condition": weather.condition.condition_text if weather.condition else None,
        "uv": weather.uv,
        "feelslike_celsius": weather.feelslike_temperature_in_celsius,
    }
@router.get("/forecast_weather/{city}")
def get_forecast_weather(city:str,db:Session = Depends(get_db)):
    forecast = fetch_future_weather(db=db,city=city)
    return {
        "city": city,
        "forecast": [
            {
                "temperature": item.temperature_in_celsius,
                "max_temperature": item.maximum_temperature_in_celsius,
                "min_temperature": item.minimum_temperature_in_celsius,
                "humidity": item.humidity,
                "wind_kph": item.wind_kph,
                "precip_mm": item.precip_mm,
                "uv": item.uv,
            }
            for item in forecast
        ]
    }
    

@router.get("/weather_by_date/{date}")
def get_weather_by_date(date:date,db:Session=Depends(get_db)):
    weather = fetch_weather_by_date(db=db,date=date)
    return {
        "weather":weather
    }

@router.get("/wind_by_city/{city}")
def get_wind_city(city:str,db:Session = Depends(get_db)):
    wind = fetch_wind_data(db=db,city=city)
    return{
        "wind":dict(wind._mapping)
    }

@router.get("/rain_city/{city}")
def get_rain_by_city(city:str,db:Session = Depends(get_db)):
    rain = fetch_rain_weather(db=db,city=city)
    print(type(rain))
    return{
        "rain":dict(rain._mapping)
    }

@router.get("/condition/{city}")
def get_condition_by_city(city:str,db:Session = Depends(get_db)):
    condition = fetch_weather_condition(db=db,city=city)
    return {
        "condition":dict(condition._mapping)
    }

@router.get("/weather_icon/{city}")
def weather_icon(city:str,db:Session = Depends(get_db)):
    weather_icon = fetch_weather_icon(db=db,city=city)
    return {
        "weather_icon":dict(weather_icon._mapping)
    }

