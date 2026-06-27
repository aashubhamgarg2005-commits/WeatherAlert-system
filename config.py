import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

class Config:
    def __init__(self):
        # Database
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PORT = os.getenv("DB_PORT")
        self.DB_NAME = os.getenv("DB_NAME")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")

        # API
        self.API_KEY = os.getenv("WEATHER_DATA_API_KEY")
        self.WEATHER_CURRENT_URL = os.getenv("WEATHER_CURRENT_DATA_URL")
        self.WEATHER_FORECAST_URL = os.getenv("WEATHER_FORECAST_DATA_URL")

        # java web token

        self.secret_key = os.getenv("SECRET_KEY")
        self.algorithem = os.getenv("ALGORITHEM")
        self.time_limit = os.getenv("ACCESS_TOKEN-EXPIRE_MINUTS")
        

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False