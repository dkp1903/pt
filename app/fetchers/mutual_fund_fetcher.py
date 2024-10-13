import logging
from app.caching import cache_get, cache_set
from app.fetchers.graphql_client import fetch_mutual_fund_data_from_graphql  # Import the GraphQL client
from fastapi import Request  # To pass the Request object for base URL

logger = logging.getLogger(__name__)

async def fetch_mutual_fund_prices(isins: list, request: Request):
    """
    Fetches mutual fund NAV using the internal GraphQL logic for ISINs.
    Calls the GraphQL endpoint internally and caches the results.
    """
    logger.info("Fetching mutual fund prices using GraphQL")
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

    # Convert the set back to a list for GraphQL calls
    unique_isins = list(remaining_isins)

    try:
        # Fetch data via the internal GraphQL client
        data = await fetch_mutual_fund_data_from_graphql(unique_isins, request)

        # Process the GraphQL response
        for item in data:
            isin = item.get("identifier")
            nav = item.get("nav")
            if nav is not None:
                cached_prices[isin] = float(nav)  # Convert to float before caching
                await cache_set(isin, cached_prices[isin])  # Cache the float value
            else:
                logger.info(f"ISIN not found: {isin}")
                cached_prices[isin] = "ISIN not found"

        return cached_prices

    except Exception as e:
        logger.error(f"Error fetching mutual fund data for ISINs: {remaining_isins}, error: {e}")
        return {isin: "Error fetching data" for isin in remaining_isins}
