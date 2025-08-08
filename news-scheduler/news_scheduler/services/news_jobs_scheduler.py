import logging
from typing import List
from uuid import uuid4

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import STATE_PAUSED, STATE_STOPPED
from apscheduler.triggers.cron import CronTrigger
from news_scheduler.connectors.kafka_producer_connector import KafkaProducerConnector
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class NewsJob(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    url: str


class NewsJobScheduler:
    def __init__(self, jobs: List[NewsJob], producer_connector: KafkaProducerConnector):
        self.jobs = jobs
        self._producer_connector = producer_connector
        self._scheduler = BackgroundScheduler()

        for job in self.jobs:
            self.add_job(job)

    def _default_func(self, job: NewsJob):
        self._producer_connector.send(key=f"Job: {job.id}", value=job.model_dump_json())

    def add_job(self, job: NewsJob):
        logger.info(f"Adding news job: {job.id}")
        self._scheduler.add_job(
            func=self._default_func,
            kwargs={"job": job},
            trigger=CronTrigger(minute="*", second=0),
        )

    def start(self):
        if (
            self._scheduler.state == STATE_STOPPED
            or self._scheduler.state == STATE_PAUSED
        ):
            self._scheduler.start()

    def shutdown(self):
        if self._scheduler.state != STATE_STOPPED:
            self._scheduler.shutdown()
