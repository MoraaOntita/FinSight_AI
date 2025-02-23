import sys
import os

# Add src directory to sys.path
sys.path.append(os.path.abspath("src"))

from src.FinSight import logger
from src.FinSight.pipeline.stage_01_data_fetch import DataFetchPipeline

STAGE_NAME = "Data Fetching"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    fetch_pipeline = DataFetchPipeline()
    fetch_pipeline.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e
