import logging

from news_fetcher.connectors.http_connector import HTTPConnector
from news_fetcher.exceptions import NewsFetcherIngestionExcepion
from news_fetcher.models.news import NewsList
from requests.exceptions import HTTPError

logger = logging.getLogger(__name__)


class NewsAPIConnector:
    def __init__(self, url: str, connector: HTTPConnector):
        self.url = url
        self._connector = connector

    def ingest_news(self, news: NewsList):
        """Invoke news-api endpoint to ingest news

        Args:
            news (NewsList): News to ingest
        """
        try:
            response = self._connector.post(
                url=self.url,
                data=news.model_dump_json(),
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
        except HTTPError as e:
            msg = f"Could not ingest news, reason: {e}"
            logger.error(msg)
            raise NewsFetcherIngestionExcepion(msg)
