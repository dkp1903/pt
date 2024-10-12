# mutual_fund_fetcher.py

import httpx
from app.caching import cache_get, cache_set
import logging

logger = logging.getLogger(__name__)

async def fetch_mutual_fund_prices(isins: list, api_url: str):
    """Fetches mutual fund NAV using the provided API and ISINs."""
    logger.info("Fetching mutual fund prices")
    cached_prices = {}
    remaining_isins = set()  # Use a set to store unique ISINs

    # Check Redis cache for each ISIN
    for isin in isins:
        cached_price = await cache_get(isin)
        if cached_price is not None:
            cached_prices[isin] = float(cached_price)  # Convert to plain float
        else:
            remaining_isins.add(isin)  # Add to set for uniqueness
    
    if not remaining_isins:
        return cached_prices

    # Convert the set back to a list for API calls
    unique_isins = list(remaining_isins)

    # Fetch data from the external API for remaining ISINs
    async with httpx.AsyncClient() as client:
        for isin in unique_isins:
            try:
                response = await client.get(f"{api_url}/{isin}", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    nav = data.get("nav")
                    if nav is not None:
                        cached_prices[isin] = float(nav)  # Convert to float before caching
                        await cache_set(isin, cached_prices[isin])  # Cache the float value
                    else:
                        logger.info(f"ISIN not found: {isin}")
                        cached_prices[isin] = "ISIN not found"
                else:
                    logger.error(f"Failed to fetch data for ISIN: {isin}, status code: {response.status_code}")
                    cached_prices[isin] = "ISIN not found"
            except httpx.RequestError as e:
                logger.error(f"Error fetching mutual fund data for ISIN {isin}: {e}")
                cached_prices[isin] = "ISIN not found"
    
    return cached_prices
