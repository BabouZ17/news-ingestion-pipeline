import logging

from news_fetcher.connectors.http_connector import HTTPConnector
from news_fetcher.exceptions import NewsFetcherFetchingException
from news_fetcher.fetchers.abstract_fetcher import AbstractFetcher
from requests import Response
from requests.exceptions import HTTPError

logger = logging.getLogger(__name__)


class HTTPFetcher(AbstractFetcher):
    def __init__(self, url: str, connector: HTTPConnector):
        self.url = url
        self._connector = connector

    def fetch(self) -> str:
        """Fetch news given an url

        Returns:
            str

        Raises:
            NewsFetchingException: When an error occured while retrieving news
        """
        try:
            response: Response = self._connector.get(url=self.url)
            response.raise_for_status()
        except HTTPError as e:
            msg = f"Could not fetch news for {self.url}, reason: {e}"
            logger.error(msg)
            raise NewsFetcherFetchingException(msg)
        return response.text
