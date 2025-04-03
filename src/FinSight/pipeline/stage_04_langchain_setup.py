from src.FinSight.components.setup_langchain_04 import setup_langchain_db
from src.FinSight import logger

STAGE_NAME = "LangChain Setup"

class LangChainSetupPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            # Call the LangChain setup function
            setup_langchain_db()

        except Exception as e:
            logger.exception(f"Error in {STAGE_NAME}: {e}")
            raise e

if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        pipeline = LangChainSetupPipeline()
        pipeline.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
