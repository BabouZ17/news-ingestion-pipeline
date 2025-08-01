from datetime import datetime
from pydantic import BaseModel

class News(BaseModel):
    author: str
    content: str
    posted_at: datetime