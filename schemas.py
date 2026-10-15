from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl


class CheckRequest(BaseModel):
    urls: list[HttpUrl] = Field(min_length=1)
    timeout: float = Field(5, gt=0)


class CheckJob(CheckRequest):
    check_id: UUID