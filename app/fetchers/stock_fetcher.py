import yfinance as yf
import requests_cache
from app.caching import cache_get, cache_set
import logging
import pandas as pd

logger = logging.getLogger(__name__)

# Set cache limit to 1D, since we get daily prices
requests_cache.install_cache('yfinance_cache', expire_after=86400)

async def fetch_stock_prices(tickers: list):
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

        if stock_data.empty:
            logger.error("Received empty stock data.")
            return {ticker: "ticker not found" for ticker in remaining_tickers}

        if stock_data.columns.nlevels == 2:
            for ticker in remaining_tickers:
                if ticker in stock_data.columns.get_level_values(1):
                    price = float(stock_data["Close"][ticker].iloc[-1])  # Convert to float
                    cached_prices[ticker] = price
                    logger.info(f"Ticker setting : {ticker} - {price}")
                    await cache_set(ticker, price)
                else:
                    logger.info(f"Ticker not found : {ticker}")
                    cached_prices[ticker] = "ticker not found"
        else:
            for ticker in remaining_tickers:
                price = float(stock_data["Close"].iloc[-1])  # Convert to float
                cached_prices[ticker] = price
                logger.info(f"Ticker setting : {ticker} - {price}")
                await cache_set(ticker, price)

        return cached_prices
    except Exception as e:
        logger.error(f"Error fetching US stock prices for {remaining_tickers}: {e}")
        return {ticker: "ticker not found" for ticker in remaining_tickers}
