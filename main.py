from src.FinSight.pipeline.stage_01_data_fetch import DataFetchPipeline
from src.FinSight.pipeline.stage_02_data_storage import DataStoragePipeline
from src.FinSight.pipeline.stage_03_db_connection_test import DBConnectionTestPipeline
from src.FinSight import logger

def main():
    try:
        # Execute Data Fetching Stage
        logger.info(">>>>> stage Data Fetching started <<<<<<")
        fetch_pipeline = DataFetchPipeline()
        fetch_pipeline.main()
        logger.info(">>>>> stage Data Fetching completed <<<<<<")

        # Execute Data Storage Stage
        logger.info(">>>>> stage Data Storage started <<<<<<")
        data_storage_pipeline = DataStoragePipeline()
        data_storage_pipeline.main()
        logger.info(">>>>> stage Data Storage completed <<<<<<")

        # Execute DB Connection Test Stage
        logger.info(">>>>> stage DB Connection Test started <<<<<<")
        db_connection_pipeline = DBConnectionTestPipeline()
        db_connection_pipeline.main()
        logger.info(">>>>> stage DB Connection Test completed <<<<<<")

    except Exception as e:
        logger.exception(e)
        raise e


if __name__ == "__main__":
    main()
