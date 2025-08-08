import logging
import os
import signal
from threading import Thread

from news_fetcher.connectors.http_connector import HTTPConnector
from news_fetcher.connectors.kafka_consumer_connector import KafkaConsumerConnector
from news_fetcher.fetchers.http_fecther import HTTPFetcher
from news_fetcher.services.news_service import NewsService

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("kafka").setLevel(logging.INFO)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    TOPIC = os.getenv("TOPIC")
    assert TOPIC is not None, "Invalid topic given"

    BOOTSTRAP_SERVERS = os.environ["BOOTSTRAP_SERVERS"]
    assert BOOTSTRAP_SERVERS is not None, "Invalid boostrap servers given"

    kafka_consumer_connector = KafkaConsumerConnector(
        bootstrap_servers=[BOOTSTRAP_SERVERS], topic=TOPIC
    )

    news_service = NewsService(
        fetcher=HTTPFetcher(connector=HTTPConnector()),
        kafka_consumer_connector=kafka_consumer_connector,
    )

    # Catch Interupts and Kill signals
    def signal_handler(sig, frame):
        logger.debug("Killing thread")
        news_service.stop()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    thread = Thread(target=news_service.run)
    thread.start()
