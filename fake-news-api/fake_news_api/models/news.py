from datetime import datetime

from pydantic import BaseModel


class News(BaseModel):
    id: str
    source: str
    title: str
    body: str
    published_at: datetime
