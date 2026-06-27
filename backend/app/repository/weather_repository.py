from sqlalchemy.orm import Session
from warehouse.schema.star_schema import (Condition,
                                          Date,
                                          Location,
                                          weather_measurements,
                                          Weather_icon,
                                          Precip_in,
                                          Rain)
import logging
from datetime import datetime, timedelta, date as date_type

logger = logging.getLogger(__name__)

# fetch today data weather data
def get_latest_weather_by_city(db: Session, city: str):
    today = datetime.now().date()
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = start_of_day + timedelta(days=1)

    weather = (
        db.query(weather_measurements)
        .join(Location, weather_measurements.location_id == Location.location_id)
        .join(Date, weather_measurements.date_id == Date.date_id)
        .filter(
            Location.location_name == city,
            Date.date >= start_of_day,
            Date.date < end_of_day,
        )
        .order_by(Date.date.desc())
        .first()
    )
    print(city)
    return weather

# fetch next 7 days weather data
def get_weather_future_by_city(db: Session, city: str):
    today = datetime.now().date()
    start_date = datetime.combine(today, datetime.min.time())
    end_date = start_date + timedelta(days=7)

    weather = (
        db.query(weather_measurements)
        .join(Location, weather_measurements.location_id == Location.location_id)
        .join(Date, weather_measurements.date_id == Date.date_id)
        .filter(
            Location.location_name == city,
            Date.date >= start_date,
            Date.date < end_date,
        )
        .all()
    )
    
    print(city)
    return weather


# fetch weather data by date
def get_weather_by_date(db: Session, weather_date: date_type):
    start_of_day = datetime.combine(weather_date, datetime.min.time())
    end_of_day = start_of_day + timedelta(days=1)

    weather = (
        db.query(weather_measurements)
        .join(Date, weather_measurements.date_id == Date.date_id)
        .join(Location, weather_measurements.location_id == Location.location_id)
        .filter(
            Date.date >= start_of_day,
            Date.date < end_of_day,
        )
        .first()
    
    )
    
    return weather
#  fetch wind data
def get_wind_data_by_city(db:Session,city:str):
    wind_data = (
        db.query(weather_measurements.wind_degree,weather_measurements.wind_direction,
                 weather_measurements.wind_kph,weather_measurements.wind_gust_speed,
                 weather_measurements.wind_mph,weather_measurements.maximum_wind_speed)
        .join(Location,weather_measurements.location_id == Location.location_id
              ).filter(Location.location_name.ilike(city))
              .first()
    )
    print(city)
    return wind_data

# fetch rain data by city
def get_rain_data_by_city(db: Session, city: str):
    rain_data = (
        db.query(weather_measurements.cloud,weather_measurements.precip_in,
                 weather_measurements.humidity,weather_measurements.precip_mm,
                 weather_measurements.pressure_in,weather_measurements.rain,
                 Rain.chance_of_rain,Rain.will_it_rain)
        .join(Rain, weather_measurements.rain_id == Rain.rain_id)
        .join(Location, weather_measurements.location_id == Location.location_id)
        .filter(Location.location_name.ilike(city))
        .first()
    )
    print(city)

    return rain_data

# fetch weather condition
def get_weather_condition_by_city(db:Session,city:str):
    weather_condition = (
        db.query(weather_measurements.cloud,weather_measurements.condition
                 ,weather_measurements.feelslike_temperature_in_celsius
                 ,weather_measurements.humidity,weather_measurements.gust_kph,
                 weather_measurements.precip,weather_measurements.sunrise,
                 weather_measurements.sunset,weather_measurements.uv)
        .join(Condition,weather_measurements.condition_id == Condition.condition_id)
        .join(Location,weather_measurements.location_id == Location.location_id)
        .filter(Location.location_name.ilike(city))
        .first()
    )
    print(city)
    return weather_condition

# weather icon 
def get_weather_icon_by_city(db:Session,city:str):
    weather_icon = (
        db.query(Weather_icon.weather_icon_url)
        .select_from(weather_measurements)
        .join(Weather_icon,weather_measurements.Weather_icon_id == Weather_icon.Weather_icon_id)
        .join(Location,weather_measurements.location_id == Location.location_id)
        .filter(Location.location_name.ilike(city))
        .first()
    )
    print(city)
    return weather_icon
# city validation
def city_exists(db: Session, city: str):
    result = (
        db.query(Location)
        .filter(Location.location_name.ilike(city))
        .first()
    )
    if result:
        return result
    else:
        raise ValueError("city not found")

