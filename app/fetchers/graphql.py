# app/graphql_endpoint.py

from ariadne import make_executable_schema, ObjectType, graphql_sync
from ariadne.asgi import GraphQL
from fastapi import FastAPI
from app.fetchers.schema import type_defs, query

# Create schema and attach resolvers
schema = make_executable_schema(type_defs, query)

# Create the GraphQLApp to be injected in the main app
graphql_app = GraphQL(schema, debug=True)

def add_graphql_route(app: FastAPI):
    """
    Function to add the GraphQL route to the FastAPI app.
    This is injected into the app in the main.py file.
    """
    app.add_route("/graphql", graphql_app)
