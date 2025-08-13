import logging
from typing import Annotated

from fastapi import Depends, Query, Response, status
from news_api.models.custom_response import CustomResponse
from news_api.models.news import BaseNews, News, NewsCount
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


async def semantic_search_news(
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
    query: Annotated[str, Query(max_length=50)] = "cybersecurity",
) -> list[BaseNews]:
    news: list[News] = await repository.keyword_search(query=query)
    return [BaseNews.model_validate(n) for n in news]


async def count_news(
    repository: Annotated[NewsRepository, Depends(get_news_repository)],
) -> NewsCount:
    count: int = await repository.count()
    return NewsCount(count=count)


async def delete_news(
    repository: Annotated[NewsRepository, Depends(get_news_repository)],
) -> CustomResponse:
    await repository.delete_news()
    return CustomResponse(message="All news were deleted")


async def add_news(
    news_candidates: list[BaseNews],
    ingestion_service: Annotated[
        NewsIngestionService, Depends(get_news_ingestion_service)
    ],
) -> CustomResponse:
    news: list[News] = [News.model_validate(n.model_dump()) for n in news_candidates]
    count = await ingestion_service.ingest_news(news)
    return CustomResponse(message=f"{count} were successfully saved")


async def get_news(
    response: Response,
    repository: Annotated[NewsRepository, Depends(get_news_repository)],
    id: str | None = None,
) -> list[BaseNews] | BaseNews | CustomResponse:
    if id is None:
        all_news: list[News] = await repository.get_all_news()
        return [BaseNews.model_validate(new) for new in all_news]
    else:
        news: News | None = await repository.get_news(id)
        if news is not None:
            return BaseNews.model_validate(news)

        response.status_code = status.HTTP_404_NOT_FOUND
        return CustomResponse(message=f"News: {id} does not exist!")
