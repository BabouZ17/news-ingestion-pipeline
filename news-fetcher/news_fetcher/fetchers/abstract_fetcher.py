from abc import ABC, abstractmethod


class AbstractFetcher(ABC):

    @abstractmethod
    def fetch(self) -> str:
        raise NotImplementedError
