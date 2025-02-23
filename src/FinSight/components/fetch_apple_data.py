import yfinance as yf
import pandas as pd
import sys
import os

# Add src directory to sys.path
sys.path.append(os.path.abspath("src"))

from src.FinSight.entity.config_entity import DataFetchConfig
from src.FinSight import logger

class DataFetch:
    def __init__(self, config: DataFetchConfig):
        self.config = config

    def fetch_data(self):
        try:
            logger.info(f"Fetching stock data for {self.config.ticker}...")

            # Fetch historical stock data
            stock = yf.Ticker(self.config.ticker)
            data = stock.history(
                period=self.config.period, 
                start=self.config.start_date, 
                end=self.config.end_date
            )

            if data.empty:
                logger.warning(f"No stock data found for {self.config.ticker}.")
            else:
                # Save data to CSV
                data.to_csv(self.config.output_file)
                logger.info(f"Stock data saved to {self.config.output_file}")

        except Exception as e:
            logger.error(f"Error fetching stock data: {str(e)}")
            logger.exception(e)
