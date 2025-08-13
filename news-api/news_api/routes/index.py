import json
from pathlib import Path
from typing import Annotated

from fastapi import Depends
from news_api.connectors.opensearch_connector import OpensearchConnector, get_connector
from news_api.models.custom_response import CustomResponse

NEWS_INDEX_NAME = "news"
NEWS_INDEX_BODY_PATH = Path(__file__).parent.parent.parent / "resources/index.json"


async def create_index(
    opensearch_connector: Annotated[OpensearchConnector, Depends(get_connector)],
) -> CustomResponse:
    body = None
    with open(NEWS_INDEX_BODY_PATH) as f:
        body = json.load(f)

    await opensearch_connector.create_index(index=NEWS_INDEX_NAME, body=body)
    return CustomResponse(message=f"Index {NEWS_INDEX_NAME} created!")
