from uuid import uuid4

from pydantic import BaseModel, Field


class NewsJob(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    url: str
