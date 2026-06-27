from sqlalchemy.orm import Session
from datetime import date as date_type
from backend.app.repository.weather_repository import (
    get_weather_condition_by_city,
    get_weather_future_by_city,
    get_latest_weather_by_city,
    get_rain_data_by_city,
    get_weather_by_date,
    get_weather_icon_by_city,
    get_wind_data_by_city,
    city_exists
)

def fetch_today_weather(db:Session,city:str):
    city_exists(db=db,city=city)
    return get_latest_weather_by_city(db=db,city=city)

def fetch_future_weather(db:Session,city:str):
    city_exists(db=db,city=city)
    return get_weather_future_by_city(db=db,city=city)

def fetch_rain_weather(db:Session,city:str):
    city_exists(db=db,city=city)
    return get_rain_data_by_city(db=db,city=city)

def fetch_weather_by_date(db:Session,date:date_type):
    return get_weather_by_date(db=db,weather_date=date)

def fetch_weather_condition(db:Session,city:str):
    city_exists(db=db,city=city)
    return get_weather_condition_by_city(db=db,city=city)

def fetch_weather_icon(db:Session,city:str):
    city_exists(db=db,city=city)
    return get_weather_icon_by_city(db=db,city=city)

def fetch_wind_data(db:Session,city:str):
    city_exists(db=db,city=city)
    return get_wind_data_by_city(db=db,city=city)
