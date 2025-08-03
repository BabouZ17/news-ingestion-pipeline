import logging
from typing import Dict, List
from uuid import uuid4

from kafka import KafkaConsumer as Consumer

logger = logging.getLogger(__name__)


class KafkaConsumer:
    def __init__(
        self,
        bootstrap_servers: List[str],
        topic: str,
        group_id: str = "default",
        api_version: str = "2.2.15",
        timeout_ms: int = 100,
    ):
        self.topic = topic
        self.group_id = group_id
        self.consumer = Consumer(
            client_id=str(uuid4()),
            group_id=self.group_id,
            bootstrap_servers=bootstrap_servers,
            api_version=api_version,
        )
        self.subscribe()
        self.timeout_ms = timeout_ms

    def subscribe(self):
        logger.info("Subscribing...")
        self.consumer.subscribe(topics=[self.topic])

    def unsubscribe(self):
        logger.info("Unsubscribing...")
        self.consumer.unsubscribe()

    def read(self):
        messages: Dict = self.consumer.poll(timeout_ms=self.timeout_ms)
        print(messages)
        if messages:
            for msg in messages:
                logger.info(msg)
        else:
            logger.info("No new messages")
