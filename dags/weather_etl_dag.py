from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2026, 6, 27),
}

with DAG(
    dag_id="weather_etl_pipeline",
    default_args=default_args,
    description="Daily Weather ETL Pipeline",
    schedule_interval="0 6 * * *",
    catchup=False,
    tags=["weather", "etl"],
) as dag:

    def extract_task():
        from ETL.extract.extract import Extract
        extractor = Extract()
        raw_data = extractor.fetch_data()
        extractor.store_into_bronze(raw_data)

    def transform_current_task():
        from ETL.transform.clean_current_weather_data import main
        main()

    def transform_forecast_task():
        from ETL.transform.clean_forecast_weather_data import main
        main()

    def load_task():
        from ETL.load.load_data import Load_data
        loader = Load_data()
        loader.main(mode="both")

    def cleanup_task():
        from ETL.refresh_database.delete_historical_data import DataCleanupService
        from backend.app.core.database_connection import get_db
        db = next(get_db())
        try:
            service = DataCleanupService(db=db)
            result = service.clean_old_weather_data(days=7)
            print(f"Cleanup result: {result}")
        finally:
            db.close()

    t1 = PythonOperator(task_id="extract_weather_data", python_callable=extract_task)
    t2 = PythonOperator(task_id="transform_current_weather", python_callable=transform_current_task)
    t3 = PythonOperator(task_id="transform_forecast_weather", python_callable=transform_forecast_task)
    t4 = PythonOperator(task_id="load_weather_data", python_callable=load_task)
    t5 = PythonOperator(task_id="cleanup_old_data", python_callable=cleanup_task)

    t1 >> [t2, t3] >> t4 >> t5