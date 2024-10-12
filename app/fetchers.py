import httpx
from app.caching import cache_get, cache_set
from app.config import settings

# API URLs (replace with real endpoints)
US_STOCK_API_URL = settings.US_STOCK_API_URL
INDIA_MUTUAL_FUND_API_URL = settings.INDIA_MUTUAL_FUND_API_URL

# Fetch US stock prices
async def fetch_us_stock_price(ticker: str):
    # Check cache first
    cached_price = await cache_get(ticker)
    if cached_price:
        return cached_price
    
    # Fetch from external API
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{US_STOCK_API_URL}/{ticker}", timeout=5)
            if response.status_code == 200:
                price = response.json().get("price")
                await cache_set(ticker, price)
                return price
    except httpx.RequestError as e:
        print(f"Error fetching US stock price for {ticker}: {e}")
    return None

# Fetch Indian mutual fund prices
async def fetch_indian_mutual_fund_price(ticker: str):
    cached_price = await cache_get(ticker)
    if cached_price:
        return cached_price

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{INDIA_MUTUAL_FUND_API_URL}/{ticker}", timeout=5)
            if response.status_code == 200:
                price = response.json().get("price")
                await cache_set(ticker, price)
                return price
    except httpx.RequestError as e:
        print(f"Error fetching Indian mutual fund price for {ticker}: {e}")
    return None

# Get prices for all tickers
async def get_prices(tickers):
    results = []
    for ticker_info in tickers:
        ticker = ticker_info.ticker
        country = ticker_info.country.lower()

        if country == 'us':
            price = await fetch_us_stock_price(ticker)
        elif country == 'india':
            price = await fetch_indian_mutual_fund_price(ticker)
        else:
            price = None
        
        results.append({"ticker": ticker, "price": price})
    
    return results
