from pydantic_settings import BaseSettings


class Config(BaseSettings):
    topic: str
    bootstrap_servers: str

    news_api_url: str
