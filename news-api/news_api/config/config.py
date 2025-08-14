from pydantic_settings import BaseSettings


class Config(BaseSettings):
    opensearch_user: str
    opensearch_password: str
    opensearch_host: str

    openai_api_key: str


def get_config():
    return Config()
