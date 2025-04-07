import os
import yaml
from box import ConfigBox
from pathlib import Path
from FinSight import logger
from dotenv import load_dotenv

def read_yaml(path_to_yaml: Path) -> ConfigBox:
    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)
    logger.info(f"yaml file: {path_to_yaml} loaded successfully")
    return ConfigBox(content)

def create_directories(path_to_directories: list):
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        logger.info(f"Created directory at: {path}")


def load_environment_variables():
    load_dotenv()  # Load environment variables from .env file
    if not os.getenv("DEEPSEEK_API_KEY"):
        raise ValueError("DEEPSEEK_API_KEY not found in environment variables")
