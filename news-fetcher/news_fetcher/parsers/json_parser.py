import logging
from json import JSONDecodeError, loads
from typing import Any

from news_fetcher.exceptions import NewsFetcherParsingException
from news_fetcher.parsers.abstract_parser import AbstractParser

logger = logging.getLogger(__name__)


class JSONParser(AbstractParser):

    def parse(self, data: str) -> Any:
        """Parse data into the expected Python object

        Args:
            data (str): The json encoded string
        Returns:
            Any
        Raises:
            NewsFetcherParsingException
        """
        try:
            return loads(data)
        except (TypeError, JSONDecodeError) as e:
            msg = f"Failed to parse data into JSON, reason: {e}"
            logger.error(msg)
            raise NewsFetcherParsingException(msg)
