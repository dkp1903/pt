### env variables

```
INDIA_MUTUAL_FUND_API_URL=https://mf.captnemo.in/nav/
REDIS_HOST=localhost
REDIS_PORT=6379
GRAPHQL_URL=http://localhost:8000/graphql # Change localhost to wherever the app is running
```

### Steps to run

```
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

docker run -d -p 6379:6379 --name redis redis

uvicorn main:app --reload


```


### Status of items

- [x] US stock market data flow

- [x] Two level caching

- [x] Rate limiting

- [x] Cache error handling

- [x] Indian MFs data flow

- [x] Refactored content to handle malformed payloads

- [x] Handle single and multi ticker cases

- [x] Multiple entries of same ticker doesn't mean multiple entries during API call

- [ ] GraphQL layer to optimize ISIN content
