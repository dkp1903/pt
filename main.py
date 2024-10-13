from fastapi import FastAPI
from app.api import router
from app.fetchers.graphql import add_graphql_route

app = FastAPI()

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Financial Data Fetching Service is running"}

add_graphql_route(app)