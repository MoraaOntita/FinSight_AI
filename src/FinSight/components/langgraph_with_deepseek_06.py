from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
import operator
from FinSight.config.configuration import ConfigurationManager
from dotenv import load_dotenv
import os

# Define the state structure
class AgentState(TypedDict):
    question: str
    table_info: str
    generated_sql: str
    query_result: str
    error: str
    attempts: Annotated[int, operator.add]

# Initialize configuration and database globally
def initialize_components():
    load_dotenv()
    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
    if not deepseek_api_key:
        raise ValueError("DEEPSEEK_API_KEY not found in environment variables")

    config_manager = ConfigurationManager()
    db_config = config_manager.get_data_storage_config()
    lc_config = config_manager.get_langchain_config()

    db = SQLDatabase.from_uri(
        db_config.db_url,
        include_tables=[db_config.table_name],
        sample_rows_in_table_info=2
    )

    llm = ChatGroq(
        api_key=deepseek_api_key,
        model=lc_config.llm_model,
        temperature=lc_config.temperature
    )

    return db, llm, db_config, lc_config

# Node to generate SQL query
def generate_sql(state: AgentState, llm, table_info) -> AgentState:
    prompt_template = (
        "Given the following database schema:\n{table_info}\n\n"
        "Generate a valid SQL query for PostgreSQL to answer this question: {question}\n"
        "Return only the SQL query itself, without any explanation or additional text.\n"
        "Use the table name 'apple_stock_data'.\n"
        "Assume columns include 'date' (timestamp), 'close_price' (numeric), and others.\n"
        "Use date range syntax (e.g., date >= 'YYYY-MM-DD') for year-based queries."
    )
    prompt = PromptTemplate(template=prompt_template, input_variables=["table_info", "question"])
    chain = prompt | llm
    
    try:
        generated_sql = chain.invoke({"table_info": table_info, "question": state["question"]}).content
        return {"generated_sql": generated_sql, "attempts": 1}
    except Exception as e:
        return {"error": str(e), "attempts": 1}

# Node to execute SQL query
def execute_query(state: AgentState, db) -> AgentState:
    if state.get("error"):
        return state
    
    try:
        result = db.run(state["generated_sql"])
        return {"query_result": result}
    except Exception as e:
        return {"error": f"SQL execution failed: {str(e)}"}

# Node to handle errors and decide next steps
def handle_error(state: AgentState) -> str:
    if state.get("error") and state["attempts"] < 3:
        return "generate_sql"  # Retry if attempts < 3
    elif state.get("error"):
        return END  # End if max attempts reached
    return END  # End if successful

# Build the graph
def build_graph(db, llm, table_info):
    workflow = StateGraph(AgentState)
    
    workflow.add_node("generate_sql", lambda state: generate_sql(state, llm, table_info))
    workflow.add_node("execute_query", lambda state: execute_query(state, db))
    
    workflow.set_entry_point("generate_sql")
    workflow.add_edge("generate_sql", "execute_query")
    workflow.add_conditional_edges(
        "execute_query",
        handle_error,
        {
            "generate_sql": "generate_sql",
            END: END
        }
    )
    
    return workflow.compile()

def run_langgraph_agent():
    try:
        # Initialize components
        db, llm, db_config, lc_config = initialize_components()
        table_info = db.get_table_info()

        # Build and compile the graph
        app = build_graph(db, llm, table_info)

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

        # Run the graph
        result = app.invoke(initial_state)

        print("LangGraph with DeepSeek setup successful!")
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
        print(f"Failed to setup LangGraph with DeepSeek: {str(e)}")

if __name__ == "__main__":
    run_langgraph_agent()