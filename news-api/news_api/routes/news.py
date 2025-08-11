import json
import logging
from pathlib import Path
from typing import Annotated

from fastapi import Depends
from news_api.connectors.opensearch import OpensearchConnector, get_connector
from news_api.models.news import BaseNews, News, NewsCount
from news_api.models.response import Response
from news_api.repositories.news import NewsRepository, get_repository
from news_api.services.news_ingestion_service import NewsIngestionService

logger = logging.getLogger(__name__)

NEWS_INDEX_NAME = "news"
NEWS_INDEX_BODY_PATH = Path(__file__).parent.parent.parent / "resources/index.json"


async def search_news(
    repository: Annotated[NewsRepository, Depends(get_repository)],
    term: str = "Cybersecurity",
) -> list[BaseNews]:
    news: list[News] = await repository.keyword_search(term=term)
    return [BaseNews.model_validate(n) for n in news]


async def count_news(
    repository: Annotated[NewsRepository, Depends(get_repository)],
) -> NewsCount:
    count: int = await repository.count()
    return NewsCount(count=count)


async def delete_news(
    repository: Annotated[NewsRepository, Depends(get_repository)],
) -> Response:
    await repository.delete_news()
    return Response(message="All news were deleted")


async def add_news(
    news: list[News],
    repository: Annotated[NewsRepository, Depends(get_repository)],
    ingestion_service: Annotated[NewsIngestionService, Depends()],
) -> Response:
    count = len(news)
    for news_candidate in news:
        should_ingest, embeddings = ingestion_service.should_ingest(news_candidate)
        if should_ingest:
            news_candidate.embeddings = embeddings
            await repository.add_news(news_candidate)
        else:
            count -= 1
            logger.info(f"News with id: {news_candidate.id} failed to be ingested")
    return Response(message=f"{count} were successfully saved")


async def get_news(
    repository: Annotated[NewsRepository, Depends(get_repository)],
) -> list[BaseNews]:

    news: list[News] = await repository.get_all_news()
    return [BaseNews.model_validate(n) for n in news]


async def create_index(
    opensearch_connector: Annotated[OpensearchConnector, Depends(get_connector)],
) -> Response:
    body = None
    with open(NEWS_INDEX_BODY_PATH) as f:
        body = json.load(f)

    await opensearch_connector.create_index(index=NEWS_INDEX_NAME, body=body)
    return Response(message=f"Index {NEWS_INDEX_NAME} created!")
