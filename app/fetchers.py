import yfinance as yf
import requests_cache
from app.caching import cache_get, cache_set
from app.config import settings
import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up requests_cache for smarter scraping and caching in yfinance
# Cache duration set to 1 day (24 hours) - adjust as per requirement
requests_cache.install_cache('yfinance_cache', expire_after=86400)

# Fetch US stock prices using yfinance (supports multiple tickers in a single API call)
async def fetch_us_stock_prices(tickers: list):
    logger.info("US")
    cached_prices = {}
    remaining_tickers = []
    
    for ticker in tickers:
        cached_price = await cache_get(ticker)
        if cached_price:
            cached_prices[ticker] = cached_price
        else:
            remaining_tickers.append(ticker)
    
    if not remaining_tickers:
        return cached_prices

    # Use yfinance to fetch the stock prices for the remaining tickers
    try:
        tickers_str = " ".join(remaining_tickers)
        stock_data = yf.download(tickers_str, period="1d")
        
        if len(remaining_tickers) == 1:
            price = stock_data["Close"].iloc[-1]
            cached_prices[remaining_tickers[0]] = price
            await cache_set(remaining_tickers[0], price)
        else:
            for ticker in remaining_tickers:
                price = stock_data["Close"][ticker].iloc[-1]
                cached_prices[ticker] = price
                await cache_set(ticker, price)
        
        return cached_prices
    except Exception as e:
        print(f"Error fetching US stock prices for {remaining_tickers}: {e}")
        return {ticker: None for ticker in remaining_tickers}

# Updated function to fetch Indian mutual fund prices using ISIN and API
async def fetch_indian_mutual_fund_prices(isins: list):
    logger.info("India")
    cached_prices = {}
    remaining_isins = []

    # Check Redis cache first for all ISINs
    for isin in isins:
        cached_price = await cache_get(isin)
        if cached_price:
           cached_prices[isin] = cached_price
        else:
            remaining_isins.append(isin)
    
    # If all ISINs are cached, return the cached prices
    if not remaining_isins:
        return cached_prices

    # Fetch data from the external API for remaining ISINs
    async with httpx.AsyncClient() as client:
        for isin in remaining_isins:
            try:
                url=settings.INDIA_MUTUAL_FUND_API_URL
                response = await client.get(f"{url}{isin}", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    nav = data.get("nav")
                    cached_prices[isin] = nav
                    # Cache the result in Redis for future requests
                    await cache_set(isin, nav)
                else:
                    print(f"Failed to fetch data for ISIN: {isin}, status code: {response.status_code}")
                    cached_prices[isin] = None
            except httpx.RequestError as e:
                print(f"Error fetching mutual fund data for ISIN {isin}: {e}")
                cached_prices[isin] = None
    
    return cached_prices

# Main function to fetch prices for both US stocks and Indian mutual funds
async def get_prices(tickers_info):
    print("Getting prices")
    us_tickers = [ticker_info.ticker for ticker_info in tickers_info if ticker_info.country.lower() == 'us']
    india_isins = [ticker_info.ticker for ticker_info in tickers_info if ticker_info.country.lower() == 'india']
    
    results = {}
    logger.info("Getting prices")

    if us_tickers:
        us_prices = await fetch_us_stock_prices(us_tickers)
        results.update(us_prices)
    
    if india_isins:
        india_prices = await fetch_indian_mutual_fund_prices(india_isins)
        results.update(india_prices)
    
    # Return the results for both US stocks and Indian mutual funds
    return [{"ticker": ticker, "price": results[ticker]} for ticker in results]
