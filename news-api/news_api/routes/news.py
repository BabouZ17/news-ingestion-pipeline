import logging
from typing import Annotated

from fastapi import Depends, Query
from news_api.models.news import BaseNews, News, NewsCount
from news_api.models.response import Response
from news_api.repositories.news import NewsRepository, get_news_repository
from news_api.services.news_embeddings_service import (
    NewsEmbeddingsService,
    get_news_embeddings_service,
)
from news_api.services.news_ingestion_service import (
    NewsIngestionService,
    get_news_ingestion_service,
)

logger = logging.getLogger(__name__)


async def hybrid_search_news(
    repository: Annotated[NewsRepository, Depends(get_news_repository)],
    news_embeddings_service: Annotated[
        NewsEmbeddingsService, Depends(get_news_embeddings_service)
    ],
    query: Annotated[str, Query(max_length=50)] = "cybersecurity",
) -> list[BaseNews]:
    query_vector: list[float] = news_embeddings_service.create_embeddings([query])[0]
    news: list[News] = await repository.hybrid_search(vector=query_vector)
    return [BaseNews.model_validate(n) for n in news]


async def knn_search_news(
    repository: Annotated[NewsRepository, Depends(get_news_repository)],
    news_embeddings_service: Annotated[
        NewsEmbeddingsService, Depends(get_news_embeddings_service)
    ],
    query: Annotated[str, Query(max_length=50)] = "cybersecurity",
) -> list[BaseNews]:
    query_vector: list[float] = news_embeddings_service.create_embeddings([query])[0]
    news: list[News] = await repository.knn_search(vector=query_vector)
    return [BaseNews.model_validate(n) for n in news]


async def keyword_search_news(
    repository: Annotated[NewsRepository, Depends(get_news_repository)],
    term: Annotated[str, Query(max_length=50)] = "cybersecurity",
) -> list[BaseNews]:
    news: list[News] = await repository.keyword_search(term=term)
    return [BaseNews.model_validate(n) for n in news]


async def count_news(
    repository: Annotated[NewsRepository, Depends(get_news_repository)],
) -> NewsCount:
    count: int = await repository.count()
    return NewsCount(count=count)


async def delete_news(
    repository: Annotated[NewsRepository, Depends(get_news_repository)],
) -> Response:
    await repository.delete_news()
    return Response(message="All news were deleted")


async def add_news(
    news_candidates: list[BaseNews],
    ingestion_service: Annotated[
        NewsIngestionService, Depends(get_news_ingestion_service)
    ],
) -> Response:
    count = len(news_candidates)
    news: list[News] = [News.model_validate(n.model_dump()) for n in news_candidates]
    for news_candidate in news:
        should_ingest, embeddings = ingestion_service.should_ingest(news_candidate)
        if should_ingest:
            news_candidate.embeddings = embeddings
            await ingestion_service.ingest_news(news_candidate)
        else:
            count -= 1
            logger.info(f"News with id: {news_candidate.id} failed to be ingested")
    return Response(message=f"{count} were successfully saved")


async def get_news(
    repository: Annotated[NewsRepository, Depends(get_news_repository)],
) -> list[BaseNews]:

    news: list[News] = await repository.get_all_news()
    return [BaseNews.model_validate(n) for n in news]
