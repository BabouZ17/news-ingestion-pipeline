import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    topic: str
    bootstrap_servers: str


def get_config():
    return Config()
