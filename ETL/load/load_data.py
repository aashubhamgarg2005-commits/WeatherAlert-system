import ast
import logging
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

from backend.app.core.database_connection import Connection
from warehouse.schema.star_schema import (
    Condition,
    Date,
    Location,
    Precip_in,
    Rain,
    Weather_icon,
    weather_measurements,
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


class Load_data:

    @staticmethod
    def parse_date(value):
        if pd.isna(value):
            return None
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(str(value))
        except ValueError:
            try:
                return pd.to_datetime(value)
            except Exception:
                return None

    @staticmethod
    def normalize_condition(value):
        if isinstance(value, dict):
            return value
        if isinstance(value, str):
            try:
                parsed = ast.literal_eval(value)
                if isinstance(parsed, dict):
                    return parsed
            except (ValueError, SyntaxError):
                pass
        return {'text': str(value), 'icon': None, 'code': None}

    @staticmethod
    def get_or_create(session, model, defaults=None, **kwargs):
        instance = session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        params = dict(kwargs)
        if defaults:
            params.update(defaults)
        instance = model(**params)
        session.add(instance)
        session.flush()  # Use flush instead of commit to get IDs without pushing to disk early
        return instance

    @staticmethod
    def load_cleaned_csv(file_path: Path) -> pd.DataFrame:
        if not file_path.exists():
            logging.error('Cleaned data file not found: %s', file_path)
            return pd.DataFrame()
        try:
            df = pd.read_csv(file_path)
            logging.info('Loaded cleaned CSV %s rows=%s', file_path, len(df))
            return df
        except Exception as exc:
            logging.error('Failed to read cleaned CSV %s: %s', file_path, exc)
            return pd.DataFrame()

    def load_current_weather(self, session, df: pd.DataFrame) -> int:
        if df.empty:
            logging.warning('No current weather rows to load.')
            return 0

        loaded = 0
        try:
            for _, row in df.iterrows():
                location = self.get_or_create(
                    session,
                    Location,
                    location_name=row.get('name'),
                    location_region=row.get('region'),
                    location_country=row.get('country'),
                    location_latitude=row.get('lat'),
                    location_longitude=row.get('lon'),
                )

                condition_data = self.normalize_condition(row.get('condition_text'))
                condition = self.get_or_create(
                    session,
                    Condition,
                    condition_text=condition_data.get('text'),
                    condition_code=row.get('condition_code') if row.get('condition_code') is not None else condition_data.get('code'),
                    condition_icon_url=row.get('condition_icon') or condition_data.get('icon'),
                )

                icon_url = row.get('condition_icon') or condition_data.get('icon')
                weather_icon = self.get_or_create(
                    session,
                    Weather_icon,
                    weather_icon_name=condition_data.get('text'),
                    weather_icon_url=icon_url,
                )

                date_value = self.parse_date(row.get('last_updated_dt') or row.get('localtime'))
                date = self.get_or_create(
                    session,
                    Date,
                    date=date_value,
                    year=date_value.year if date_value else None,
                    month=date_value.month if date_value else None,
                    day=date_value.day if date_value else None,
                    day_of_week=date_value.isoweekday() if date_value else None,
                )

                rain = Rain(
                    will_it_rain=bool(row.get('will_it_rain', False)),
                    will_it_snow=bool(row.get('will_it_snow', False)),
                    chance_of_rain=int(row.get('chance_of_rain') or 0),
                    chance_of_snow=int(row.get('chance_of_snow') or 0),
                )
                session.add(rain)
                session.flush()

                precip = Precip_in(
                    day_totalprecip_mm=float(row.get('precip_mm') or 0.0),
                    day_totalprecip_in=float(row.get('precip_in') or 0.0),
                )
                session.add(precip)
                session.flush()

                measurement = weather_measurements(
                    location_id=location.location_id,
                    Weather_icon_id=weather_icon.Weather_icon_id,
                    date_id=date.date_id,
                    condition_id=condition.condition_id,
                    rain_id=rain.rain_id,
                    is_day=bool(row.get('is_day')) if row.get('is_day') is not None else None,
                    temperature_in_celsius=row.get('temp_c'),
                    temperature_in_fahrenheit=row.get('temp_f'),
                    maximum_temperature_in_celsius=row.get('temp_c'),
                    maximum_temperature_in_fahrenheit=row.get('temp_f'),
                    minimum_temperature_in_celsius=row.get('temp_c'),
                    minimum_temperature_in_fahrenheit=row.get('temp_f'),
                    average_temperature_in_celsius=row.get('temp_c'),
                    average_temperature_in_fahrenheit=row.get('temp_f'),
                    uv=row.get('uv'),
                    wind_mph=row.get('wind_mph'),
                    wind_kph=row.get('wind_kph'),
                    maximum_wind_speed=row.get('gust_kph') or row.get('wind_kph'),
                    wind_degree=row.get('wind_degree'),
                    wind_direction=row.get('wind_dir'),
                    wind_gust_speed=row.get('gust_kph') or row.get('gust_mph'),
                    gust_mph=row.get('gust_mph'),
                    gust_kph=row.get('gust_kph'),
                    humidity=row.get('humidity'),
                    pressure_mb=row.get('pressure_mb'),
                    pressure_in=row.get('pressure_in'),
                    cloud=row.get('cloud'),
                    feelslike_temperature_in_celsius=row.get('feelslike_c'),
                    feelslike_temperature_in_fahrenheit=row.get('feelslike_f'),
                    vis_km=row.get('vis_km'),
                    vis_miles=row.get('vis_miles'),
                    precip_id=precip.precip_in_id,
                    precip_mm=row.get('precip_mm'),
                    precip_in=row.get('precip_in'),
                    sunrise=self.parse_date(row.get('sunrise')),
                    sunset=self.parse_date(row.get('sunset')),
                )
                session.add(measurement)
                loaded += 1

            session.commit()  # Atomically commit the entire batch together
        except Exception as e:
            session.rollback()
            logging.error("Failed loading current weather batch, rolling back: %s", e)
            raise e

        logging.info('Loaded %s current weather records', loaded)
        return loaded

    def load_forecast_weather(self, session, df: pd.DataFrame) -> int:
        if df.empty:
            logging.warning('No forecast weather rows to load.')
            return 0

        loaded = 0
        try:
            for _, row in df.iterrows():
                location = self.get_or_create(
                    session,
                    Location,
                    location_name=row.get('name'),
                    location_region=row.get('region'),
                    location_country=row.get('country'),
                    location_latitude=row.get('lat'),
                    location_longitude=row.get('lon'),
                )

                condition_data = self.normalize_condition(row.get('day_condition'))
                condition = self.get_or_create(
                    session,
                    Condition,
                    condition_text=condition_data.get('text'),
                    condition_code=int(condition_data.get('code')) if condition_data.get('code') else None,
                    condition_icon_url=condition_data.get('icon'),
                )

                weather_icon = self.get_or_create(
                    session,
                    Weather_icon,
                    weather_icon_name=condition_data.get('text'),
                    weather_icon_url=condition_data.get('icon'),
                )

                date_value = self.parse_date(row.get('date_dt') or row.get('date'))
                date = self.get_or_create(
                    session,
                    Date,
                    date=date_value,
                    year=date_value.year if date_value else None,
                    month=date_value.month if date_value else None,
                    day=date_value.day if date_value else None,
                    day_of_week=date_value.isoweekday() if date_value else None,
                )

                rain = Rain(
                    will_it_rain=bool(row.get('day_daily_will_it_rain', 0)),
                    will_it_snow=bool(row.get('day_daily_will_it_snow', 0)),
                    chance_of_rain=int(row.get('day_daily_chance_of_rain') or 0),
                    chance_of_snow=int(row.get('day_daily_chance_of_snow') or 0),
                )
                session.add(rain)
                session.flush()

                precip = Precip_in(
                    day_totalprecip_mm=float(row.get('day_totalprecip_mm', 0.0)),
                    day_totalprecip_in=float(row.get('day_totalprecip_in', 0.0)),
                )
                session.add(precip)
                session.flush()

                measurement = weather_measurements(
                    location_id=location.location_id,
                    Weather_icon_id=weather_icon.Weather_icon_id,
                    date_id=date.date_id,
                    condition_id=condition.condition_id,
                    rain_id=rain.rain_id,
                    is_day=None,
                    temperature_in_celsius=row.get('day_avgtemp_c'),
                    temperature_in_fahrenheit=row.get('day_avgtemp_f'),
                    maximum_temperature_in_celsius=row.get('day_maxtemp_c'),
                    maximum_temperature_in_fahrenheit=row.get('day_maxtemp_f'),
                    minimum_temperature_in_celsius=row.get('day_mintemp_c'),
                    minimum_temperature_in_fahrenheit=row.get('day_mintemp_f'),
                    average_temperature_in_celsius=row.get('day_avgtemp_c'),
                    average_temperature_in_fahrenheit=row.get('day_avgtemp_f'),
                    uv=row.get('day_uv'),
                    wind_mph=row.get('day_maxwind_mph'),
                    wind_kph=row.get('day_maxwind_kph'),
                    maximum_wind_speed=row.get('day_maxwind_kph'),
                    wind_degree=None,
                    wind_direction=None,
                    wind_gust_speed=None,
                    gust_mph=None,
                    gust_kph=None,
                    humidity=row.get('day_avghumidity'),
                    pressure_mb=None,
                    pressure_in=None,
                    cloud=None,
                    feelslike_temperature_in_celsius=None,
                    feelslike_temperature_in_fahrenheit=None,
                    vis_km=row.get('day_avgvis_km'),
                    vis_miles=row.get('day_avgvis_miles'),
                    precip_id=precip.precip_in_id,
                    precip_mm=row.get('day_totalprecip_mm'),
                    precip_in=row.get('day_totalprecip_in'),
                    sunrise=self.parse_date(row.get('astro_sunrise')),
                    sunset=self.parse_date(row.get('astro_sunset')),
                )
                session.add(measurement)
                loaded += 1

            session.commit()  # Atomically commit the entire batch together
        except Exception as e:
            session.rollback()
            logging.error("Failed loading forecast weather batch, rolling back: %s", e)
            raise e

        logging.info('Loaded %s forecast weather records', loaded)
        return loaded

    def main(self, mode: str = 'both') -> None:
        connection = Connection()
        session = connection.get_session()
        try:
            data_root = ROOT_DIR / 'data' / 'cleaned'
            if mode in ('current', 'both'):
                current_file = data_root / 'current_weather_data_cleaned.csv'
                current_df = self.load_cleaned_csv(current_file)
                if not current_df.empty:
                    self.load_current_weather(session, current_df)

            if mode in ('forecast', 'both'):
                forecast_file = data_root / 'forecast_weather_data_cleaned.csv'
                forecast_df = self.load_cleaned_csv(forecast_file)
                if not forecast_df.empty:
                    self.load_forecast_weather(session, forecast_df)

        finally:
            session.close()
            connection.dispose()


if __name__ == '__main__':
    import argparse

    load_data = Load_data()

    parser = argparse.ArgumentParser(description='Load cleaned weather CSV data into the database.')
    parser.add_argument(
        '--mode',
        choices=['current', 'forecast', 'both'],
        default='both',
        help='Load current weather, forecast weather, or both.',
    )
    args = parser.parse_args()
    load_data.main(args.mode)