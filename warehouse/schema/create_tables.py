import logging
from pathlib import Path

from config import Config
from backend.core.database_connection import Connection
from .star_schema import Base
from backend.modals.user import users,UserProfile,UserPreference



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CreateTables:
    def __init__(self):
        self.connection = Connection()
        self.engine = self.connection.engine

    def create_tables(self):
        try:
            logger.info("Creating tables in the database...")
            Base.metadata.create_all(self.engine)
            logger.info("Tables created successfully.")
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
        finally:
            self.connection.close()

if __name__ == "__main__":
    creator = CreateTables()
    creator.create_tables()



