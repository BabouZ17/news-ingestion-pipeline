import logging
import time
from threading import Event

from news_fetcher.connectors.kafka_consumer_connector import (
    KafkaConsumerConnector,
    Message,
)
from news_fetcher.connectors.news_api_connector import NewsAPIConnector
from news_fetcher.fetchers.abstract_fetcher import AbstractFetcher
from news_fetcher.models.news import News, NewsList
from news_fetcher.models.news_job import NewsJob

logger = logging.getLogger(__name__)


class NewsService:
    def __init__(
        self,
        news_fetcher: AbstractFetcher,
        news_api_connector: NewsAPIConnector,
        kafka_consumer_connector: KafkaConsumerConnector,
    ):
        self.news_fetcher = news_fetcher
        self.news_api_connector = news_api_connector
        self.kafka_consumer_connector = kafka_consumer_connector
        self.event = Event()

    def is_running(self) -> bool:
        return not self.event.is_set()

    def run(self):
        logger.info("Starting to run...")
        while self.is_running():
            messages: list[Message] | None = self.kafka_consumer_connector.consume()
            if messages is not None:
                for msg in messages:
                    # Parse message
                    job: NewsJob = NewsJob.model_validate_json(msg.value)
                    logger.info(f"Received job: {job.model_dump()}")

                    # Fetch news
                    content: str = self.news_fetcher.fetch(job.url)
                    logger.debug(f"Retrieved news info: {content[:100]}")

                    news: NewsList = NewsList.model_validate_json(content)

                    # Invoke news ingestion
                    self.news_api_connector.ingest_news(news)
            else:
                time.sleep(1)

    def stop(self):
        self.event.set()
