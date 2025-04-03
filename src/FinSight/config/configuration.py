import os
from pathlib import Path
from FinSight.constants import CONFIG_FILE_PATH
from FinSight.utils.common import read_yaml, create_directories
from FinSight.entity.config_entity import DataFetchConfig, DataStorageConfig, DBConnectionConfig
from box import ConfigBox
from FinSight import logger
from typing import Any
from dataclasses import dataclass

class ConfigurationManager:
    def __init__(self):
        self.config = read_yaml(CONFIG_FILE_PATH)
        create_directories([self.config.artifacts_root])

    def get_data_fetch_config(self) -> DataFetchConfig:
        config = self.config.data_fetch
        create_directories([config.root_dir])

        return DataFetchConfig(
            root_dir=config.root_dir,
            ticker=config.ticker,
            start_date=config.start_date,
            end_date=config.end_date,
            period=config.period,
            output_file=config.output_file
        )

    def get_data_storage_config(self) -> DataStorageConfig:
        config = self.config.data_storage
        create_directories([Path(config.root_dir)])
        return DataStorageConfig(
            root_dir=Path(config.root_dir),
            db_url=config.db_url,
            table_name=config.table_name
        )

    def get_db_connection_config(self) -> DBConnectionConfig:
        """
        Returns the DBConnectionConfig object containing the database URL.
        """
        config = self.config.data_storage
        return DBConnectionConfig(db_url=config.db_url)

    def get_langchain_config(self):
        """
        Returns the langchain configuration, if available.
        """
        if 'langchain' in self.config:
            return self.config.langchain
        else:
            return None
        
    def get_db_url(self) -> str:
            """
            Returns the database URL from the data storage configuration.
            This method will now work again to return the db_url directly.
            """
            return self.config.data_storage.db_url