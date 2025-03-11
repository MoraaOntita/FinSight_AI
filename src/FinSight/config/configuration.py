import os
from pathlib import Path
from FinSight.constants import CONFIG_FILE_PATH
from FinSight.utils.common import read_yaml, create_directories
from FinSight.entity.config_entity import DataFetchConfig, DataStorageConfig

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

    #FIX: Add this method
    def get_langchain_config(self):
        config = self.config.langchain
        return config
