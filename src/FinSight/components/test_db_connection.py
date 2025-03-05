# src/FinSight/components/test_db_connection.py
from sqlalchemy import create_engine, text
from FinSight.config.configuration import ConfigurationManager

def test_db_connection():
    try:
        # Get configuration
        config_manager = ConfigurationManager()
        db_config = config_manager.get_data_storage_config()
        
        # Create engine and test connection
        engine = create_engine(db_config.db_url)
        with engine.connect() as connection:
            print(f"Successfully connected to database: {db_config.db_url.split('@')[1]}")
            # Use text() for raw SQL in SQLAlchemy 2.0+
            version = connection.execute(text("SELECT version();")).fetchone()[0]
            print(f"PostgreSQL Version: {version}")
            
    except Exception as e:
        print(f"Database connection failed: {str(e)}")

if __name__ == "__main__":
    test_db_connection()