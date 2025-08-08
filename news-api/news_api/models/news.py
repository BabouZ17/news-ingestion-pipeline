from datetime import datetime

from pydantic import BaseModel


class News(BaseModel):
    id: str
    source: str
    title: str
    body: str | None
    published_at: datetime


class NewsCount(BaseModel):
    count: int
