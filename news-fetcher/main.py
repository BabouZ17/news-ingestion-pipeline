import os

from news_fetcher.connectors.kafka_consumer import KafkaConsumer

if __name__ == "__main__":
    TOPIC = os.getenv("TOPIC")
    assert TOPIC is not None, "Invalid topic given"

    BOOTSTRAP_SERVERS = os.environ["BOOTSTRAP_SERVERS"]
    assert BOOTSTRAP_SERVERS is not None, "Invalid boostrap servers given"

    kafka_consumer = KafkaConsumer(bootstrap_servers=[BOOTSTRAP_SERVERS], topic=TOPIC)
    while 1:
        kafka_consumer.read()
