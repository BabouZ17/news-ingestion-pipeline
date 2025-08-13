import logging
from typing import Any
from uuid import uuid4

from kafka import KafkaConsumer
from kafka.errors import KafkaError
from news_fetcher.exceptions import NewsFetcherConsumerException
from pydantic import BaseModel, field_validator

logger = logging.getLogger(__name__)


class Message(BaseModel):
    topic: str
    partition: int
    offset: int
    key: str
    value: str

    @field_validator("key", "value", mode="before")
    @classmethod
    def to_str(cls, value: Any):
        if not isinstance(value, bytes):
            raise ValueError(f"{value} should be of type 'bytes'")
        else:
            return value.decode("utf-8")


class KafkaConsumerConnector:
    def __init__(
        self,
        bootstrap_servers: list[str],
        topic: str,
        group_id: str = "default",
        api_version: str = "2.2.15",
    ):
        self.topic = topic
        self.group_id = group_id
        self.consumer = KafkaConsumer(
            client_id=str(uuid4()),
            group_id=self.group_id,
            bootstrap_servers=bootstrap_servers,
            api_version=api_version,
        )
        self.subscribe()

    def subscribe(self):
        logger.debug("Subscribing...")
        self.consumer.subscribe(topics=[self.topic])

    def unsubscribe(self):
        logger.debug("Unsubscribing...")
        self.consumer.unsubscribe()

    def consume(self) -> list[Message] | None:
        """Poll for new messages.

        Returns:
            list[Message] | None: Polled messages if any, None otherwise
        Raises:
            NewsFetcherConsumerException: When polling failed.
        """
        try:
            records: dict[str, Any] = self.consumer.poll()
            logger.debug(f"Received records: {records}")
            if records:
                for _, consumer_records in records.items():
                    return [
                        Message(
                            topic=record.topic,
                            partition=record.partition,
                            offset=record.offset,
                            key=record.key,
                            value=record.value,
                        )
                        for record in consumer_records
                    ]
            else:
                return None
        except KafkaError as e:
            msg = f"An error occured during message consumption: {e}"
            logger.error(msg)
            raise NewsFetcherConsumerException(msg)
