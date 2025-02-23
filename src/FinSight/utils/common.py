import os
import yaml
from box import ConfigBox
from ensure import ensure_annotations
import sys

# Add src directory to sys.path
sys.path.append(os.path.abspath("src"))

from pathlib import Path
from src.FinSight import logger

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Reads YAML file and returns as ConfigBox."""
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"YAML file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except Exception as e:
        logger.error(f"Error reading YAML file: {e}")
        raise e

@ensure_annotations
def create_directories(path_to_directories: list):
    """Create directories if they don't exist."""
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        logger.info(f"Created directory at: {path}")
