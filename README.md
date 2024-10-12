### env variables

```
INDIA_MUTUAL_FUND_API_URL=https://api.example.com/mutual-fund
REDIS_HOST=localhost
REDIS_PORT=6379
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

[X]US stock market data flow

[X]Two level caching

[X]Rate limiting

[X]Cache error handling

[X]Indian MFs data flow

[X]Refactored content to handle malformed payloads

[X]Handle single and multi ticker cases

[X]Multiple entries of same ticker doesn't mean multiple entries during API call

[]GraphQL layer to optimize ISIN content