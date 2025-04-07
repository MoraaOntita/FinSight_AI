from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from FinSight.config.configuration import ConfigurationManager
from dotenv import load_dotenv
import os
from src.FinSight import logger

def setup_langchain_with_deepseek(query_input: str):  # Query is passed dynamically
    try:
        # Load environment variables
        load_dotenv()
        deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        if not deepseek_api_key:
            raise ValueError("DEEPSEEK_API_KEY not found in environment variables")

        # Initialize configuration
        config_manager = ConfigurationManager()
        db_config = config_manager.get_data_storage_config()
        lc_config = config_manager.get_langchain_config()

        # Initialize PostgreSQL database connection
        db = SQLDatabase.from_uri(
            db_config.db_url,
            include_tables=[db_config.table_name],
            sample_rows_in_table_info=2
        )

        # Initialize DeepSeek LLM via Groq
        llm = ChatGroq(
            api_key=deepseek_api_key,
            model=lc_config.llm_model,
            temperature=lc_config.temperature
        )

        # Fetch the prompt template from config for dynamic usage
        prompt_template = lc_config.prompt_template  # Dynamic loading of the prompt template
        prompt = PromptTemplate(template=prompt_template, input_variables=["question"])

        # Create the chain manually using LLMChain
        chain = LLMChain(llm=llm, prompt=prompt)

        logger.info("LangChain with DeepSeek setup successful!")
        logger.info(f"Connected to database: {db_config.db_url.split('@')[1]}")
        logger.info(f"Table included: {db_config.table_name}")
        logger.info(f"Using LLM: {lc_config.llm_model}")

        # Processing the dynamic query passed as an argument
        logger.info(f"Processing query: {query_input}")

        # Generate SQL from the dynamic query
        generated_sql = chain.run(question=query_input)
        logger.info(f"Generated SQL: {generated_sql}")

        # Execute the generated query
        result = db.run(generated_sql)
        logger.info(f"Query result: {result}")

    except Exception as e:
        logger.error(f"Failed to setup LangChain with DeepSeek: {str(e)}")

