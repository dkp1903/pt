from app.fetchers.stock_fetcher import fetch_stock_prices
from app.fetchers.mutual_fund_fetcher import fetch_mutual_fund_prices
from app.config import settings
import logging

logger = logging.getLogger(__name__)

async def get_prices(tickers_info):
    """Fetches prices for both US stocks and Indian mutual funds."""
    logger.info("Processing price requests")

    # Separate tickers and ISINs
    tickers = [info.ticker for info in tickers_info if not info.ticker.startswith("INF")]
    isins = [info.ticker for info in tickers_info if info.ticker.startswith("INF")]

    results = {}

    # Fetch stock prices
    if tickers:
        prices = await fetch_stock_prices(tickers)
        results.update(prices)

    # Fetch mutual fund prices
    if isins:
        prices = await fetch_mutual_fund_prices(isins, settings.INDIA_MUTUAL_FUND_API_URL)
        results.update(prices)

    # Return the results for both US stocks and Indian mutual funds
    return [{"identifier": ticker, "price": results[ticker]} for ticker in results]
