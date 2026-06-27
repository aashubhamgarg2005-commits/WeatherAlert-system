from datetime import datetime, timedelta
import logging

from sqlalchemy.orm import Session
from sqlalchemy import exists

from warehouse.schema.star_schema import (
    weather_measurements,
    Date,
    Rain,
    Precip_in,
)

logger = logging.getLogger(__name__)


class DataCleanupService:

    def __init__(self, db: Session):
        self.db = db

    def clean_old_weather_data(self, days: int = 7):
        """
        Delete weather records older than 'days'
        """

        try:
            cutoff_date = datetime.now() - timedelta(days=days)

            logger.info(f"Deleting records older than {cutoff_date}")

            old_records = (
                self.db.query(weather_measurements)
                .join(Date, weather_measurements.date_id == Date.date_id)
                .filter(Date.date < cutoff_date)
                .all()
            )

            deleted = len(old_records)

            for record in old_records:
                self.db.delete(record)

            self.db.commit()

            logger.info(f"{deleted} weather records deleted.")

            self.remove_orphan_dates()
            self.remove_orphan_rain()
            self.remove_orphan_precip()

            return {
                "status": "success",
                "deleted_weather_records": deleted
            }

        except Exception as e:

            self.db.rollback()

            logger.exception("Cleanup Failed")

            raise e

    def remove_orphan_dates(self):

        deleted = (
            self.db.query(Date)
            .filter(
                ~exists().where(
                    weather_measurements.date_id == Date.date_id
                )
            )
            .delete(synchronize_session=False)
        )

        self.db.commit()

        logger.info(f"{deleted} orphan dates deleted.")

    def remove_orphan_rain(self):

        deleted = (
            self.db.query(Rain)
            .filter(
                ~exists().where(
                    weather_measurements.rain_id == Rain.rain_id
                )
            )
            .delete(synchronize_session=False)
        )

        self.db.commit()

        logger.info(f"{deleted} orphan rain records deleted.")

    def remove_orphan_precip(self):

        deleted = (
            self.db.query(Precip_in)
            .filter(
                ~exists().where(
                    weather_measurements.precip_id == Precip_in.precip_in_id
                )
            )
            .delete(synchronize_session=False)
        )

        self.db.commit()

        logger.info(f"{deleted} orphan precipitation records deleted.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from backend.app.core.database_connection import get_db
    db = next(get_db())
    try:
        service = DataCleanupService(db=db)
        result = service.clean_old_weather_data(days=7)
        print(f"Result: {result}")
    finally:
        db.close()
