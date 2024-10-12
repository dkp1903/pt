import yfinance as yf
import requests_cache
from app.caching import cache_get, cache_set
from app.config import settings
import httpx

# Set up requests_cache for smarter scraping and caching in yfinance
# Cache duration set to 1 day (24 hours) - adjust as per requirement
requests_cache.install_cache('yfinance_cache', expire_after=86400)

# Fetch US stock prices using yfinance (supports multiple tickers in a single API call)
async def fetch_us_stock_prices(tickers: list):
    # Check cache first for all tickers in Redis
    cached_prices = {}
    remaining_tickers = []
    
    for ticker in tickers:
        cached_price = await cache_get(ticker)
        if cached_price:
            cached_prices[ticker] = cached_price
        else:
            remaining_tickers.append(ticker)
    
    # If all tickers are cached, return the cached prices
    if not remaining_tickers:
        return cached_prices

    # Use yfinance to fetch the stock prices for the remaining tickers
    try:
        tickers_str = " ".join(remaining_tickers)
        stock_data = yf.download(tickers_str, period="1d")
        
        # If there's only one ticker left, stock_data is a single dataframe
        if len(remaining_tickers) == 1:
            price = stock_data["Close"].iloc[-1]
            cached_prices[remaining_tickers[0]] = price
            await cache_set(remaining_tickers[0], price)
        else:
            for ticker in remaining_tickers:
                # Get the closing price for each ticker
                price = stock_data["Close"][ticker].iloc[-1]
                cached_prices[ticker] = price
                await cache_set(ticker, price)
        
        return cached_prices
    except Exception as e:
        print(f"Error fetching US stock prices for {remaining_tickers}: {e}")
        return {ticker: None for ticker in remaining_tickers}

# Fetch Indian mutual fund prices (mocked as this is a placeholder for real API calls)
async def fetch_indian_mutual_fund_price(ticker: str):
    cached_price = await cache_get(ticker)
    if cached_price:
        return cached_price

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.INDIA_MUTUAL_FUND_API_URL}/{ticker}", timeout=5)
            if response.status_code == 200:
                price = response.json().get("price")
                await cache_set(ticker, price)
                return price
    except httpx.RequestError as e:
        print(f"Error fetching Indian mutual fund price for {ticker}: {e}")
    return None

# Main function to fetch prices for both US stocks and Indian mutual funds
async def get_prices(tickers_info):
    us_tickers = [ticker_info.ticker for ticker_info in tickers_info if ticker_info.country.lower() == 'us']
    india_tickers = [ticker_info.ticker for ticker_info in tickers_info if ticker_info.country.lower() == 'india']
    
    results = {}

    if us_tickers:
        us_prices = await fetch_us_stock_prices(us_tickers)
        results.update(us_prices)
    
    for india_ticker in india_tickers:
        price = await fetch_indian_mutual_fund_price(india_ticker)
        results[india_ticker] = price
    
    # Return the results for both US stocks and Indian mutual funds
    return [{"ticker": ticker, "price": results[ticker]} for ticker in results]
