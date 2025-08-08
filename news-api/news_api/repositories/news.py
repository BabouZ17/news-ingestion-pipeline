from typing import Annotated, Any

from fastapi import Depends
from news_api.connectors.opensearch import OpensearchConnector, get_connector
from news_api.models.news import News


class NewsVectorRepository:
    def __init__(self, connector: OpensearchConnector, index: str = "news-vc"):
        self.connector = connector
        self.index = index


class NewsRepository:
    def __init__(self, connector: OpensearchConnector, index: str = "news"):
        self.connector = connector
        self.index = index

    async def count(self) -> int:
        return await self.connector.count(index=self.index)

    async def add_news(self, news: News):
        await self.connector.index_document(
            index=self.index, document=news.model_dump(), id=news.id
        )

    async def get_all_news(self) -> list[News]:
        news: list[News] = list()
        items: list[dict[str, Any]] = await self.connector.list_documents(
            index=self.index
        )
        for item in items:
            news.append(News.model_validate(**item))
        return news


async def get_repository(
    connector: Annotated[OpensearchConnector, Depends(get_connector)],
):
    repository = NewsRepository(connector=connector)
    yield repository


async def get_vc_repository(
    connector: Annotated[OpensearchConnector, Depends(get_connector)],
):
    repository = NewsVectorRepository(connector=connector)
    yield repository
