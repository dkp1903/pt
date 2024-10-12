# data_handler.py

import pandas as pd
import logging

logger = logging.getLogger(__name__)

def process_multi_index_data(stock_data: pd.DataFrame, remaining_tickers: list):
    """
    Processes a MultiIndex DataFrame to extract prices for multiple tickers.
    
    :param stock_data: The MultiIndex DataFrame returned from yfinance.
    :param remaining_tickers: List of tickers to process.
    :return: A dictionary containing ticker prices or 'ticker not found'.
    """
    cached_prices = {}

    for ticker in remaining_tickers:
        if ticker in stock_data.columns.get_level_values(1):  # Check for ticker in columns
            price = float(stock_data["Close"][ticker].iloc[-1])  # Convert to float
            cached_prices[ticker] = price
            logger.info(f"Ticker setting : {ticker} - {price}")
        else:
            logger.info(f"Ticker not found : {ticker}")
            cached_prices[ticker] = "ticker not found"

    return cached_prices

def process_single_index_data(stock_data: pd.DataFrame, remaining_tickers: list):
    """
    Processes a single-index DataFrame to extract prices for a single ticker.
    
    :param stock_data: The single-index DataFrame returned from yfinance.
    :param remaining_tickers: List of tickers to process.
    :return: A dictionary containing ticker prices.
    """
    cached_prices = {}

    for ticker in remaining_tickers:
        price = float(stock_data["Close"].iloc[-1])  # Convert to float
        cached_prices[ticker] = price
        logger.info(f"Ticker setting : {ticker} - {price}")

    return cached_prices

def process_stock_data(stock_data: pd.DataFrame, remaining_tickers: list):
    """
    Determines the structure of the DataFrame and processes it accordingly.
    
    :param stock_data: The DataFrame returned from yfinance.
    :param remaining_tickers: List of tickers to process.
    :return: A dictionary containing ticker prices.
    """
    if stock_data.empty:
        logger.error("Received empty stock data.")
        return {ticker: "ticker not found" for ticker in remaining_tickers}

    # Determine if the DataFrame is MultiIndexed or single-indexed
    if stock_data.columns.nlevels == 2:
        return process_multi_index_data(stock_data, remaining_tickers)
    else:
        return process_single_index_data(stock_data, remaining_tickers)
