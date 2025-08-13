import asyncio
import logging
from datetime import datetime
from typing import Annotated

from fastapi import Depends
from langchain_community.utils.math import cosine_similarity
from news_api.config.config import Config
from news_api.connectors.opensearch_connector import OpensearchConnector
from news_api.models.news import News, NewsEmbedding
from news_api.repositories.news import NewsRepository, get_news_repository
from news_api.services.news_embeddings_service import (
    NewsEmbeddingsService,
    get_news_embeddings_service,
)

logger = logging.getLogger(__name__)

# Corpus of words to compare relevancy upon
CORPUS: list[str] = ["cybersecurity threats", "outages", "software bugs"]


class NewsIngestionService:
    def __init__(
        self,
        embeddings_service: NewsEmbeddingsService,
        repository: NewsRepository,
        ingestion_threshold: float = 0.5,
    ):
        self.embeddings_service = embeddings_service
        self.repository = repository
        self.ingestion_threshold = ingestion_threshold
        self._embedded_corpus = dict()

    async def news_exists(self, news: News) -> bool:
        """Check either a given news already exists in database

        Args:
            news (News): The news to look upon
        Returns:
            bool
        """
        if await self.repository.get_news(id=news.id) is not None:
            return True
        else:
            return False

    def embedded_corpus(self) -> dict[str, list[list[float]]]:
        """Compute the embeddings of the corpus

        Only done once to avoid extra cost.

        Returns:
            dict[str, list[list[float]]]
        """
        if len(self._embedded_corpus) == 0:
            for corpus_sentence in CORPUS:
                self._embedded_corpus[corpus_sentence] = (
                    self.embeddings_service.create_embeddings(
                        self.embeddings_service.split_text(corpus_sentence)
                    )
                )
        return self._embedded_corpus

    async def should_ingest(self, news: News) -> tuple[bool, News]:
        """Check if a news content is relevant enough to be ingested

        To do so, we:
            - check if the news is already indexed or not
            - tokenize the news content
            - compute the embeddings for each text chunk.
            - compute the cosine similarity for each split with each corpus chunk
            - sort the results and if the highest is superior or equal to threshold
            then, news is ingested

        Args:
            news (News): News to ingest

        Returns:
            tuple[boolean, News]
        """
        # Check if the news already indexed in db
        if await self.news_exists(news):
            logger.debug(f"News: {news.id} already exists, so dropped.")
            return False, news

        # Split the raw content
        text_chunks: list[str] = self.embeddings_service.split_text(
            text=news.body if news.body is not None else ""
        )
        logger.debug(f"text_chunks: {text_chunks[:100]}")

        # Compute embeddings for text chunks
        text_embeddings = self.embeddings_service.create_embeddings(text_chunks)

        corpus_similarities_scores: list[float] = list()
        for corpus_text, corpus_embedding in self.embedded_corpus().items():
            similarity = cosine_similarity(corpus_embedding, text_embeddings)[0][0]
            logger.debug(f"Similarity for corpus: {corpus_text} is: {similarity}")
            corpus_similarities_scores.append(similarity)

        # Map NewsEmbedding
        news_embeddings: list[NewsEmbedding] = list()
        for embedding, chunk in zip(text_embeddings, text_chunks):
            news_embeddings.append(NewsEmbedding(chunk=chunk, embedding=embedding))

        news.embeddings = news_embeddings

        corpus_similarities_scores.sort()
        return (corpus_similarities_scores[-1] >= self.ingestion_threshold, news)

    async def ingest_single_news(self, news: News):
        """Ingest a single news into database

        Args:
            news (News): News to ingest
        Returns:
            bool: Either news was ingested
        """
        should_ingest, updated_news = await self.should_ingest(news)
        if should_ingest:
            await self.repository.add_news(updated_news)
            return True
        return False

    async def ingest_news(self, news: list[News]) -> int:
        """Ingest news into database

        Args:
            news (list[News]): List of news to ingest
        Returns:
            int: count of news ingested
        """
        tasks: list[asyncio.Task[object]] = list()
        async with asyncio.TaskGroup() as tg:
            for n in news:
                task = tg.create_task(self.ingest_single_news(n))
                tasks.append(task)
        return sum([task.result() for task in tasks])  # type: ignore


async def get_news_ingestion_service(
    embeddings_service: Annotated[
        NewsEmbeddingsService, Depends(get_news_embeddings_service)
    ],
    repository: Annotated[NewsRepository, Depends(get_news_repository)],
):
    service = NewsIngestionService(
        embeddings_service=embeddings_service, repository=repository
    )
    yield service


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    exemples = [
        News(
            id="1",
            source="dev",
            title="Cybersecurity",
            body="Major cybersecurity threats have occured recently. Amazon has received no less than 5 millions daily attacks in 2025",
            published_at=datetime(year=2025, month=1, day=1),
        ),
        News(
            id="2",
            source="dev",
            title="Software updates",
            body="Software updates are a critical aspect of cybersecurity, with outdated software providing an easy entry point for hackers. To protect against software-related threats, it's essential to implement robust software update practices, including regular updates and patching. This can help prevent cyber attacks and protect sensitive data.",
            published_at=datetime(year=2025, month=1, day=1),
        ),
        News(
            id="3",
            source="dev",
            title="Useless",
            body="The sky is blue",
            published_at=datetime(year=2025, month=1, day=1),
        ),
    ]

    config = Config()
    ingestion_service = NewsIngestionService(
        embeddings_service=NewsEmbeddingsService(),
        repository=NewsRepository(
            connector=OpensearchConnector(
                user=config.opensearch_user,
                password=config.opensearch_password,
                host=config.opensearch_host,
            )
        ),
    )
    for ex in exemples:
        result, _ = asyncio.run(ingestion_service.should_ingest(ex))
        print(result)
