import json
from pathlib import Path
from typing import Annotated

from fastapi import Depends
from news_api.connectors.opensearch import OpensearchConnector, get_connector
from news_api.models.news import News, NewsCount
from news_api.repositories.news import NewsRepository, get_repository

NEWS_INDEX_NAME = "news"
NEWS_INDEX_BODY_PATH = (
    Path(__file__).parent.parent.parent / "resources/keyword_index.json"
)

VECTOR_NEWS_INDEX_NAME = "news-vector"
VECTOR_NEWS_INDEX_BODY_PATH = (
    Path(__file__).parent.parent.parent / "resources/vector_store_index.json"
)


async def count_news(
    repository: Annotated[NewsRepository, Depends(get_repository)],
) -> NewsCount:
    count: int = await repository.count()
    return NewsCount(count=count)


async def add_news(
    news: list[News], repository: Annotated[NewsRepository, Depends(get_repository)]
):
    for n in news:
        await repository.add_news(n)


async def get_news(
    repository: Annotated[NewsRepository, Depends(get_repository)],
) -> list[News]:
    return await repository.get_all_news()


async def create_index(
    opensearch_connector: Annotated[OpensearchConnector, Depends(get_connector)],
):
    body = None
    with open(NEWS_INDEX_BODY_PATH) as f:
        body = json.load(f)
        print(body)

    await opensearch_connector.create_index(index=NEWS_INDEX_NAME, body=body)


async def create_vector_index(
    opensearch_connector: Annotated[OpensearchConnector, Depends(get_connector)],
):
    body = None
    with open(VECTOR_NEWS_INDEX_BODY_PATH) as f:
        body = json.load(f)

    await opensearch_connector.create_index(index=VECTOR_NEWS_INDEX_NAME, body=body)
