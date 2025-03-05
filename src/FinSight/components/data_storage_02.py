import pandas as pd
from sqlalchemy import create_engine
from FinSight import logger
from FinSight.entity.config_entity import DataStorageConfig
from pathlib import Path

class DataStorage:
    def __init__(self, config: DataStorageConfig, data_fetch_output_file: Path):
        self.config = config
        self.data_fetch_output_file = data_fetch_output_file

    def store_data(self):
        try:
            # Use the configured CSV file path
            csv_file_path = Path(self.data_fetch_output_file)  

            # Check if file exists
            if not csv_file_path.exists():
                raise FileNotFoundError(f"CSV file not found: {csv_file_path}")

            df = pd.read_csv(csv_file_path)
            engine = create_engine(self.config.db_url)
            df.to_sql(self.config.table_name, engine, if_exists="replace", index=False)
            logger.info(f"Data successfully inserted into PostgreSQL table: {self.config.table_name}")
        except Exception as e:
            logger.exception(f"Error storing data: {e}")
            raise e
