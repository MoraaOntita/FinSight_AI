import sys
import os
from pathlib import Path

# Add src directory to sys.path
sys.path.append(os.path.abspath("src"))

from src.FinSight import logger
from src.FinSight.pipeline.stage_01_data_fetch import DataFetchPipeline
from src.FinSight.pipeline.stage_02_data_storage import DataStoragePipeline

# Execute Data Fetching Stage
STAGE_NAME = "Data Fetching"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    fetch_pipeline = DataFetchPipeline()
    fetch_pipeline.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

# Execute Data Storage Stage
STAGE_NAME = "Data Storage Stage"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    data_storage = DataStoragePipeline()
    data_storage.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e