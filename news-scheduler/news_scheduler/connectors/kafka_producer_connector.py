from typing import Annotated

from fastapi import Depends
from kafka import KafkaProducer as Producer
from news_scheduler.config.config import Config, get_config


class KafkaProducerConnector:
    def __init__(
        self, topic: str, bootstrap_servers: list[str], api_version: str = "2.2.15"
    ):
        self.topic = topic
        self._producer = Producer(
            bootstrap_servers=bootstrap_servers, api_version=api_version
        )

    def send(self, key: str, value: str) -> None:
        self._producer.send(
            self.topic, key=key.encode("utf-8"), value=value.encode("utf-8")
        )

    def flush(self):
        self._producer.flush()


async def get_kafka_producer_connector(
    config: Annotated[Config, Depends(get_config)],
):
    producer = KafkaProducerConnector(
        topic=config.topic, bootstrap_servers=[config.bootstrap_servers]
    )
    yield producer
    producer.flush()
