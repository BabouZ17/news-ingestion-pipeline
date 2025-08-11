from typing import Annotated, Any

from fastapi import Depends
from news_api.connectors.opensearch_connector import OpensearchConnector, get_connector
from news_api.models.news import News


class NewsRepository:
    def __init__(self, connector: OpensearchConnector, index: str = "news"):
        self.connector = connector
        self.index = index

    @staticmethod
    def map_to_news(results: list[dict[str, Any]]) -> list[News]:
        return [News.model_validate(n) for n in results]

    async def knn_search(self, vector: list[float], k: int = 20) -> list[News]:
        body = {
            "query": {
                "nested": {
                    "path": "embeddings",
                    "query": {
                        "knn": {"embeddings.embedding": {"vector": vector, "k": k}}
                    },
                }
            }
        }
        items = await self.connector.search(index=self.index, body=body)
        return self.map_to_news(items)

    async def hybrid_search(
        self, vector: list[float], k: int = 20, boost: int = 100
    ) -> list[News]:
        body = {
            "query": {
                "bool": {
                    "must": {
                        "nested": {
                            "path": "embeddings",
                            "query": {
                                "knn": {
                                    "embeddings.embedding": {"vector": vector, "k": k}
                                }
                            },
                        }
                    },
                    "should": [
                        {"range": {"published_at": {"boost": boost, "gte": "now-7d/d"}}}
                    ],
                }
            }
        }
        items = await self.connector.search(index=self.index, body=body)
        return self.map_to_news(items)

    async def keyword_search(self, term: str, size: int = 20) -> list[News]:
        body = {"query": {"match": {"body": term}}, "size": size}
        items = await self.connector.search(index=self.index, body=body)
        return self.map_to_news(items)

    async def count(self) -> int:
        return await self.connector.count(index=self.index)

    async def delete_news(self):
        return await self.connector.delete_documents(index=self.index)

    async def add_news(self, news: News):
        await self.connector.index_document(
            index=self.index, document=news.model_dump(), id=news.id
        )

    async def get_all_news(self) -> list[News]:
        items: list[dict[str, Any]] = await self.connector.list_documents(
            index=self.index
        )
        return self.map_to_news(items)


async def get_news_repository(
    connector: Annotated[OpensearchConnector, Depends(get_connector)],
):
    repository = NewsRepository(connector=connector)
    yield repository
