# stock_fetcher.py

import yfinance as yf
import requests_cache
from app.caching import cache_get, cache_set
import logging
from .data_handler import process_stock_data  # Import the new data handler

logger = logging.getLogger(__name__)

# Set cache limit to 1D, since we get daily prices
requests_cache.install_cache('yfinance_cache', expire_after=86400)

async def fetch_stock_prices(tickers: list):
    """Fetches stock prices using yfinance for the given tickers."""
    logger.info("Fetching stock prices data")
    cached_prices = {}
    remaining_tickers = set()  # Use a set to store unique tickers
    
    # Check Redis cache for each ticker
    for ticker in tickers:
        cached_price = await cache_get(ticker)
        if cached_price is not None:
            cached_prices[ticker] = float(cached_price)  # Convert to plain float
        else:
            remaining_tickers.add(ticker)  # Add to set for uniqueness
    
    if not remaining_tickers:
        return cached_prices

    # Convert the set back to a list for yfinance API call
    unique_tickers = list(remaining_tickers)

    # Fetch prices for remaining tickers using yfinance
    try:
        tickers_str = " ".join(unique_tickers)
        stock_data = yf.download(tickers_str, period="1d")
        
        logger.info(f"Stock Data : {stock_data}")

        # Use the new data handler to process stock data
        return process_stock_data(stock_data, unique_tickers)
        
    except Exception as e:
        logger.error(f"Error fetching US stock prices for {unique_tickers}: {e}")
        return {ticker: "ticker not found" for ticker in unique_tickers}
