from datetime import datetime

from pydantic import BaseModel


class NewsEmbedding(BaseModel):
    chunk: str
    embedding: list[float]


class BaseNews(BaseModel):
    id: str
    source: str
    title: str
    body: str | None = None
    published_at: datetime


class News(BaseNews):
    embeddings: list[NewsEmbedding] | None = None


class NewsCount(BaseModel):
    count: int
