import os
from pathlib import Path
import sys

# Add src directory to sys.path
sys.path.append(os.path.abspath("src"))

from FinSight.utils.common import read_yaml, create_directories
from src.FinSight.entity.config_entity import DataFetchConfig
from src.FinSight import logger

CONFIG_FILE_PATH = Path("config/config.yaml")


class ConfigurationManager:
    def __init__(self, config_filepath=CONFIG_FILE_PATH):
        self.config = read_yaml(config_filepath)
        create_directories([self.config.artifacts_root])

    def get_data_fetch_config(self) -> DataFetchConfig:
        config = self.config.data_fetch
        create_directories([config.root_dir])

        return DataFetchConfig(
            root_dir=Path(config.root_dir),
            ticker=config.ticker,
            period=config.period,
            start_date=config.start_date,
            end_date=config.end_date,
            output_file=Path(config.output_file),
        )
