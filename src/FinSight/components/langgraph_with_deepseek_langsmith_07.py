from FinSight.components.langgraph_with_deepseek_06 import (
    AgentState, initialize_components, generate_sql, execute_query, 
    handle_error, build_graph
)
from langsmith import Client
from langchain_core.runnables import RunnableConfig
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up LangSmith environment variables
load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "FinSight-Agent"

# Override nodes to include LangSmith config
def generate_sql_with_tracing(state: AgentState, llm, table_info, config: RunnableConfig) -> AgentState:
    return generate_sql(state, llm, table_info)  # Pass config implicitly via LangChain's invoke

def execute_query_with_tracing(state: AgentState, db, config: RunnableConfig) -> AgentState:
    return execute_query(state, db)  # No LLM call here, so config isn't used directly

def build_graph_with_langsmith(db, llm, table_info):
    workflow = build_graph(db, llm, table_info)  # Use base graph builder
    # No need to redefine nodes; LangSmith tracing works via config
    return workflow

def run_langgraph_agent_with_langsmith():
    try:
        # Initialize components and LangSmith client
        db, llm, db_config, lc_config = initialize_components()
        langsmith_api_key = os.getenv("LANGSMITH_API_KEY")
        if not langsmith_api_key:
            raise ValueError("LANGSMITH_API_KEY not found in environment variables")
        langsmith_client = Client()
        table_info = db.get_table_info()

        # Build graph (reuses base graph with tracing implicitly handled)
        app = build_graph_with_langsmith(db, llm, table_info)

        # Test with a sample query
        sample_query = "What was the highest closing price of AAPL stock in 2023?"
        initial_state = {
            "question": sample_query,
            "table_info": table_info,
            "generated_sql": "",
            "query_result": "",
            "error": "",
            "attempts": 0
        }

        # Run with LangSmith tracing
        config = {"configurable": {"thread_id": "fin-agent-001"}}
        result = app.invoke(initial_state, config=config)

        # Log to LangSmith
        langsmith_client.create_run(
            name="FinSightAgentRun",
            run_type="chain",
            inputs={"question": sample_query},
            outputs=result,
            project_name="FinSight-Agent"
        )

        print("LangGraph with DeepSeek and LangSmith setup successful!")
        print(f"Connected to database: {db_config.db_url.split('@')[1]}")
        print(f"Table included: {db_config.table_name}")
        print(f"Using LLM: {lc_config.llm_model}")
        print(f"Sample query: {sample_query}")
        print(f"Generated SQL: {result['generated_sql']}")
        if result.get("error"):
            print(f"Error: {result['error']}")
        else:
            print(f"Query result: {result['query_result']}")

    except Exception as e:
        logger.error(f"Failed to run agent with LangSmith: {str(e)}")
        print(f"Failed to setup LangGraph with DeepSeek and LangSmith: {str(e)}")

if __name__ == "__main__":
    run_langgraph_agent_with_langsmith()