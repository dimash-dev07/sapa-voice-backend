import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ClientCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=255)
    phone: str = Field(min_length=5, max_length=32)
    email: EmailStr | None = None
    company: str | None = None
    notes: str | None = None


class ClientUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=255)
    phone: str | None = None
    email: EmailStr | None = None
    company: str | None = None
    notes: str | None = None


class ClientRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    full_name: str
    phone: str
    email: str | None
    company: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime


class ClientList(BaseModel):
    total: int
    items: list[ClientRead]