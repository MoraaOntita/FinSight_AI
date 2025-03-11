from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from FinSight.config.configuration import ConfigurationManager
from dotenv import load_dotenv
import os

def setup_langchain_with_deepseek():
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

        # Define a prompt template for generating SQL queries
        prompt_template = (
            "You are an assistant that generates SQL queries based on natural language questions.\n"
            "Given the following question, produce a valid SQL query for the provided database.\n\n"
            "Question: {question}\n\nSQL Query:"
        )
        prompt = PromptTemplate(template=prompt_template, input_variables=["question"])

        # Create the chain manually using LLMChain
        chain = LLMChain(llm=llm, prompt=prompt)

        print("LangChain with DeepSeek setup successful!")
        print(f"Connected to database: {db_config.db_url.split('@')[1]}")
        print(f"Table included: {db_config.table_name}")
        print(f"Using LLM: {lc_config.llm_model}")

        # Test with a sample query
        sample_query = "What was the highest closing price of AAPL stock in 2023?"
        generated_sql = chain.run(question=sample_query)

        print(f"Sample query: {sample_query}")
        print(f"Generated SQL: {generated_sql}")

        # Execute the generated query
        result = db.run(generated_sql)
        print(f"Query result: {result}")

    except Exception as e:
        print(f"Failed to setup LangChain with DeepSeek: {str(e)}")

if __name__ == "__main__":
    setup_langchain_with_deepseek()
