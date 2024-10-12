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
    remaining_tickers = []
    
    # Check Redis cache for each ticker
    for ticker in tickers:
        cached_price = await cache_get(ticker)
        if cached_price is not None:
            cached_prices[ticker] = float(cached_price)  # Convert to plain float
        else:
            remaining_tickers.append(ticker)
    
    if not remaining_tickers:
        return cached_prices

    # Fetch prices for remaining tickers using yfinance
    try:
        tickers_str = " ".join(remaining_tickers)
        stock_data = yf.download(tickers_str, period="1d")
        
        logger.info(f"Stock Data : {stock_data}")

        # Use the new data handler to process stock data
        return process_stock_data(stock_data, remaining_tickers)
        
    except Exception as e:
        logger.error(f"Error fetching US stock prices for {remaining_tickers}: {e}")
        return {ticker: "ticker not found" for ticker in remaining_tickers}
