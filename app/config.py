from pydantic import BaseSettings

class Settings(BaseSettings):
    INDIA_MUTUAL_FUND_API_URL: str
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    class Config:
        env_file = ".env"

# Instantiate settings
settings = Settings()
