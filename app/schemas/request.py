import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.request import RequestStatus


class RequestCreate(BaseModel):
    client_phone: str = Field(min_length=5, max_length=32, examples=["+77011234567"])
    text: str = Field(min_length=1, max_length=2000, examples=["Сәлем, бағаңыз қанша?"])


class RequestRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    client_phone: str
    text: str
    response: str | None
    status: RequestStatus
    created_at: datetime
    updated_at: datetime


class RequestList(BaseModel):
    total: int
    items: list[RequestRead]