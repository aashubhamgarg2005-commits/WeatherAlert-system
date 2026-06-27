from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,Float,ForeignKey,DateTime,Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Location(Base):
    __tablename__ = "Dim_location"
    location_id = Column(Integer, primary_key=True,autoincrement=True)
    location_name = Column(String)
    location_region = Column(String)
    location_country = Column(String)
    location_latitude = Column(Float)
    location_longitude = Column(Float)

class Weather_icon(Base):
    __tablename__ = "Dim_weather_icon"
    Weather_icon_id = Column(Integer, primary_key=True,autoincrement=True)
    weather_icon_name = Column(String)
    weather_icon_url = Column(String)

class Date(Base):
    __tablename__ = "Dim_date"
    date_id = Column(Integer, primary_key=True,autoincrement=True)
    date = Column(DateTime)
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    day_of_week = Column(Integer)

class Condition(Base):
    __tablename__ = "Dim_condition"
    condition_id = Column(Integer, primary_key=True, autoincrement=True)
    condition_text = Column(String)
    condition_code = Column(Integer)
    condition_icon_url = Column(String)

class Rain(Base):
    __tablename__ = "Fact_rain"
    rain_id = Column(Integer, primary_key=True,autoincrement=True)
    will_it_rain = Column(Boolean)
    will_it_snow = Column(Boolean)
    chance_of_rain = Column(Integer)
    chance_of_snow = Column(Integer)

class Precip_in(Base):
    __tablename__ = "Dim_precip_in"
    precip_in_id = Column(Integer, primary_key=True,autoincrement=True)
    day_totalprecip_mm = Column(Float)
    day_totalprecip_in = Column(Float)

class weather_measurements(Base):
    __tablename__ = "Fact_weather_measurements"
    measurement_id = Column(Integer, primary_key=True,autoincrement=True)
    location_id = Column(Integer,ForeignKey("Dim_location.location_id"),nullable=False)
    Weather_icon_id = Column(Integer,ForeignKey("Dim_weather_icon.Weather_icon_id"),nullable=False)
    date_id = Column(Integer,ForeignKey("Dim_date.date_id"),nullable=False)
    condition_id = Column(Integer,ForeignKey("Dim_condition.condition_id"),nullable=False)
    rain_id = Column(Integer,ForeignKey("Fact_rain.rain_id"),nullable=False)
    precip_id = Column(Integer,ForeignKey("Dim_precip_in.precip_in_id"), nullable=True)
    is_day = Column(Boolean)
    temperature_in_celsius = Column(Float)
    temperature_in_fahrenheit = Column(Float)
    maximum_temperature_in_celsius = Column(Float)
    maximum_temperature_in_fahrenheit = Column(Float)
    minimum_temperature_in_celsius = Column(Float)
    minimum_temperature_in_fahrenheit = Column(Float)
    average_temperature_in_celsius = Column(Float)
    average_temperature_in_fahrenheit = Column(Float)
    uv = Column(Float)
    wind_mph = Column(Float)
    wind_kph = Column(Float)
    maximum_wind_speed = Column(Float)
    wind_degree = Column(Float)
    wind_direction = Column(String)
    wind_gust_speed = Column(Float)
    gust_mph = Column(Float)
    gust_kph = Column(Float)
    humidity = Column(Float)
    pressure_mb = Column(Float)
    pressure_in = Column(Float)
    cloud = Column(Float)
    feelslike_temperature_in_celsius = Column(Float)
    feelslike_temperature_in_fahrenheit = Column(Float)
    vis_km = Column(Float)
    vis_miles = Column(Float)
    precip_mm = Column(Float)
    precip_in = Column(Float)
    sunrise = Column(DateTime)
    sunset = Column(DateTime)
    location = relationship(Location)
    weather_icon = relationship(Weather_icon)
    date = relationship(Date)
    condition = relationship(Condition)
    rain = relationship(Rain)
    precip = relationship(Precip_in)
