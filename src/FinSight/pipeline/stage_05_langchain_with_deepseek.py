from src.FinSight.components.langchain_with_deepseek_05 import setup_langchain_with_deepseek
from src.FinSight import logger
import sys

STAGE_NAME = "LangChain with DeepSeek"

class LangChainDeepSeekPipeline:
    def __init__(self, query_input: str):
        self.query_input = query_input

    def main(self):
        try:
            # Call the LangChain setup function with dynamic query input
            setup_langchain_with_deepseek(self.query_input)
        except Exception as e:
            logger.exception(f"Error in {STAGE_NAME}: {e}")
            raise e

def run_pipeline(query_input: str):
    """Function to run the LangChain DeepSeek pipeline with dynamic input."""
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        pipeline = LangChainDeepSeekPipeline(query_input)
        pipeline.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logger.error("Query input not provided. Exiting.")
        sys.exit(1)

    query_input = sys.argv[1]  # Accepting query input from command line argument
    run_pipeline(query_input)
