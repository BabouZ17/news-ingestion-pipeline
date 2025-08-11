import logging
import os
from typing import Any

from opensearchpy import AsyncOpenSearch

logger = logging.getLogger(__name__)


class OpensearchConnector:
    def __init__(
        self,
        user: str | None = None,
        password: str | None = None,
        host: str = "opensearch",
        port: int = 9200,
    ):
        if user is None:
            user = os.getenv("OPENSEARCH_USER")
            assert user is not None, "'user' has to be set"
        if password is None:
            password = os.getenv("OPENSEARCH_PASSWORD")
            assert password is not None, "'password' has to be set"

        self._client = AsyncOpenSearch(
            hosts=[{"host": host, "port": port}],
            http_auth=(user, password),
            use_ssl=True,
            verify_certs=False,
            ssh_show_warn=False,
        )

    @staticmethod
    def map_result(result: dict[str, Any]) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = list()
        for item in result["hits"]["hits"]:
            items.append(item["_source"])
        return items

    async def search(self, index: str, body: dict[str, Any]) -> list[dict[str, Any]]:
        result = await self._client.search(index=index, body=body)
        return self.map_result(result)

    async def create_index(self, index: str, body: dict[str, Any]):
        if not await self._client.indices.exists(index=index):
            await self._client.indices.create(index=index, body=body)
        else:
            logger.info(f"Index {index} already exists!")

    async def index_document(self, index: str, document: Any, id: str):
        # If needed, bulk api is available...
        await self._client.index(index=index, body=document, id=id)

    async def list_documents(self, index: str) -> list[dict[str, Any]]:
        result = await self._client.search(
            index=index, body={"query": {"match_all": {}}}
        )
        return self.map_result(result)

    async def count(self, index: str) -> int:
        result: dict[str, Any] = await self._client.count(index=index)
        return result["count"]

    async def delete_documents(self, index: str):
        await self._client.delete_by_query(
            index=index, body={"query": {"match_all": {}}}
        )

    async def close(self):
        await self._client.close()


async def get_connector():
    connector = OpensearchConnector()
    try:
        yield connector
    finally:
        await connector.close()
