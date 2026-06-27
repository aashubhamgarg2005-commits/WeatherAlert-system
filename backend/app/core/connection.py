from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = Config()
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Connection:
    def __init__(self):
        self.engine = engine
        self.Session = SessionLocal
        self.session = self.Session()

    def get_session(self):
        return self.session

    def close(self):
        self.session.close()

    def dispose(self):
        self.engine.dispose()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)
    preference_columns = {
        column["name"] for column in inspector.get_columns("user_preference")
    }
    if "state_name" not in preference_columns:
        with engine.begin() as connection:
            connection.execute(
                text("ALTER TABLE user_preference ADD COLUMN state_name VARCHAR")
            )
