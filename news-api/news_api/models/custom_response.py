from pydantic import BaseModel


class CustomResponse(BaseModel):
    message: str
    details: str | None = None
