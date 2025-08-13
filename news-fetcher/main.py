import logging
import os
import signal
from threading import Thread

from news_fetcher.config.config import Config
from news_fetcher.connectors.http_connector import HTTPConnector
from news_fetcher.connectors.kafka_consumer_connector import KafkaConsumerConnector
from news_fetcher.connectors.news_api_connector import NewsAPIConnector
from news_fetcher.fetchers.http_fecther import HTTPFetcher
from news_fetcher.services.news_service import NewsService

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("kafka").setLevel(logging.INFO)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    config = Config()

    kafka_consumer_connector = KafkaConsumerConnector(
        topic=config.topic, bootstrap_servers=[config.bootstrap_servers]
    )

    news_api_connector = NewsAPIConnector(
        url=config.news_api_url, connector=HTTPConnector()
    )

    news_service = NewsService(
        news_fetcher=HTTPFetcher(connector=HTTPConnector()),
        news_api_connector=news_api_connector,
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
