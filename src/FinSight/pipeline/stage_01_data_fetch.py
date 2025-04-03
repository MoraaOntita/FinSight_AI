import sys
import os

# Add src directory to sys.path
sys.path.append(os.path.abspath("src"))

from src.FinSight.config.configuration import ConfigurationManager
from FinSight.components.fetch_apple_data_01 import DataFetch
from src.FinSight import logger

STAGE_NAME = "Data Fetching"

class DataFetchPipeline:
    def __init__(self):
        pass

    def main(self):
        config_manager = ConfigurationManager()
        data_fetch_config = config_manager.get_data_fetch_config()
        data_fetch = DataFetch(config=data_fetch_config)
        data_fetch.fetch_data()


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataFetchPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
