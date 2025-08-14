from datetime import datetime

from pydantic import BaseModel, RootModel, field_serializer


class NewsEmbedding(BaseModel):
    chunk: str
    embedding: list[float]


class News(BaseModel):
    id: str
    source: str
    title: str
    body: str | None = None
    embeddings: list[NewsEmbedding] | None = None
    published_at: datetime

    @field_serializer("published_at", when_used="json")
    def serialize_published_at(self, published_at: datetime):
        return published_at.isoformat()


NewsList = RootModel[list[News]]
