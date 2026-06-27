import pandas as pd
import numpy as np
from datetime import datetime
from abc import ABC, abstractmethod
import logging
import os
from pathlib import Path
import json
from ast import literal_eval

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class BaseTransformer(ABC):
    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

class ForecastWeatherTransformer(BaseTransformer):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms raw forecast weather data into a cleaned format.
        """
        try:
            if df.empty:
                logging.warning("Input DataFrame is empty.")
                return df

            # Convert string representations of dictionaries to actual dictionaries
            df_copy = df.copy()
            df_copy['location'] = df_copy['location'].apply(lambda x: literal_eval(x) if isinstance(x, str) else x)
            df_copy['forecast'] = df_copy['forecast'].apply(lambda x: literal_eval(x) if isinstance(x, str) else x)

            records = []

            # For each row, expand forecastday entries into separate rows combined with location
            for _, row in df_copy.iterrows():
                loc = row.get('location') or {}
                forecast = row.get('forecast') or {}

                # forecast may be dict with key 'forecastday' -> list
                forecastdays = None
                if isinstance(forecast, dict):
                    forecastdays = forecast.get('forecastday')

                if not forecastdays:
                    # If no forecastday list, just combine location and forecast dict
                    rec = {}
                    rec.update(loc if isinstance(loc, dict) else {})
                    if isinstance(forecast, dict):
                        # flatten nested 'day' and 'astro' if present
                        day = forecast.pop('day', {}) if 'day' in forecast else {}
                        astro = forecast.pop('astro', {}) if 'astro' in forecast else {}
                        rec.update(forecast)
                        rec.update({f'day_{k}': v for k, v in day.items()})
                        rec.update({f'astro_{k}': v for k, v in astro.items()})
                    records.append(rec)
                else:
                    for fd in forecastdays:
                        # fd is a dict with keys: date, date_epoch, day, astro, hour
                        fd_copy = dict(fd)
                        day = fd_copy.pop('day', {})
                        astro = fd_copy.pop('astro', {})
                        # drop 'hour' to avoid large nested lists; keep if needed in future
                        fd_copy.pop('hour', None)

                        rec = {}
                        rec.update(loc if isinstance(loc, dict) else {})
                        rec.update(fd_copy)
                        rec.update({f'day_{k}': v for k, v in day.items()})
                        rec.update({f'astro_{k}': v for k, v in astro.items()})
                        records.append(rec)

            transformed_df = pd.DataFrame.from_records(records)

            # Convert epoch/date fields to datetime where applicable
            if 'date_epoch' in transformed_df.columns:
                transformed_df['date_dt'] = pd.to_datetime(transformed_df['date_epoch'], unit='s').dt.date

            if 'last_updated_epoch' in transformed_df.columns:
                transformed_df['last_updated_dt'] = pd.to_datetime(transformed_df['last_updated_epoch'], unit='s')
                transformed_df['last_updated_dt'] = transformed_df['last_updated_dt'].dt.date

            # Rename columns for consistency
            transformed_df.columns = [col.replace('.', '_').lower() for col in transformed_df.columns]

            logging.info("Forecast weather data transformation successful.")
            return transformed_df

        except Exception as e:
            logging.error(f"Error transforming forecast weather data: {e}", exc_info=True)
            return pd.DataFrame()


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load raw weather data from CSV file.

    Args:
        file_path: Path to the CSV file

    Returns:
        DataFrame containing the raw data
    """
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Data loaded successfully from {file_path}. Shape: {df.shape}")
        return df
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return pd.DataFrame()
    except Exception as e:
        logging.error(f"Error loading data from {file_path}: {e}", exc_info=True)
        return pd.DataFrame()


def save_data(df: pd.DataFrame, output_path: str) -> None:
    """
    Save cleaned data to CSV file.

    Args:
        df: DataFrame to save
        output_path: Path where to save the CSV file
    """
    try:
        df.to_csv(output_path, index=False)
        logging.info(f"Data saved successfully to {output_path}")
    except Exception as e:
        logging.error(f"Error saving data to {output_path}: {e}", exc_info=True)


def main():
    """
    Main execution function for forecast weather data transformation.
    """
    # Define file paths relative to repository root
    script_dir = Path(__file__).parent.parent.parent
    input_file = script_dir / "data" / "raw" / "forecast_weather_data.csv"
    output_dir = script_dir / "data" / "cleaned"
    output_file = output_dir / "forecast_weather_data_cleaned.csv"

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load raw data
    raw_df = load_data(str(input_file))

    if raw_df.empty:
        logging.warning("No data to process. Exiting.")
        return

    # Transform data
    transformer = ForecastWeatherTransformer()
    cleaned_df = transformer.transform(raw_df)

    # Save cleaned data
    if not cleaned_df.empty:
        save_data(cleaned_df, str(output_file))
        logging.info(f"Transformation completed. Output shape: {cleaned_df.shape}")
    else:
        logging.warning("No data to save after transformation.")


if __name__ == "__main__":
    main()
                    