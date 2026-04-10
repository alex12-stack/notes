from pydantic import BaseModel, Field

import datetime

import enum

from sqlalchemy import Enum


class Is_Public(enum.Enum):
    Public = "public"
    Private = "private"

class Note(BaseModel):
    content: str
    title: str
    folder_id: int
    is_public: Is_Public
    created_at: datetime.datetime

class NotePatch(BaseModel):
    content: str | None
    title: str | None
    folder_id: int | None
    is_public: Is_Public | None
    created_at: datetime.datetime | None