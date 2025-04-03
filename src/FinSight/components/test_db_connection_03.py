from sqlalchemy import create_engine, text
from FinSight import logger

class DBConnectionTest:
    def __init__(self, db_url: str):
        self.db_url = db_url

    def test_connection(self):
        try:
            # Create engine and test connection
            engine = create_engine(self.db_url)
            with engine.connect() as connection:
                logger.info(f"Successfully connected to database: {self.db_url.split('@')[1]}")
                # Use text() for raw SQL in SQLAlchemy 2.0+
                version = connection.execute(text("SELECT version();")).fetchone()[0]
                logger.info(f"PostgreSQL Version: {version}")
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            logger.exception(e)
