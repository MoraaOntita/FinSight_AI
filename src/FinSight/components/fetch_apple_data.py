import yfinance as yf
import pandas as pd
import sys
import os
import concurrent.futures
from functools import wraps

# Add src directory to sys.path
sys.path.append(os.path.abspath("src"))

from src.FinSight.entity.config_entity import DataFetchConfig
from src.FinSight import logger

def log_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Executing {func.__name__}...")
        result = func(*args, **kwargs)
        logger.info(f"Finished {func.__name__}.")
        return result
    return wrapper

class DataFetch:
    def __init__(self, config: DataFetchConfig):
        self.config = config

    @log_execution
    def fetch_data(self):
        try:
            logger.info(f"Fetching stock data for {self.config.ticker}...")
            data = self._get_stock_data()
            if data.empty:
                logger.warning(f"No stock data found for {self.config.ticker}.")
            else:
                self._save_data(data)
        except Exception as e:
            logger.error(f"Error fetching stock data: {str(e)}")
            logger.exception(e)

    @log_execution
    def _get_stock_data(self):
        stock = yf.Ticker(self.config.ticker)
        return stock.history(
            period=self.config.period, 
            start=self.config.start_date, 
            end=self.config.end_date
        )

    @log_execution
    def _save_data(self, data: pd.DataFrame):
        data.to_csv(self.config.output_file)
        logger.info(f"Stock data saved to {self.config.output_file}")

    @staticmethod
    def fetch_multiple_data(configs):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(DataFetch(config).fetch_data) for config in configs]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"Error in concurrent fetch: {str(e)}")
                    logger.exception(e)