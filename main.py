import sys
import os
from pathlib import Path

# Add src directory to sys.path
sys.path.append(os.path.abspath("src"))

from src.FinSight import logger
from src.FinSight.pipeline.stage_01_data_fetch import DataFetchPipeline
from src.FinSight.pipeline.stage_02_data_storage import DataStoragePipeline
from src.FinSight.pipeline.stage_03_db_connection_test import DBConnectionTestPipeline
from src.FinSight.pipeline.stage_04_langchain_setup import LangChainSetupPipeline
from src.FinSight.pipeline.stage_05_langchain_with_deepseek import LangChainDeepSeekPipeline

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

# Execute DB Connection Test Stage
STAGE_NAME = "DB Connection Test"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    db_connection_pipeline = DBConnectionTestPipeline()
    db_connection_pipeline.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

# Execute LangChain Setup Stage
STAGE_NAME = "LangChain Setup"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    langchain_pipeline = LangChainSetupPipeline()
    langchain_pipeline.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e


STAGE_NAME = "LangChain with DeepSeek"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")

    # Get dynamic query input from the user
    query_input = input("Please enter your query: ")
    logger.info(f"Processing query: {query_input}")

    # Initialize and run LangChainDeepSeekPipeline
    langchain_deepseek_pipeline = LangChainDeepSeekPipeline(query_input)
    langchain_deepseek_pipeline.main()

    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e