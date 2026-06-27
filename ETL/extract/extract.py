import logging
import sys
from pathlib import Path
import pandas as pd
import requests

# Ensure the project root is on the Python path when run as a script.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from config import Config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class Extract:

    def __init__(self):
        self.config = Config()
        # Hardcoded locations moved to an instance variable for easier adjustments
        self.locations = [
            "Meerut",
            "Delhi",
            "Noida",
            "Gurgaon",
            "Faridabad",
            "Mumbai",
        ]

    def fetch_current_weather_data(self) -> list:
        """Fetches current weather data for predefined locations from the API."""
        if not self.config.API_KEY or not self.config.WEATHER_CURRENT_URL:
            logging.error(
                "Missing API configuration for current weather. "
                "Check WEATHER_DATA_API_KEY and WEATHER_CURRENT_DATA_URL."
            )
            return []

        current_data = []
        try:
            for loc in self.locations:
                url = self.config.WEATHER_CURRENT_URL
                params = {
                    "q": loc,
                    "key": self.config.API_KEY,
                    "units": "metric",
                }

                response = requests.get(url, params=params, timeout=10)

                if response.status_code == 200:
                    weather_data = response.json()
                    current_data.append(weather_data)
                    logging.info(
                        f"Weather data fetched successfully for location: {loc}"
                    )
                else:
                    logging.error(
                        f"Failed to fetch data for {loc}. Status Code: {response.status_code}. Response: {response.text}"
                    )

            return current_data
        except Exception as e:
            logging.error(
                "An error occurred during the data extraction loop",
                exc_info=True,
            )
            return current_data

    def fetch_forecast_weather_data(self) -> list:
        """Fetches forecast weather data for predefined locations from the API."""
        if not self.config.API_KEY or not self.config.WEATHER_FORECAST_URL:
            logging.error(
                "Missing API configuration for forecast weather. "
                "Check WEATHER_DATA_API_KEY and WEATHER_FORECAST_DATA_URL."
            )
            return []

        forecast_data = []
        try:
            for loc in self.locations:
                url = self.config.WEATHER_FORECAST_URL
                params = {
                    "q": loc,
                    "key": self.config.API_KEY,
                    "days": 7,
                }

                response = requests.get(url, params=params, timeout=10)

                if response.status_code == 200:
                    weather_forecast_data = response.json()
                    forecast_data.append(weather_forecast_data)
                    logging.info(
                        f"Weather forecast data fetched successfully for location: {loc}"
                    )
                else:
                    logging.error(
                        f"Failed to fetch forecast data for location : {loc} , response : {response.text}"
                    )

            return forecast_data
        except Exception as e:
            logging.error(
                "An error occurred during the forecast data extraction loop",
                exc_info=True,
            )
            return forecast_data

    def store_current_data(self, current_data: list):
        """Stores current weather data into the Bronze layer as a CSV."""
        if not current_data:
            logging.warning("No data available to store into Bronze layer.")
            return

        try:
            df = pd.DataFrame(current_data)

            # Dynamically determine the project root directory
            project_root = Path(__file__).resolve().parents[2]
            file_dir = project_root / "data" / "raw"

            # Create directory if it doesn't exist
            file_dir.mkdir(parents=True, exist_ok=True)
            file_path = file_dir / "current_weather_data.csv"

            df.to_csv(file_path, index=False)
            logging.info(f"Weather data stored successfully at {file_path}")
        except Exception as e:
            logging.error(
                "Failed to store weather data into Bronze layer", exc_info=True
            )

    def store_forecast_data(self, forecast_data: list):
        """Stores forecast weather data into the Bronze layer as a CSV."""
        if not forecast_data:
            logging.warning("No data available to store into Bronze layer.")
            return

        try:
            df = pd.DataFrame(forecast_data)

            # Dynamically determine the project root directory
            project_root = Path(__file__).resolve().parents[2]
            file_dir = project_root / "data" / "raw"

            # Create directory if it doesn't exist
            file_dir.mkdir(parents=True, exist_ok=True)
            file_path = file_dir / "forecast_weather_data.csv"

            df.to_csv(file_path, index=False)
            logging.info(f"Weather data stored successfully at {file_path}")
        except Exception as e:
            logging.error(
                "Failed to store weather data into Bronze layer", exc_info=True
            )

    def fetch_data(self) -> dict:
        """Orchestrates fetching both current and forecast data."""
        return {
            "current": self.fetch_current_weather_data(),
            "forecast": self.fetch_forecast_weather_data(),
        }

    def store_into_bronze(self, raw_data: dict):
        """Orchestrates storing both datasets into the Bronze layer."""
        self.store_current_data(raw_data.get("current", []))
        self.store_forecast_data(raw_data.get("forecast", []))


if __name__ == "__main__":
    extract = Extract()
    
    # Clean orchestration execution flow
    logging.info("Starting Weather ETL Extraction Process...")
    raw_weather_data = extract.fetch_data()
    extract.store_into_bronze(raw_weather_data)
    logging.info("Weather ETL Extraction Process completed successfully.")