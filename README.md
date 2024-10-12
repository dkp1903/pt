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

chmod +x setup.sh

./setup.sh

```


### Status of items

[X]US stock market data flow

[X]Two level caching

[X]Rate limiting

[X]Cache error handling

[]Indian MFs data flow

[]Refactored content to handle malformed payloads