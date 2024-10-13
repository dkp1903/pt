from ariadne import QueryType
import httpx

# Define the type definitions (schema)
type_defs = """
    type Query {
        mutualFundPrices(isins: [String!]): [MutualFundPrice!]!
    }

    type MutualFundPrice {
        identifier: String!
        nav: Float
    }
"""

# Create a QueryType instance to define resolver functions
query = QueryType()

# Resolver function for mutual fund prices
@query.field("mutualFundPrices")
async def resolve_mutual_fund_prices(_, info, isins):
    results = []
    api_url = "https://mf.captnemo.in/nav"  # Your existing mutual fund API endpoint

    async with httpx.AsyncClient() as client:
        for isin in isins:
            try:
                response = await client.get(f"{api_url}/{isin}")
                if response.status_code == 200:
                    data = response.json()
                    current_nav = data.get("nav")  # Only fetch current NAV
                    if current_nav is not None:
                        results.append({"identifier": isin, "nav": current_nav})
                    else:
                        results.append({"identifier": isin, "nav": None})
                else:
                    results.append({"identifier": isin, "nav": None})
            except httpx.RequestError as e:
                results.append({"identifier": isin, "nav": None})
                print(f"An error occurred while fetching ISIN {isin}: {e}")

    return results
