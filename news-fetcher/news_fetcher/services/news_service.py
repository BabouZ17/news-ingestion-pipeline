import logging
import time
from threading import Event
from typing import Dict, List

from news_fetcher.connectors.kafka_consumer_connector import (
    KafkaConsumerConnector,
    Message,
)
from news_fetcher.fetchers.abstract_fetcher import AbstractFetcher
from pydantic import BaseModel

logger = logging.getLogger(__name__)


# Will need to address model redundancy
class NewsJob(BaseModel):
    id: str
    name: str
    url: str


class NewsService:
    def __init__(
        self, fetcher: AbstractFetcher, kafka_consumer_connector: KafkaConsumerConnector
    ):
        self.fetcher = fetcher
        self.kafka_consumer_connector = kafka_consumer_connector
        self.event = Event()

    def is_running(self) -> bool:
        return not self.event.is_set()

    def run(self):
        logger.info("Starting to run...")
        while self.is_running():
            messages: List[Message] | None = self.kafka_consumer_connector.consume()
            if messages is not None:
                jobs: List[NewsJob] = []
                for msg in messages:
                    jobs.append(NewsJob.model_validate_json(msg.value))
                logger.debug(jobs)
            else:
                time.sleep(1)

    def stop(self):
        self.event.set()
