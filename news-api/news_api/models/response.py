from pydantic import BaseModel


class Response(BaseModel):
    message: str
    details: str | None = None
