from src.FinSight.components.test_db_connection_03 import DBConnectionTest
from src.FinSight.config.configuration import ConfigurationManager
from src.FinSight import logger

STAGE_NAME = "Database Connection Test"

class DBConnectionTestPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            # Load configuration and get DB URL
            config_manager = ConfigurationManager()
            db_url = config_manager.get_db_url()

            # Test database connection
            db_connection_test = DBConnectionTest(db_url)
            db_connection_test.test_connection()

        except Exception as e:
            logger.exception(f"Error in {STAGE_NAME}: {e}")
            raise e


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        pipeline = DBConnectionTestPipeline()
        pipeline.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
