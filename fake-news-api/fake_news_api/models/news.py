from datetime import datetime

from pydantic import BaseModel


class News(BaseModel):
    source: str
    title: str
    content: str
    posted_at: datetime
