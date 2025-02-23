import pandas as pd
from sqlalchemy import create_engine
from FinSight import logger
from FinSight.entity.config_entity import DataStorageConfig

class DataStorage:
    def __init__(self, config: DataStorageConfig):
        self.config = config

    def store_data(self):
        try:
            df = pd.read_csv(self.config.local_data_file)
            engine = create_engine(self.config.db_url)
            df.to_sql(self.config.table_name, engine, if_exists="replace", index=False)
            logger.info(f"Data successfully inserted into PostgreSQL table: {self.config.table_name}")
        except Exception as e:
            logger.exception(f"Error storing data: {e}")
            raise e
