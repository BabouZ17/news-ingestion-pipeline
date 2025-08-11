from pydantic import BaseModel


class NewsJob(BaseModel):
    id: str
    name: str
    url: str
