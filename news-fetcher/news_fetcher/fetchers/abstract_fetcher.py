from abc import ABC, abstractmethod


class AbstractFetcher(ABC):

    @abstractmethod
    def fetch(self, url: str) -> str:
        raise NotImplementedError
