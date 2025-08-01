from abc import ABC, abstractmethod
from typing import Any


class AbstractParser(ABC):

    @abstractmethod
    def parse(self, data: str) -> Any:
        raise NotImplementedError
