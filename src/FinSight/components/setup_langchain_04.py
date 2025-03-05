from langchain_community.utilities.sql_database import SQLDatabase
from FinSight.config.configuration import ConfigurationManager

def setup_langchain_db():
    try:
        # Initialize configuration
        config_manager = ConfigurationManager()
        db_config = config_manager.get_data_storage_config()

        # Initialize PostgreSQL database connection for LangChain
        db = SQLDatabase.from_uri(
            db_config.db_url,
            include_tables=[db_config.table_name],
            sample_rows_in_table_info=2
        )

        print("LangChain database setup successful!")
        print(f"Connected to: {db_config.db_url.split('@')[1]}")
        print(f"Table included: {db_config.table_name}")
        
        # Test by getting table info
        table_info = db.get_table_info()
        print(f"Table info:\n{table_info}")

        # Optional: Run a simple direct SQL query to verify
        result = db.run(f"SELECT COUNT(*) FROM {db_config.table_name}")
        print(f"Number of rows in {db_config.table_name}: {result}")

    except Exception as e:
        print(f"Failed to setup LangChain database: {str(e)}")

if __name__ == "__main__":
    setup_langchain_db()
