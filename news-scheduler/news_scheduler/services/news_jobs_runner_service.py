import logging
from typing import Annotated

from fastapi import Depends
from news_scheduler.connectors.kafka_producer_connector import (
    KafkaProducerConnector,
    get_kafka_producer_connector,
)
from news_scheduler.models.news_job import NewsJob

logger = logging.getLogger(__name__)


class NewsJobRunnerService:
    def __init__(self, producer_connector: KafkaProducerConnector):
        self._producer_connector = producer_connector

    def run_job(self, job: NewsJob):
        """Run the job

        Args:
            job (NewsJob): Job to run
        """
        logger.debug(f"Ran job: {job.id} with url: {job.url}")
        self._producer_connector.send(key=f"Job: {job.id}", value=job.model_dump_json())


async def get_news_job_runner_service(
    kafka_producer: Annotated[
        KafkaProducerConnector, Depends(get_kafka_producer_connector)
    ],
):
    yield NewsJobRunnerService(kafka_producer)
