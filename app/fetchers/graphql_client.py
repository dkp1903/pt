import httpx
from fastapi import Request
import logging
from app.config import settings

logger = logging.getLogger(__name__)

async def fetch_mutual_fund_data_from_graphql(isins: list, request: Request):
    graphql_url=settings.GRAPHQL_URL
    query = """
    query GetMutualFundPrices($isins: [String!]) {
        mutualFundPrices(isins: $isins) {
            identifier
            nav
        }
    }
    """
    
    variables = {"isins": isins}
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(graphql_url, json={"query": query, "variables": variables})
            if response.status_code == 200:
                data = response.json().get('data', {}).get('mutualFundPrices', [])
                return data
            else:
                logger.error(f"Error calling GraphQL: {response.status_code} {response.text}")
                return {"error": "Error calling GraphQL"}
    except httpx.RequestError as exc:
        logger.error(f"An error occurred while requesting GraphQL: {exc}")
        return {"error": "Request failed"}
