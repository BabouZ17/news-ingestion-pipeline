from typing import List

from kafka import KafkaProducer as Producer


class KafkaProducer:
    def __init__(
        self, topic: str, bootstrap_servers: List[str], api_version: str = "2.2.15"
    ):
        self.topic = topic
        self.producer = Producer(
            bootstrap_servers=bootstrap_servers, api_version=api_version
        )

    def send(self, key: str, value: str) -> None:
        self.producer.send(
            self.topic, key=key.encode("utf-8"), value=value.encode("utf-8")
        )
