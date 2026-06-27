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

class CurrentWeatherTransformer(BaseTransformer):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms raw current weather data into a cleaned format.
        """
        try:
            if df.empty:
                logging.warning("Input DataFrame is empty.")
                return df

            # Convert string representations of dictionaries to actual dictionaries
            df_copy = df.copy()
            df_copy['location'] = df_copy['location'].apply(lambda x: literal_eval(x) if isinstance(x, str) else x)
            df_copy['current'] = df_copy['current'].apply(lambda x: literal_eval(x) if isinstance(x, str) else x)

            # Flatten nested JSON structures
            # Extracting 'location' and 'current' columns which are usually dictionaries in the raw response
            location_df = pd.json_normalize(df_copy['location'])
            current_df = pd.json_normalize(df_copy['current'])

            # Combine flattened data
            transformed_df = pd.concat([location_df, current_df], axis=1)

            # Convert epoch to datetime
            if 'last_updated_epoch' in transformed_df.columns:
                transformed_df['last_updated_dt'] = pd.to_datetime(transformed_df['last_updated_epoch'], unit='s')

            # Rename columns for consistency
            transformed_df.columns = [col.replace('.', '_').lower() for col in transformed_df.columns]

            logging.info("Current weather data transformation successful.")
            return transformed_df

        except Exception as e:
            logging.error(f"Error transforming current weather data: {e}", exc_info=True)
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
    Main execution function for current weather data transformation.
    """
    # Define file paths relative to script location
    script_dir = Path(__file__).parent.parent.parent
    input_file = script_dir / "data" / "raw" / "current_weather_data.csv"
    output_dir = script_dir / "data" / "cleaned"
    output_file = output_dir / "current_weather_data_cleaned.csv"
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load raw data
    raw_df = load_data(str(input_file))
    
    if raw_df.empty:
        logging.warning("No data to process. Exiting.")
        return
    
    # Transform data
    transformer = CurrentWeatherTransformer()
    cleaned_df = transformer.transform(raw_df)
    
    # Save cleaned data
    if not cleaned_df.empty:
        save_data(cleaned_df, str(output_file))
        logging.info(f"Transformation completed. Output shape: {cleaned_df.shape}")
    else:
        logging.warning("No data to save after transformation.")


if __name__ == "__main__":
    main()
