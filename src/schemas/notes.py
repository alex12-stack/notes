from pydantic import BaseModel, Field
import datetime
import enum
from sqlalchemy import Enum


class IsPublic(enum.Enum):
    Public = "public"
    Private = "private"



class CreateNote(BaseModel):
    content: str
    title: str
    folder_id: int | None = None
    is_public: IsPublic = IsPublic.Private


class GetNotesFiltered(BaseModel):
    content: str | None = None
    title: str | None = None
    is_public: IsPublic = None
    folder_id: int | None = None
    created_at: datetime.datetime | None = None


class PatchNote(BaseModel):
    title: str | None = None
    content: str | None = None
    folder_id: int | None = None
    is_public: IsPublic | None = None