import sys
import os
from pathlib import Path

# Add src directory to sys.path
sys.path.append(os.path.abspath("src"))

from src.FinSight.config.configuration import ConfigurationManager
from FinSight.components.data_storage_02 import DataStorage
from src.FinSight import logger

STAGE_NAME = "Data Storage Stage"

class DataStoragePipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_fetch_config = config.get_data_fetch_config()  # Get fetch config to access output file
        data_storage_config = config.get_data_storage_config()
        data_storage = DataStorage(
            config=data_storage_config,
            data_fetch_output_file=Path(data_fetch_config.output_file)  # Pass the CSV file path
        )
        data_storage.store_data()

if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataStoragePipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e